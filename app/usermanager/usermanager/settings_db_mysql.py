from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'usermanager',
        'USER': 'mysql',
        'PASSWORD': 'mysql',
        'HOST': 'mysql',
        'PORT': '3306',
    },
}
