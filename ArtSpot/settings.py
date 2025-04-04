from pathlib import Path
import os
from dotenv import load_dotenv  # Use environment variables for sensitive data

# Load environment variables from a .env file (optional but recommended)
load_dotenv()

# Ensure BASE_DIR is properly defined
BASE_DIR = Path(__file__).resolve().parent.parent

RAZORPAY_KEY_ID = "rzp_test_zr1dwQlGjh0OwY"
RAZORPAY_KEY_SECRET = "pMVy1h79sknA8VOYeFpkjwSL"


# Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-zn@^g9!l0mat885@uc14(#+5ld@5ixlvju1s((yp1sb#d_fh0z')  # Use an env variable
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Set as an env variable in production

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Required for `collectstatic`

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Installed Apps
INSTALLED_APPS = [
    'channels',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for serving static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'ArtSpot.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI Application
ASGI_APPLICATION = 'ArtSpot.asgi.application'

# Database Configuration (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'ArtMart'),
        'USER': os.getenv('MYSQL_USER', 'Sayman'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'Sayman@2007'),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),  # Change if using an external database
        'PORT': os.getenv('MYSQL_PORT', '3306'),  # Default MySQL port is 3306
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF Failure View
CSRF_FAILURE_VIEW = 'home.views.custom_csrf_failure_view'
from celery.schedules import crontab



CHANNEL_LAYERS={
    'default':{
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BEAT_SCHEDULE = {
    'delete_idle_lobbies': {
        'task': 'chat.tasks.delete_idle_lobbies',
        'schedule': crontab(minute=0, hour='*/1'),  # Runs every hour
    },
}
