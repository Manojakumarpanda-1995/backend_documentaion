"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
#For log the errors
from logging.handlers import RotatingFileHandler

info=logging.handlers.RotatingFileHandler(
    filename=os.path.join(BASE_DIR, "logs/djangoLog.log"),
    mode='a',
    backupCount=10,
    maxBytes=50*1024*1024,
    encoding=None,
    delay=0
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[info]
)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')pkmt+86uec16u%r-!-naw0oxoxtm)z+1b=6qee7=s7^p-!fm9'
# 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']#,"13.126.141.50"]
SERVERURL="http://"+ALLOWED_HOSTS[0]
BACKEND_URL="http://{}:96".format(ALLOWED_HOSTS[0])
APPEND_SLASH=False
# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'corsheaders',
    'rest_framework',
    'usermanagement',#.apps.usermanagementConfig',
    'organization',
    'project',
    "rest_framework_swagger",
    "drf_yasg",
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'corsheaders.middleware.CorsPostCsrfMiddleware',
    'backend.UserVerification.CheckToken',
]

ROOT_URLCONF = 'backend.urls'
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True

ACCESS_CONTROL_ALLOW_ORIGIN = "*"
ACCESS_CONTROL_EXPOSE_HEADERS = "X-Requested-With, Content-Type"
# ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
ACCESS_CONTROL_ALLOW_HEADERS = "X-Requested-With, Content-Type"
ACCESS_CONTROL_MAX_AGE = "1000"

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
            'libraries' : {
                'staticfiles': 'django.templatetags.static', 
            }
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'OPTIONS': {
        #     "database": "backend",
        #     "user": "root",
        #     # "host": "0.0.0.0",
        #     # "port": 3306,
        #     # "host": "mysql1",
        #     "host": "backend_mysql",
        #     "password": "newP@ssw0rd@1234567@"
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# REST_FRAMEWORK={ 'DEFAULT_SCHEMA_CLASS': ['rest_framework.schemas.coreapi.AutoSchema',
                                        #   "rest_framework.schemas.openapi.AutoSchema"],
REST_FRAMEWORK={ 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    "DEFAULT_RENDERER_CLASSES":("rest_framework.renderers.JSONRenderer",),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
   
    # 'SECURITY_DEFINITIONS': {
    #     "ApiKeyAuth":{
    #         type: "apiKey",
    #         "in": "header"
    #     }}
}
# from rest_framework.parsers.
SWAGGER_SETTINGS = {
    # For using django admin panel for authentication
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': 'usermanagement:loginapi',
    'JSON_EDITOR': True,
    "SHOW_REQUEST_HEADERS":True,
    'enabled_methods': [
        # 'get',
        'post',
        # 'put',
        # 'patch',
        # 'delete'
    ],
    # 'LOGOUT_URL': 'rest_framework:logout',

    # # For using other mechanisms for authentication ('basic' uses username/password)
    'SECURITY_DEFINITIONS': {
        "ApiKeyAuth":{
            "type": "apiKey",
            "in": "header",
            "name":"Authorization"
    #     # 'basic': {
    #     #     'type': 'basic',
        },
    },

    # For validating your swagger schema(setting None to not validate)
    # 'VALIDATOR_URL': None,
}

LOGIN_URL = 'usermanagement:loginapi'
# LOGOUT_URL = 'usermanagement:logout'
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,"static")]
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static')

MEDIA_URL = '/media_files/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media_files')

EMAIL_IP = "smtp.gmail.com"
EMAIL = "noreply@momenttext.com"
EMAIL_PASSWORD = "ydg8K(v!XM-9Zuaw"
EMAIL_USERNAME = "Backend Alert"
# EMAIL_IP = "mail.privateemail.com"
EMAIL_USE_SSL = True
# EMAIL_PORT=25s
ENCRYPTED_ENCRYPTION_KEY = b'ScXL9dqxFMSoIUa4J+2xwjPzyLyQefzwKWDyM38pV7myDLfVz96SOpCmI1cDaI6NVEmY2ZRdgC83HJQM9B2mNulr1rWdRL81v2lwu1ssZ4NF/ytW6yi5hEpqVhX2yzCkwwbKfabIsqPpiNEM8JUI8A=='
CRON_JOB_TIME_LIST = [0, 1, 0, 0] # days, hous, minutes, seconds

DOWNLOAD_URL_EXPIRY=60 #seconds
OTP_EXPIRY_DURATION = 15 #minutes
LOCKOUT_COUNT_RESET_DURATION = 10 #minutes
INCORRECT_PASSWORD_COUNT_THRESHOLD = 5 #minutes #If wrong password is entered x number of times within these minutes then lockout will be initiated
INCORRECT_PASSWORD_COUNT_MAX_ATTEMPTS = 5 #Should be grater than 1 # If these many number of wrong password attempts are made in x minutes then lockout will be intiated

LOCKOUT_PASSWORD_RESET_INIT_DURATION = 10 #minutes
PASSWORD_RESET_INIT_COUNT_THRESHOLD = 5 #minutes #If wrong password is entered x number of times within these minutes then lockout will be initiated
PASSWORD_RESET_INIT_COUNT_MAX_ATTEMPTS = 5 #Should be grater than 1 # If these many number of wrong password attempts are made in x minutes then lockout will be intiated
FILE_DOWNLOAD_URL_EXPIRY = 60 #secs

VERIFICATION_LINK_EXPIRY_DURATION = 30 #mins

CELERY_BROKER_URL = 'amqp://backend:r@bb@tP@ssw0rd@1233456@@backend_rabbit'

VERIFICATION_LINK_EXPIRY_DURATION = 30 #mins

FRONT_END_URL = "http://localhost"
STORAGE_THRESHOLD = 50 #MB


TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')

from pymongo import MongoClient
# import urllib.parse

# username = urllib.parse.quote_plus('backend')
# password = urllib.parse.quote_plus('sd@f@sjdkfe323tfd@')
# client = MongoClient('mongodb://%s:%s@backend_mongodb/' % (username, password))
# client = MongoClient('mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb')
client = MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
# mongo_uri = "mongodb://backend:" + urllib.quote("sd@f@sjdkfe323tfd@") + "@backend_mongodb/"
# client = MongoClient("mongodb://backend:sd@f@sjdkfe323tfd@@backend_mongodb")
# client = MongoClient(mongo_uri)

db = client.admin
ACTIVITY_LOGS_DB = db.activity_logs
ERROR_LOGS_DB = db.error_logs

