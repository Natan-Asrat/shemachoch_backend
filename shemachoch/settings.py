from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import os, datetime
# import dotenv
# dotenv.read_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

AUTH_USER_MODEL = 'core.Employee'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'true' if os.environ.get('DEBUG') else True
FIREBASE_ACCOUNT_TYPE = os.environ.get('FIREBASE_ACCOUNT_TYPE')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY_ID = os.environ.get('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_PRIVATE_KEY = os.environ.get('FIREBASE_PRIVATE_KEY')
FIREBASE_CLIENT_EMAIL = os.environ.get('FIREBASE_CLIENT_EMAIL')
FIREBASE_CLIENT_ID = os.environ.get('FIREBASE_CLIENT_ID')
FIREBASE_AUTH_URI = os.environ.get('FIREBASE_AUTH_URI')
FIREBASE_TOKEN_URI = os.environ.get('FIREBASE_TOKEN_URI')
FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL')
FIREBASE_CLIENT_X509_CERT_URL = os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
EXPIRES_IN = int(os.environ.get('EXPIRES_IN'))
EXPIRES_MONTHS_OR_YEARS_LATER = os.environ.get('EXPIRES_MONTHS_OR_YEARS_LATER')
if(EXPIRES_MONTHS_OR_YEARS_LATER == 'Y'):
    EXPIRES_IN = EXPIRES_IN*365
if(EXPIRES_MONTHS_OR_YEARS_LATER == 'M'):
    EXPIRES_IN = EXPIRES_IN*30

SUGAR_UNIT = os.environ.get("SUGAR_UNIT")
OIL_UNIT = os.environ.get("OIL_UNIT")


CYCLE_START_DATE = os.environ.get('CYCLE_START_DATE')
CYCLE_START_DATE = datetime.datetime.strptime(CYCLE_START_DATE, "%Y-%m-%d").date()
daysPassed = (datetime.date.today() - CYCLE_START_DATE).days
GROUP_1_DURATION = int(os.environ.get('GROUP_1_DURATION'))
GROUP_2_DURATION = int(os.environ.get('GROUP_2_DURATION'))
GROUP_3_DURATION = int(os.environ.get('GROUP_3_DURATION'))
GROUP_4_DURATION = int(os.environ.get('GROUP_4_DURATION'))
GROUPS_DURATIONS = [
    GROUP_1_DURATION,
    GROUP_2_DURATION,
    GROUP_3_DURATION,
    GROUP_4_DURATION
]
CYCLE_DURATION = 0
for duration in GROUPS_DURATIONS:
    CYCLE_DURATION+=duration
LAST_CYCLE_COUNT = int(os.environ.get('LAST_CYCLE_COUNT'))
CYCLE_COUNT_NOW = LAST_CYCLE_COUNT + 1 + daysPassed // CYCLE_DURATION

ALLOWED_HOSTS = ['.onrender.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'corsheaders',
    'rest_framework',
    'debug_toolbar'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'shemachoch.urls'

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

WSGI_APPLICATION = 'shemachoch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

import dj_database_url
DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_LINK'))

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.authentication.FirebaseAuthentication',
        'django.contrib.auth.backends.ModelBackend',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]
}