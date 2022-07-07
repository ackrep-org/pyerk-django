"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '79+i(fmz-9-aiztl(bd1=qm!c=g)nqnkc!&_j+d^==g+b7bo8!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # for improved testing experience
    'django_nose',

    # to safely render HTML
    'django_bleach',

    # the example app
    'mainapp.apps.MainAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 1

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a', 'br', 'hr',
                       'h1', 'h2', 'h3', 'h4', 'h5', 'ul', 'ol', 'li', 'pre', 'code', 'myscript',
                       'table', 'th', 'tr', 'td', 'thead', 'tbody', 'div', 'span']


def allow_attributes(tag, name, value):
    """
    Use callable to decide which attributes we allow.
    Background: "script" should only be allowed for type="math/tex".

    see also: https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags
    """
    if name in ['href', 'title', 'style']:
        return True
    elif tag in ("span", "div") and name == "class":
        return True
    # elif tag == "script" and name == "type" and value.startswith("math/tex"):
    #     return True
    elif tag == "myscript":
        # Unfortunately, bleach checks every tag separately. To allow `<script type="application/json">
        # script has to be allowed in general. If the type-attributedoes not match the rule then only
        # the attribute is stripped, leaving potential harmful code inside <script>.

        # Thus we introduce a fake tag `myscipt` which will be handled and checked by a custom filter
        return True
    else:
        return False


BLEACH_ALLOWED_ATTRIBUTES = allow_attributes
BLEACH_STRIP_TAGS = False
