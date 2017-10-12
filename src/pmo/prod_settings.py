"""Production Django settings.
"""
from pmo.common_settings import *  # pylint: disable=wildcard-import,unused-wildcard-import

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pmodb',
        'USER': 'root',
        'PASSWORD': 'pmodb',
        'HOST': 'db',
        'PORT': '3306',
    }
}
