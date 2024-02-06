# settings_test.py

from .settings import *

DATABASES = {
    'default': {
            
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb+srv://hamzaashraf:DwlsgnrpBwnz1pN5@cluster0.r0dkzmp.mongodb.net/?retryWrites=true&w=majority',
            'username': 'hamzaashraf',
            'password': 'DwlsgnrpBwnz1pN5',
            'name': 'test_employeeManagment',
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
}
