import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env', override=False)


def env_bool(name, default=False):
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {'1', 'true', 'yes', 'on'}


def env_csv(name, default=''):
    return [item.strip() for item in os.environ.get(name, default).split(',') if item.strip()]


SECRET_KEY = (
    os.environ.get('SECRET_KEY')
    or os.environ.get('DJANGO_SECRET_KEY')
    or ''
).strip().strip("'\"")
DEBUG = env_bool('DEBUG', default=False)

if not SECRET_KEY:
    raise ImproperlyConfigured(
        'SECRET_KEY is missing. Set it in .env for local work, or in the PaaS environment for production.'
    )

ALLOWED_HOSTS = env_csv('ALLOWED_HOSTS', '127.0.0.1,localhost,.liara.run,.liara.ir')
CSRF_TRUSTED_ORIGINS = [
    origin for origin in env_csv(
        'CSRF_TRUSTED_ORIGINS',
        'https://*.liara.run,https://*.liara.ir',
    )
    if origin.startswith(('http://', 'https://'))
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website.apps.WebsiteConfig',
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
]

ROOT_URLCONF = 'config.urls'

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
                'website.context_processors.site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


def postgres_from_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.split('+')[0]
    if scheme not in {'postgres', 'postgresql'}:
        raise ImproperlyConfigured('DATABASE_URL must be a PostgreSQL URL.')
    config = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': unquote(parsed.path.lstrip('/')),
        'USER': unquote(parsed.username or ''),
        'PASSWORD': unquote(parsed.password or ''),
        'HOST': parsed.hostname or '',
        'PORT': str(parsed.port or 5432),
        'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '60')),
    }
    sslmode = parse_qs(parsed.query).get('sslmode', [''])[0]
    if sslmode:
        config['OPTIONS'] = {'sslmode': sslmode}
    return config


def sqlite_path():
    configured = os.environ.get('SQLITE_PATH', '').strip()
    if configured:
        return Path(configured)
    return BASE_DIR / 'DB' / 'db.sqlite3'


database_url = os.environ.get('DATABASE_URL', '').strip()
postgres_host = os.environ.get('POSTGRESQL_DB_HOST', '').strip()

if database_url:
    DATABASES = {'default': postgres_from_url(database_url)}
elif postgres_host:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRESQL_DB_NAME', 'postgres'),
            'USER': os.environ.get('POSTGRESQL_DB_USER', ''),
            'PASSWORD': os.environ.get('POSTGRESQL_DB_PASS', ''),
            'HOST': postgres_host,
            'PORT': os.environ.get('POSTGRESQL_DB_PORT', '5432'),
            'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '60')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_path(),
        }
    }


AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
