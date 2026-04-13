"""
Django settings for budget_tracker project.

This file stores the main configuration for the entire Django project.
When Django starts, it reads these values to know which apps are installed,
which database to use, where templates live, and how login should behave.
"""

from pathlib import Path

# BASE_DIR points to the main project folder and is used to build paths to
# files like the SQLite database.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET_KEY helps Django protect forms, sessions, and other secure features.
# This is okay for school development, but a real deployment should keep it
# outside the codebase.
SECRET_KEY = 'django-insecure-b#q&_#kq0l^ouzc#!ob8j!o=2um7riooog2fk2m2mwqq=@$-&l'

# DEBUG=True shows detailed error pages while developing.
DEBUG = True

# ALLOWED_HOSTS controls which hostnames are allowed to serve this project.
# An empty list is common during local development.
ALLOWED_HOSTS = []


# INSTALLED_APPS tells Django which built-in features and local apps should be
# loaded when the project starts.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'budget',
]

# MIDDLEWARE is a stack of request/response helpers that run on every page
# load. For example, some handle sessions, authentication, or CSRF protection.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'budget_tracker.urls'

# TEMPLATES tells Django how to find and render HTML templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'budget_tracker.wsgi.application'


# The project uses SQLite, which stores all data in a single file. This keeps
# setup simple for a capstone project.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# These validators help users choose safer passwords during registration.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# These settings control language and time behavior in the project.
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# STATIC_URL is the URL prefix Django uses to serve CSS and other static files.
STATIC_URL = 'static/'

# These settings decide where users are sent for login, after login, and after
# logout.
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Map Django's built-in message levels to Bootstrap alert class names.
# By default Django uses "error" but Bootstrap expects "danger", so this
# override makes flash messages style correctly without any template logic.
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.ERROR: "danger",
}
