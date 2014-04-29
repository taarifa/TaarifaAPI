"""Global API configuration."""

from os import environ
from urlparse import urlparse

from schemas import facility_schema, request_schema, service_schema

API_NAME = 'Taarifa'
URL_PREFIX = 'api'
if 'EVE_DEBUG' in environ:
    DEBUG = True

if 'MONGOLAB_URI' in environ:
    url = urlparse(environ['MONGOLAB_URI'])
    MONGO_HOST = url.hostname
    MONGO_PORT = url.port
    MONGO_USERNAME = url.username
    MONGO_PASSWORD = url.password
    MONGO_DBNAME = url.path[1:]
else:
    MONGO_DBNAME = API_NAME

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

services = {
    "schema": service_schema,
}

requests = {
    "schema": request_schema,
}

facilities = {
    "item_title": "facility",
    "schema": facility_schema,
}

DOMAIN = {
    'services': services,
    'requests': requests,
    'facilities': facilities,
}

# FIXME: Temporarily allow CORS requests for development purposes
X_DOMAINS = "*"
