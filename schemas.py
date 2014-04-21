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

service_schema = {
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
    'description': {
        'type': 'string',
    },
    'group': {
        'type': 'string',
    },
    'keywords': {
        'type': 'list',
        'schema': {
            'type': 'string',
        },
    },
    'protocol_type': {
        'type': 'string',
    },
    'service_name': {
        'type': 'string',
        'required': True,
    },
    'service_code': {
        'type': 'string',
        'required': True,
        'unique': True,
    },
}
