"""Pyramid OGC API extension."""

import json
import logging
from typing import Any, Callable, Optional, cast

import pyramid.config
import pyramid.request
import pyramid.response
import pyramid_openapi3
import yaml
from openapi_core.spec import Spec
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.threadlocal import get_current_request

_LOG = logging.getLogger(__name__)


def includeme(config: pyramid.config.Configurator) -> None:
    """Include the OGC API extension."""
    config.include("pyramid_openapi3")
    config.add_directive("pyramid_ogcapi_register_routes", register_routes)
    config.add_route("pyramid_ogcapi.spec", "/openapi.yaml")


class _OgcType:
    def __init__(self, val: str, config: pyramid.config.Configurator):
        del config
        self.val = val

    def phash(self) -> str:
        """Return a string that uniquely identifies the predicate."""

        return f"ogc_type = {self.val}"

    def __call__(self, context: Any, request: pyramid.request.Request) -> bool:
        """Return a true value if the predicate should be used."""

        del context

        if request.params.get("f") in ["html", "json"]:
            return request.params["f"].lower() == self.val  # type: ignore
        return request.accept.best_match(["text/html", "application/json", "application/geo+json"]).split("/")[1].split("+")[-1] == self.val  # type: ignore


def _get_view(
    views: Any, method_config: Any, route_name: str, path: str, helps: list[str], with_help: bool = True
) -> Optional[Callable[[pyramid.request.Request], Any]]:
    content = method_config.get("responses", {}).get("200", {}).get("content", {})
    json_content = content.get("application/json", {}) or content.get("application/geo+json", {})
    example = json_content.get("example", {})
    description = method_config.get("description", "")
    description = description.content() if hasattr(description, "content") else description
    if description:
        description = "\n\n        " + description

    if with_help:
        helps.append(
            f'''
    @pyramid_ogcapi.typed_request
    def {route_name.lower()}(self, pyramid_request: pyramid.request.Request, request: Any) -> Any:
        """
        Get the result for the path '{path}'.{description}
        """

        return {example.content() if hasattr(example, 'content') else example}'''
        )

    if hasattr(views, route_name.lower()):
        return cast(Callable[[pyramid.request.Request], Any], getattr(views, route_name.lower()))
    _LOG.error("Missing view named '%s'", route_name.lower())

    return None


def path2route_name_prefix(path: str, route_prefix: str = "") -> str:
    return route_prefix + (
        "landing_page"
        if path == "/"
        else path.lstrip("/").replace("/", "_").replace("{", "").replace("}", "").replace("-", "_")
    )


