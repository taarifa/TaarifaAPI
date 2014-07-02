from os import environ, path

from eve import Eve
from eve.io.mongo import Validator
from eve.methods.delete import delete, deleteitem
from eve.methods.post import post

from flask import current_app as app
from flask.ext.bootstrap import Bootstrap
from flask.ext.compress import Compress
from eve_docs import eve_docs

from settings import API_NAME, requests, resources


class KeySchemaValidator(Validator):

    def _validate_dynamicschema(self, schema, field, dct):
        """Validate the dictionary `dct` against a schema dynamically read from
        another document of (potentially) another resource.

        A `dynamicschema` has the following fields:

        * ``resource``: resource to load the schema from
        * ``field``: the field name to use in querying the resource (its value
          is taken as the same field in the current document)
        * ``schema``: the field in the retrieved document holding the schema
        * ``transform``: a function to transform the schema (optional)"""
        query = {schema['field']: self.document[schema['field']]}
        res = app.data.find_one(schema['resource'], None, **query)
        if res:
            dynamic_schema = res[schema['schema']]
            if 'transform' in schema:
                dynamic_schema = schema['transform'](dynamic_schema)
            self._validate_schema(dynamic_schema, field, dct)
        else:
            self._error(field, "Could not find any %s for query %s" %
                        (schema['resource'], query))

    def _validate_keyschema(self, schema, field, dct):
        "Validate all keys of dictionary `dct` against schema `schema`."
        for key, value in dct.items():
            self._validate_schema(schema, key, value)

    def _validate_type_point(self, field, value):
        "Validate a GeoJSON Point."
        schema = {'type': {'type': 'string', 'choices': ['Point']},
                  'coordinates': {'type': 'list',
                                  'minlength': 2,
                                  'maxlength': 2,
                                  'schema': {'type': 'float'}}}
        self._validate_schema(schema, field, value)
        if not -180.0 <= value['coordinates'][0] <= 180.0:
            self._error(field, "Longitude must be in the range -180.0, 180.0")
        if not -90.0 <= value['coordinates'][1] <= 90.0:
            self._error(field, "Latitude must be in the range -90.0, 90.0")

settingsfile = path.join(path.abspath(path.dirname(__file__)), 'settings.py')
api = Eve(API_NAME, validator=KeySchemaValidator, settings=settingsfile)

Bootstrap(api)
Compress(api)
api.register_blueprint(eve_docs, url_prefix='/docs')

resource_url = lambda resource: '/' + api.config['URL_PREFIX'] + '/' + resource


def get_schema(resource):
    "Get the schema for a given resource."
    return api.config['DOMAIN'][resource]['schema']


def add_document(resource, document):
    "Add a new document to the given resource."
    with api.test_request_context(resource_url(resource)):
        return post(resource, payl=document)


def delete_document(resource, document):
    "Delete a given documents of the given resource."
    with api.test_request_context(resource_url(resource)):
        return deleteitem(resource, document)


def delete_documents(resource):
    "Delete all documents of the given resource."
    with api.test_request_context(resource_url(resource)):
        return delete(resource)


def register_resource(resource, schema, source, filt):
    """Register a new resource with the given schema and filter. This creates
    a new endpoint for the resource, whereas documents are stored in the source
    collection and a filter is applied.

    .. note:: This method calls Flask's add_url_rule under the hood, which
        raises an AssertionError in debugging mode when used after the first
        request was served."""
    api.register_resource(resource, {'item_title': resource,
                                     'schema': schema,
                                     'datasource': {'source': source,
                                                    'filter': filt}})


def register_resources(resources, conf):
    "Add existing resources as API resources."
    for res in resources:
        if 'endpoint' in res:
            schema = conf['schema']
            schema.update(res['fields'])
            register_resource(res['endpoint'], schema, conf['source'],
                              {conf['key']: res[conf['key']]})

register_services = lambda d: register_resources(d, requests)
register_facilities = lambda d: register_resources(d, resources)


def add_services():
    "Add existing services as API resources."
    with api.app_context():
        register_services(api.data.driver.db['services'].find())


def add_facilities():
    "Add existing facilities as API resources."
    with api.app_context():
        register_facilities(api.data.driver.db['facilities'].find())

# Register hook to add resource for service when inserted into the database
# FIXME: this hook fails in debug mode due an AssertionError raised by Flask
api.on_insert_services += register_services
api.on_insert_facilities += register_facilities
add_services()
add_facilities()


def main():
    # Heroku support: bind to PORT if defined, otherwise default to 5000.
    if 'PORT' in environ:
        port = int(environ.get('PORT'))
        host = '0.0.0.0'
    else:
        port = 5000
        host = '127.0.0.1'
    api.run(host=host, port=port)

if __name__ == '__main__':
    main()
