"""
Generate links for the landing page of the API.
"""

import logging
from typing import Optional

import pyramid.request

import pyramid_ogcapi

_LOG = logging.getLogger(__name__)


def self_link(request: pyramid.request.Request, title: str = "this document (JSON)") -> dict:
    """Return a link to the current landing page."""
    return {
        "href": request.current_route_url(_query={"f": "json"}),
        "rel": "self",
        "type": "application/json",
        "title": title,
    }


def sub_links(request: pyramid.request.Request, api_name: str, route_prefix: str = "") -> list[dict]:
    """Return a list of links to the endpoints of the API."""

    spec = request.registry.settings[api_name]["spec"]

    current_route_name = request.matched_route.name
    if current_route_name.endswith("_json") or current_route_name.endswith("_html"):
        current_route_name = current_route_name[:-5]

    current_path = None
    for path in spec["paths"]:
        route_name = pyramid_ogcapi.path2route_name_prefix(path, route_prefix)
        if route_name == current_route_name:
            current_path = path.rstrip("/")
            break

    sub_paths = []
    for path, config in spec["paths"].items():
        if path != "/" and path.startswith(current_path + "/") and "{" not in path and "get" in config:
            extra_path = path[len(current_path) + 1 :]
            if "/" not in extra_path:
                sub_paths.append(path)

    links = []
    for path in sub_paths:
        links.append(link(request, api_name, path, route_prefix=route_prefix))

    return links


def link(
    request: pyramid.request.Request,
    api_name: str,
    path: str,
    relation_type: Optional[str] = None,
    json: bool = False,
    route_prefix: str = "",
) -> dict:
    """Return a link to an endpoint specified by its path and link relation type."""
    spec = request.registry.settings[api_name]["spec"]
    route_name_prefix = pyramid_ogcapi.path2route_name_prefix(path, route_prefix)
    route_name = route_name_prefix + ("_json" if json else "_html")
    path_config = spec["paths"][path]

    used_mime_type = "application/json" if json else "text/html"
    if json:
        for mime_type in path_config["get"]["responses"].get("200", {}).get("content", {}):
            if "json" in mime_type:
                used_mime_type = mime_type
                break

    return {
        "href": request.route_url(route_name),
        "rel": relation_type or route_name_prefix,
        "type": used_mime_type,
        "title": path_config["get"]["summary"],
    }
