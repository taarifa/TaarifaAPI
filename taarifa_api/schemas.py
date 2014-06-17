boolean_field_false = {'type': 'boolean', 'default': False}
boolean_field_true = {'type': 'boolean', 'default': True}
integer_field = {'type': 'integer'}
float_field = {'type': 'float'}
list_field = {'type': 'list'}
string_field = {'type': 'string'}
unique_string_field = {'type': 'string', 'unique': True}
required_string_field = {'type': 'string', 'required': True}
unique_req_string_field = {'type': 'string', 'required': True, 'unique': True}
dict_field = {'type': 'dict'}
data_relation = {'type': 'dict',
                 'schema': {'resource': string_field,
                            'field': string_field,
                            'embeddable': boolean_field_false,
                            'version': boolean_field_false}}

field_schema = {
    'type': {
        'type': 'string',
        'allowed': ['string',
                    'boolean',
                    'integer',
                    'float',
                    'number',
                    'datetime',
                    'dict',
                    'list',
                    'objectid',
                    'file',
                    'point'],
    },
    'required': boolean_field_false,
    'readonly': boolean_field_false,
    'minlength': integer_field,
    'maxlength': integer_field,
    'min': integer_field,
    'max': integer_field,
    'allowed': list_field,
    'empty': boolean_field_true,
    'items': list_field,
    'schema': dict_field,
    'unique': boolean_field_false,
    'data_relation': data_relation,
    'nullable': boolean_field_false,
    'default': {},
    'versioned': boolean_field_true,
    'label': string_field,
}

# Service attributes conforming to the Open311 GeoReport v2 service definition:
# http://wiki.open311.org/GeoReport_v2#Response_2
attribute_schema = {
    'variable': boolean_field_true,
    'code': unique_string_field,
    'datatype': {
        'type': 'string',
        'allowed': ['string',
                    'number',
                    'datetime',
                    'text',
                    'singlevaluelist',
                    'multivaluelist'],
    },
    'required': boolean_field_false,
    'datatype_description': string_field,
    'order': integer_field,
    'description': string_field,
    'values': {
        'type': 'list',
        'schema': {
            'key': string_field,
            'name': string_field,
        },
    },
    # This field is not part of the Open311 service definition, but allows to
    # enforce foreign key constraints in the API
    'relation': data_relation,
}

# Service conforming to the Open311 GeoReport v2 service definition:
# http://wiki.open311.org/GeoReport_v2#Response
# endpoint is an extra fields to denote the dynamically created endpoint for
# the service
service_schema = {
    'jurisdiction_id': string_field,
    'service_code': unique_req_string_field,
    'service_name': required_string_field,
    'description': string_field,
    'metadata': boolean_field_false,
    'type': {
        'type': 'string',
        'allowed': ['realtime', 'batch', 'blackbox'],
        'default': 'realtime',
    },
    'keywords': {
        'type': 'list',
        'schema': string_field,
    },
    'group': string_field,
    'attributes': {
        'type': 'list',
        'schema': attribute_schema,
    },
    'endpoint': string_field,
}


def attributes2schema(attributes):
    """Transform the list of Open311 service attributes into a valid Cerberus
    schema (see: http://wiki.open311.org/GeoReport_v2#Response_2)."""
    schema = {}
    for attr in attributes:
        if attr['variable']:
            typ = attr['datatype']
            # Attributes of type 'text', 'singlevaluelist', 'multivaluelist'
            # are represented as strings
            if typ in ['text', 'singlevaluelist', 'multivaluelist']:
                typ = 'string'
            field = attr['code']
            schema[field] = {'type': typ, 'required': attr['required']}
            # If the attribute has a list of values, use their keys as allowed
            # values for this attribute
            if 'values' in attr:
                schema[field]['allowed'] = [v['key'] for v in attr['values']]
            # If the attribute has a data relation, enforce the foreign key
            # constraint on it
            if 'relation' in attr:
                schema[field]['data_relation'] = attr['relation']
    return schema

# Service request conforming to the Open311 GeoReport v2 request definition:
# http://wiki.open311.org/GeoReport_v2#POST_Service_Request
# http://wiki.open311.org/GeoReport_v2#GET_Service_Requests
request_schema = {
    'jurisdiction_id': string_field,
    'service_code': {
        'type': 'string',
        'required': True,
        'data_relation': {
            'resource': 'services',
            'field': 'service_code',
        }
    },
    'attribute': {
        'type': 'dict',
        'dynamicschema': {
            'resource': 'services',
            'field': 'service_code',
            'schema': 'attributes',
            'transform': attributes2schema,
        },
    },
    # FIXME: at least one of the location fields is required
    'lat': float_field,
    'long': float_field,
    'address_string': string_field,
    'address_id': string_field,
    'zipcode': string_field,
    'email': string_field,
    'device_id': string_field,
    'account_id': string_field,
    'first_name': string_field,
    'last_name': string_field,
    'phone': string_field,
    'description': string_field,
    'media_url': string_field,
    'status': {
        'type': 'string',
        'allowed': ['open', 'closed'],
        'default': 'open',
    },
    'status_notes': string_field,
    'agency_responsible': string_field,
    'service_notice': string_field,
    # requested_datetime = _created
    # updated_datetime = _updated
    'expected_datetime': {
        'type': 'datetime',
    },
}

facility_schema = {
    'jurisdiction_id': string_field,
    'facility_code': unique_req_string_field,
    'facility_name': required_string_field,
    'description': string_field,
    'keywords': {
        'type': 'list',
        'schema': string_field,
    },
    'group': string_field,
    'attributes': {
        'type': 'list',
        'schema': attribute_schema,
    },
    'endpoint': string_field,
    'fields': {
        'required': True,
        'type': 'dict',
        'keyschema': field_schema,
    },
}

resource_schema = {
    'facility_code': {
        'type': 'string',
        'required': True,
        'data_relation': {
            'resource': 'facilities',
            'field': 'facility_code',
        }
    },
}
