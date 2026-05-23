import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-krishimitra-2024-farmers-platform-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'core',
    'crops',
    'market',
    'chat',
    'schemes',
    'farmmanager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LanguageMiddleware',  # ADD THIS LINE
]

ROOT_URLCONF = 'krishimitra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.language_processor',
                'core.context_processors.language_processor', 
            ],
        },
    },
]

WSGI_APPLICATION = 'krishimitra.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'core.Farmer'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

WEATHER_API_KEY = 'dummy-key-for-now'  # Replace with real OpenWeatherMap key

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Add to bottom of settings.py
WEATHER_API_KEY = '267d8aad3a1eaf20185c4451e603e632'  
# Replace with your OpenWeatherMap API key
# PWA Settings - Add at the very bottom of settings.py
PWA_APP_NAME = 'KrishiMitra'
PWA_APP_DESCRIPTION = "AI-Powered Smart Farming Platform for Indian Farmers"
PWA_APP_THEME_COLOR = '#2e7d32'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_STATUS_BAR_COLOR = '#2e7d32'
PWA_APP_ICONS = [
    {
        'src': '/static/icons/icon-72x72.png',
        'sizes': '72x72',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-96x96.png',
        'sizes': '96x96',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-128x128.png',
        'sizes': '128x128',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-144x144.png',
        'sizes': '144x144',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-152x152.png',
        'sizes': '152x152',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-192x192.png',
        'sizes': '192x192',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-384x384.png',
        'sizes': '384x384',
        'type': 'image/png',
    },
    {
        'src': '/static/icons/icon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png',
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/icons/icon-512x512.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)',
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en'
PWA_APP_OFFLINE_URL = '/offline/'
# Add to settings.py
# SMS Configuration (TextLocal - Free for testing)
TEXTLOCAL_API_KEY = "YOUR_TEXTLOCAL_API_KEY"  # Get from https://textlocal.in
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_SID"  # If using Twilio
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_TOKEN"  # If using Twilio
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio number

# Add at the bottom of settings.py

# Multi-language settings
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('hi', _('Hindi')),
    ('kn', _('Kannada')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_L10N = True
# Add at the very bottom of settings.py
import os

# Allow Koyeb domain
ALLOWED_HOSTS = ['*', '.koyeb.app']

# Use SQLite with writable location on Koyeb
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',  # Koyeb allows writing to /tmp
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/media'