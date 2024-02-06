# settings_test.py

from .settings import *

DATABASES = {
    'default': {
            
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb_uri',
            'username': 'uname',
            'password': 'password',
            'name': 'test_dbname',
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
}
