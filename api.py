import json
from os import environ

from eve import Eve
from eve.io.mongo import Validator

from settings import API_NAME, URL_PREFIX


class KeySchemaValidator(Validator):
    def _validate_keyschema(self, schema, field, dct):
        "Validate all keys of dictionary `dct` against schema `schema`."
        for key, value in dct.items():
            self._validate_schema(schema, key, value)

api = Eve(API_NAME, validator=KeySchemaValidator)


def add_document(resource, document):
    "Add a new document to the given resource."
    return api.test_client().post('/' + URL_PREFIX + '/' + resource,
                                  data=json.dumps(document),
                                  content_type='application/json')

if __name__ == '__main__':
    # Heroku support: bind to PORT if defined, otherwise default to 5000.
    if 'PORT' in environ:
        port = int(environ.get('PORT'))
        host = '0.0.0.0'
    else:
        port = 5000
        host = '127.0.0.1'
    api.run(host=host, port=port)
