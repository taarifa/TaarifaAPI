"""Global API configuration."""

from os import environ

# This module is both imported from and executed. In the former case only
# relative imports are supported, in the latter only absolute.
try:
    from schemas import facility_schema, request_schema, resource_schema, \
        service_schema
except ImportError:
    from taarifa_api.schemas import facility_schema, request_schema, \
        resource_schema, service_schema

API_NAME = 'TaarifaAPI'
URL_PREFIX = environ.get('API_URL_PREFIX', 'api')
if 'EVE_DEBUG' in environ:
    DEBUG = True
    TRAP_HTTP_EXCEPTIONS = True
    TRAP_BAD_REQUEST_KEY_ERRORS = True

if 'MONGO_URI' in environ:
    MONGO_URI = environ['MONGO_URI']
else:
    MONGO_DBNAME = environ.get('MONGO_DBNAME', API_NAME)

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']

services = {
    "schema": service_schema,
    "transparent_schema_rules": True,
}

requests = {
    "schema": request_schema,
    "source": "requests",
    "key": "service_code",
}

facilities = {
    "item_title": "facility",
    "schema": facility_schema,
    "transparent_schema_rules": True,
}

resources = {
    "schema": resource_schema,
    "source": "resources",
    "key": "facility_code",
}

DOMAIN = {
    'services': services,
    'requests': requests,
    'facilities': facilities,
    'resources': resources,
}

# Allow requesting up to 100 results per page
PAGINATION_LIMIT = 100
# FIXME: Temporarily allow CORS requests for development purposes
X_DOMAINS = "*"
# Enable Flask-Compress in debug mode
COMPRESS_DEBUG = True
# gzip compression level
COMPRESS_LEVEL = 9
# Enable document version control
VERSIONING = True
# For debugging
# TRAP_HTTP_EXCEPTIONS = True
# TRAP_BAD_REQUEST_KEY_ERRORS = True
