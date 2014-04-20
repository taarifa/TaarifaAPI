service_schema = {
    'name': {
        'type': 'string',
        'required': True,
    },
    'fields': {
        'type': 'dict',
        'required': True,
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
