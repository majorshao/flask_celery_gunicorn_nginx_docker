import os

ENVIRONMENT = 'prod'

SEARCH_CONFIG = {}
SEARCH_CONFIG.update(dict.fromkeys(
    ['prod'], {
        'ALLOWED_URLS': {
            'name':
                {'url': 'https://names.mcquay.me/api/v0', 'payload': ''},
            'joke':
                {'url': 'http://api.icndb.com/jokes/random',
                 'payload': {'firstName': 'John', 'lastName': 'Doe', 'limitTo': '[nerdy]'}}
        }
    }))
