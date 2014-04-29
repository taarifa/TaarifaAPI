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
                    'file'],
    },
    'required': {
        'type': 'boolean',
        'default': False,
    },
    'readonly': {
        'type': 'boolean',
        'default': False,
    },
    'minlength': {
        'type': 'integer',
    },
    'maxlength': {
        'type': 'integer',
    },
    'min': {
        'type': 'integer',
    },
    'max': {
        'type': 'integer',
    },
    'allowed': {
        'type': 'list',
    },
    'empty': {
        'type': 'boolean',
        'default': True,
    },
    'items': {
        'type': 'list',
    },
    'scheam': {
        'type': 'dict',
    },
    'unique': {
        'type': 'boolean',
        'default': False,
    },
    'data_relation': {
        'type': 'dict',
        'schema': {
            'resource': {
                'type': 'string',
            },
            'field': {
                'type': 'string',
            },
            'embeddable': {
                'type': 'boolean',
                'default': False,
            },
            'version': {
                'type': 'boolean',
                'default': False,
            },
        },
    },
    'nullable': {
        'type': 'boolean',
        'default': False,
    },
    'default': {},
    'versioned': {
        'type': 'boolean',
        'default': True,
    },
}

# Service attributes conforming to the Open311 GeoReport v2 service definition:
# http://wiki.open311.org/GeoReport_v2#Response_2
attribute_schema = {
    'variable': {
        'type': 'boolean',
        'default': False,
    },
    'code': {
        'type': 'string',
        'unique': True,
    },
    'datatype': {
        'type': 'string',
        'allowed': ['string',
                    'number',
                    'datetime',
                    'text',
                    'singlevaluelist',
                    'multivaluelist'],
    },
    'required': {
        'type': 'boolean',
        'default': False,
    },
    'datatype_description': {
        'type': 'string',
    },
    'order': {
        'type': 'integer',
    },
    'description': {
        'type': 'string',
    },
    'values': {
        'type': 'list',
        'schema': {
            'key': {
                'type': 'string',
            },
            'name': {
                'type': 'string',
            },
        },
    },
}

# Service conforming to the Open311 GeoReport v2 service definition:
# http://wiki.open311.org/GeoReport_v2#Response
# name is an extra fields to denote the dynamically created endpoint for the
# service
service_schema = {
    'jurisdiction_id': {
        'type': 'string',
    },
    'service_code': {
        'type': 'string',
        'required': True,
        'unique': True,
    },
    'service_name': {
        'type': 'string',
        'required': True,
    },
    'description': {
        'type': 'string',
    },
    'metadata': {
        'type': 'boolean',
        'default': False,
    },
    'type': {
        'type': 'string',
        'allowed': ['realtime', 'batch', 'blackbox'],
        'default': 'realtime',
    },
    'keywords': {
        'type': 'list',
        'schema': {
            'type': 'string',
        },
    },
    'group': {
        'type': 'string',
    },
    'attributes': {
        'type': 'list',
        'schema': attribute_schema,
    },
    'name': {
        'type': 'string',
    },
}

# Service request conforming to the Open311 GeoReport v2 request definition:
# http://wiki.open311.org/GeoReport_v2#POST_Service_Request
# http://wiki.open311.org/GeoReport_v2#GET_Service_Requests
request_schema = {
    'service_code': {
        'type': 'string',
        'required': True,
        'data_relation': {
            'resource': 'services',
            'field': 'service_code',
        }
    },
    # FIXME: at least one of the location fields is required
    'lat': {
        'type': 'float',
    },
    'long': {
        'type': 'float',
    },
    'address_string': {
        'type': 'string',
    },
    'address_id': {
        'type': 'string',
    },
    'zipcode': {
        'type': 'string',
    },
    'email': {
        'type': 'string',  # FIXME: add email validator?
    },
    'device_id': {
        'type': 'string',
    },
    'account_id': {  # FIXME: account management?
        'type': 'string',
    },
    'first_name': {
        'type': 'string',
    },
    'last_name': {
        'type': 'string',
    },
    'phone': {
        'type': 'string',
    },
    'description': {
        'type': 'string',
    },
    'media_url': {
        'type': 'string',
    },
    'status': {
        'type': 'string',
        'allowed': ['open', 'closed'],
        'default': 'open',
    },
    'status_notes': {
        'type': 'string',
    },
    'agency_responsible': {
        'type': 'string',
    },
    'service_notice': {
        'type': 'string',
    },
    # requested_datetime = _created
    # updated_datetime = _updated
    'expected_datetime': {
        'type': 'datetime',
    },
}
