from pathlib import Path

# BASE_DIR указывает на корневую папку проекта.
# Через него удобно строить пути к базе данных, media-файлам и статике.
BASE_DIR = Path(__file__).resolve().parent.parent


# Учебный проект запускается локально, поэтому DEBUG включен.
# Для реального сайта SECRET_KEY нужно хранить в .env, а DEBUG выключать.
SECRET_KEY = 'django-insecure-#5-68s+y6sapo=xi+*g^mhgg$0+5ofzw06hbmhda+=vkc0laf+'
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'gallery',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'arthub.urls'

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

WSGI_APPLICATION = 'arthub.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Стандартные валидаторы паролей Django.
# Они не дают пользователю поставить слишком простой пароль.
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


LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# STATIC_URL нужен для css/js проекта.
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_URL и MEDIA_ROOT нужны для картинок, которые пользователи загружают
# через форму публикации работы.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# После входа и выхода пользователь возвращается на главную страницу.
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'