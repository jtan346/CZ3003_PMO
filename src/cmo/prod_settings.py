"""Production Django settings.
"""
from cmo.common_settings import *  # pylint: disable=wildcard-import,unused-wildcard-import

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmodb',
        'USER': 'root',
        'PASSWORD': 'cmodb',
        'HOST': 'db',
        'PORT': '3306',
    }
}