class _SpecProxy:
    """
    Proxy used to generate a spec with the correct servers.
    """

    def __init__(self, spec: dict[str, Any], settings: dict[str, Any]) -> None:
        self._spec = spec
        self._settings = settings

    def keys(self) -> list[str]:
        """Return the keys of the mapping object."""

        return self._spec.keys()

    def values(self) -> list[Any]:
        """Return the values of the mapping object."""

        return self._spec.values()

    def items(self) -> list[tuple[str, Any]]:
        """Return the items of the mapping object."""

        return self._spec.items()

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for key if key is in the dictionary, else default."""

        if key == "servers":
            request = get_current_request()
            return [
                {
                    "url": f"http://localhost/{p.rstrip('/')}"
                    if request is None
                    else request.route_url("landing_page_html")
                }
                for p in self._settings.get("pyramid_ogcapi", {}).get("route_prefix", [])
            ]

        return self._spec.get(key, default)

    def __getitem__(self, key) -> Any:
        if key == "servers":
            self.get(key)
        return self._spec[key]

    def __contains__(self, key) -> bool:
        return key in self._spec

    def __len__(self) -> int:
        return len(self._spec)

    def __truediv__(self, other) -> Any:
        return self._spec / other


def register_routes(
    config: pyramid.config.Configurator,
    views: Any,
    apiname: str = "pyramid_openapi3",
    route_prefix: str = "",
    path_template: Optional[dict[str, str]] = None,
    json_renderer: str = "json",
    spec_route_name: str = "pyramid_ogcapi.spec",
    spec_route: str = "/ogcapi.yaml",
    spec_permission: str = NO_PERMISSION_REQUIRED,
) -> None:
    """
    Register routes of an OSC API application.

    :param route_name_ext: Extension's key for using a ``route_name`` argument
    :param root_factory_ext: Extension's key for using a ``factory`` argument
    """

    if path_template is None:
        path_template = {}

    config.registry.settings.setdefault("pyramid_ogcapi", {}).setdefault("route_prefix", []).append(
        config.route_prefix
    )

    def action() -> None:
        assert path_template is not None

        settings = config.registry.settings
        settings[apiname]["spec"] = _SpecProxy(settings[apiname]["spec"], settings)

        # Add the spec view
        def spec_view(request: pyramid.request.Request) -> pyramid.response.Response:
            with open(config.registry.settings[apiname]["filepath"], encoding="utf-8") as f:
                spec = yaml.load(f, Loader=yaml.SafeLoader)
                if "servers" not in spec:
                    spec["servers"] = [
                        {
                            "url": request.route_url("landing_page_html"),
                        }
                    ]
                request.response.text = yaml.dump(spec, Dumper=yaml.SafeDumper)
            return request.response

        assert spec_route_name != config.registry.settings[apiname]["spec_route_name"]
        config.registry.settings[apiname]["spec_route_name"] = spec_route_name
        config.add_route(spec_route_name, spec_route)
        config.add_view(route_name=spec_route_name, permission=spec_permission, view=spec_view)
        ###

        config.add_route_predicate("ogc_type", _OgcType)

        spec = config.registry.settings[apiname]["spec"]

        # Resolve the $ref
        def resolve_ref(obj: Any, spec: dict[str, Any], path) -> None:
            if len(path) > 100:
                _LOG.debug("Abort recursive path: %s", ", ".join(path))
                return
            if isinstance(obj, dict):
                if "$ref" in obj:
                    ref = obj["$ref"]
                    if ref.startswith("#/"):
                        ref = ref[2:]
                    else:
                        raise NotImplementedError(f"Only local reference are supported: {ref}")
                    ref_split = ref.split("/")
                    new_obj = spec
                    for ref_part in ref_split:
                        new_obj = new_obj[ref_part]
                    del obj["$ref"]
                    obj.update(new_obj)

                for key, val in obj.items():
                    resolve_ref(val, spec, [*path, key])
            elif isinstance(obj, list):
                for val in obj:
                    resolve_ref(val, spec, [*path, "[]"])

        resolve_ref(spec["paths"], spec, [])

        helps: list[str] = []
        view_path = config.registry.settings.setdefault("pyramid_ogcapi", {}).setdefault("view_path", {})
        for pattern, path_config in spec.get("paths", {}).items():
            route_name = path2route_name_prefix(pattern, route_prefix)

            for method, method_config in path_config.items():
                content = method_config.get("responses", {}).get("200", {}).get("content", {})
                json_html = (
                    method == "get"
                    and ("application/json" in content or "application/geo+json" in content)
                    and "text/html" in content
                )
                # Create the routes and views for the HTML and JSON based on the same data
                if json_html:
                    config.add_route(
                        f"{route_name}_html",
                        pattern,
                        request_method="GET",
                        ogc_type="html",
                    )
                    config.add_view(
                        _get_view(views, method_config, route_name, pattern, helps),
                        route_name=f"{route_name}_html",
                        renderer=path_template.get(pattern, "pyramid_ogcapi:templates/default.mako"),
                        openapi=True,
                    )
                    view_path[f"{route_name}_html"] = path_config
                    config.add_route(
                        f"{route_name}_json",
                        pattern,
                        request_method="GET",
                        ogc_type="json",
                    )
                    config.add_view(
                        _get_view(views, method_config, route_name, pattern, helps, with_help=False),
                        route_name=f"{route_name}_json",
                        renderer=json_renderer,
                        openapi=True,
                    )
                    view_path[f"{route_name}_json"] = path_config

                method_route_name = f"{route_name}_{method}" if method != "get" else route_name

                # Create the routes and views for all the other cases
                for content_type in content.keys():
                    if json_html and content_type in (
                        "application/json",
                        "application/geo+json",
                        "text/html",
                    ):
                        continue

                    renderer = None
                    if content_type in ("application/json", "application/geo+json"):
                        renderer = json_renderer
                    elif "text/html" in content:
                        renderer = path_template.get(pattern, "pyramid_ogcapi:templates/default.mako")
                    current_route_name = (
                        f"{method_route_name}_{content_type.replace('/', '_')('+', '_')('.', '_')('-', '_')}"
                        if len(content) > 1
                        else method_route_name
                    )

                    config.add_route(
                        current_route_name,
                        pattern,
                        request_method=method.upper(),
                    )
                    config.add_view(
                        _get_view(views, method_config, current_route_name, pattern, helps),
                        route_name=current_route_name,
                        renderer=renderer,
                        openapi=True,
                    )
        _LOG.debug("Use the following code to add it:\n%s", "\n\n".join(helps))

    config.action(("pyramid_openapi3_register_routes",), action, order=pyramid.config.PHASE1_CONFIG)


def typed_request(
    func: Callable[[Any, pyramid.request.Request, Any], Any]
) -> Callable[[Any, pyramid.request.Request], Any]:
    """
    Decorate for openapi views to have a typed request.

    To be used with the generated types by jsonschema_gentype
    """

    def wrapper(obj: Any, request: pyramid.request.Request) -> Any:
        _typed_request: dict[str, Any] = {}
        try:
            _typed_request["request_body"] = request.json_body
        except json.JSONDecodeError:
            pass
        _typed_request["path"] = request.matchdict
        _typed_request["query"] = request.params

        return func(obj, request, _typed_request)

    return wrapper
