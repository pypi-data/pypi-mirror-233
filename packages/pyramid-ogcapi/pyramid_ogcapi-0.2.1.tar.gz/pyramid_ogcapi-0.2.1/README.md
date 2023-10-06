# Pyramid OGC API

Tools used to facilitate the development of OGC API services with Pyramid.
Provide template the the HTML vies of the API, have a generic one for la kind of view.
Automatically create the routes and the views based on the OpenAPI 3 specification file and the OGC API common consideration.
Provide some functions to facilitate the create of the template.
Provide some functions to facilitate the create of the api.
Provide some functions to facilitate the creation od an OpenLayers Map.

OGC API common consideration that we will consider to create some facilitation:

- The f argument to switch between the HTML and the JSON view.
- The link definition.
- The paging definition.

It will also provide an example of the OGC API Feature service with:

- The crs parameter..
- The CQL filter based on (pygeofiler)[https://pypi.org/project/pygeofilter/].
- The CRUD interface.

## Installation

```bash
python3 -m pip install pyramid-ogcapi
```

## Getting started

Get the OGC API bundled specifications from the [OGC GitHub organization](https://github.com/opengeospatial/),
and save it as `ogcapi-bundled.json`.

Add in your configuration:

```python
config.include("pyramid_ogcapi")
config.pyramid_openapi3_spec('ogcapi-bundled.json', apiname='ogcapi')
config.pyramid_openapi3_add_explorer(apiname='ogcapi')
config.pyramid_ogcapi_register_routes(apiname='ogcapi')
```

Integrate with [jsonschema_gentypes](https://pypi.org/project/jsonschema-gentypes/).

Add the following views:

```python

from pyramid import view_config
from pyramid_ogcapi import request_dict
from .ogcapi import OgcapiCollectionsCollectionidGet, OgcapiCollectionsCollectionidGetResponse

@request_dict
def myview(
  request: pyramid.request.Request,
  request_typed: OgcapiCollectionsCollectionidGet,
) -> OgcapiCollectionsCollectionidGetResponse:
    return {...}

```

Integrate with [jsonschema_gentypes](https://pypi.org/project/jsonschema-gentypes/)

## Start example

Run the example:

```bash
make run
```

Open the [Swagger UI](http://localhost:9123/ogcapi/docs/).

Open the [OpenAPI main page](http://localhost:9123/ogcapi/).

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```

The `prospector` tests should pass.

The code should be typed.

The code should be tested with `pytests`.
