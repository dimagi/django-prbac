"""
Settings just for running the django-prbac tests or checking out
the admin site.
"""

SECRET_KEY = 'Not a secret key at all, actually'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django-prbac.db',
    }
}

INSTALLED_APPS = [
    # Django apps necessary to run the admin site
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    # And this app
    'django_prbac',
]

STATIC_URL = '/static/'

ROOT_URLCONF = 'django_prbac.urls'

MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]
