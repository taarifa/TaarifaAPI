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

# Service conforming to the Open311 GeoReport v2 service definition:
# http://wiki.open311.org/GeoReport_v2#Response
# name, fields and unique are extra fields
service_schema = {
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
    'name': {
        'type': 'string',
        'required': True,
    },
    'fields': {
        'type': 'dict',
        'required': True,
        'keyschema': field_schema,
    },
    'unique': {
        'type': 'boolean',
        'default': False,
    },
}
