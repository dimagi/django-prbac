
SECRET_KEY='Not a secret key at all, actually'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django-prbac.db',
    }
}

INSTALLED_APPS = [
    'django_prbac',
    'south',
]
