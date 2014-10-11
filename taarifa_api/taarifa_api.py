from os import environ, path

from eve import Eve
from eve.io.mongo import Validator
from eve.methods.delete import delete, deleteitem
from eve.methods.post import post
from eve.render import send_response

from flask import request, current_app as app
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


@api.route('/' + api.config['URL_PREFIX'] + '/<facility_code>/values/<field>')
def resource_values(facility_code, field):
    """Get unique values for the specified resource field."""
    query = dict(request.args.items())
    query['facility_code'] = facility_code
    resources = app.data.driver.db['resources'].find(query)
    return send_response('resources',
                         (sorted(resources.distinct(field)),))


@api.route('/' + api.config['URL_PREFIX'] + '/<facility_code>/count/<field>')
def resource_count(facility_code, field):
    """Get number of resources grouped a given field."""
    query = dict(request.args.items())
    query['facility_code'] = facility_code
    data = app.data.driver.db['resources'].group(
        field.split(','), query, initial={'count': 0},
        reduce="function(curr, result) {result.count++;}")
    return send_response('resources', [data])


@api.route('/' + api.config['URL_PREFIX'] + '/<facility_code>/sum/<group>/<field>')
def resource_sum(facility_code, group, field):
    """Get group sum of a given field."""
    fields = field.split(',')
    query = dict(request.args.items())
    query['facility_code'] = facility_code
    data = app.data.driver.db['resources'].aggregate([
        {
            "$match": query
        },
        {
            "$group": {
                "_id": '$' + group,
                "sum": {'$sum': {'$add': ['$' + f for f in fields] }},
            }
        },
        {"$sort": {group: 1}}])['result']
    return send_response('resources', [data])


@api.route('/' + api.config['URL_PREFIX'] + '/<facility_code>/diff/<group>/<field_a>/<field_b>')
def resource_diff(facility_code, group, field_a, field_b):
    """Get group difference in sum of two fields."""
    subtrahends = field_a.split(',')
    minuends = field_b.split(',')
    query = dict(request.args.items())
    query['facility_code'] = facility_code
    data = app.data.driver.db['resources'].aggregate([
        {
            '$match': query
        },
        {
            '$group': {
                '_id': '$' + group,
                'sum_subtrahend': {'$sum': {'$add': ['$' + f for f in subtrahends] }},
                'sum_minuend': {'$sum': {'$add': ['$' + f for f in minuends] }}
            }
        },
        {
            '$project': {
                '_id': 1,
                'sum_subtrahend': 1,
                'sum_minuend': 1,
                'difference': {'$subtract': ['$sum_subtrahend', '$sum_minuend']}
            }
        },
        {'$sort': {group: 1}}])['result']
    return send_response('resources', [data])


@api.route('/' + api.config['URL_PREFIX'] + '/<facility_code>/ratio/<group>/<field_a>/<field_b>')
def resource_ratio(facility_code, group, field_a, field_b):
    """Get group ratio of sum of two fields."""
    dividends = field_a.split(',')
    divisors = field_b.split(',')
    query = dict(request.args.items())
    query['facility_code'] = facility_code
    data = app.data.driver.db['resources'].aggregate([
        {
            '$match': query
        },
        {
            '$group': {
                '_id': '$' + group,
                'sum_dividend': {'$sum': {'$add': ['$' + f for f in dividends] }},
                'sum_divisor': {'$sum': {'$add': ['$' + f for f in divisors] }}
            }
        },
        {
            '$project': {
                '_id': 1,
                'sum_dividend': 1,
                'sum_divisor': 1,
                'ratio': {'$divide': ['$sum_dividend', '$sum_divisor']}
            }
        },
        {'$sort': {group: 1}}])['result']
    return send_response('resources', [data])


@api.route('/' + api.config['URL_PREFIX'] + '/<facility_code>/product_sum/<group>/<field_a>/<field_b>')
def resource_product_sum(facility_code, group, field_a, field_b):
    """Get group sum of product of two fields."""
    multiplicands = field_a.split(',')
    multipliers = field_b.split(',')
    query = dict(request.args.items())
    query['facility_code'] = facility_code
    data = app.data.driver.db['resources'].aggregate([
        {
            '$match': query
        },
        {
            '$group': {
                '_id': '$' + group,
                'product_sum': {
                    '$sum': {
                        '$multiply': [
                            {'$add': ['$' + f for f in multiplicands]},
                            {'$add': ['$' + f for f in multipliers]}
                        ]
                    }
                }
            }
        },
        {'$sort': {group: 1}}])['result']
    return send_response('resources', [data])


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
