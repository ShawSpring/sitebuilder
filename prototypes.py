#!/usr/bin/env python
import os
import sys

from django.conf import settings, global_settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    default_settings=global_settings,  ##这样才能全局的访问到 settings.xxx
    SECRET_KEY='iplp!i75$8@mcp@$mv%knrnf36ka@rwqx41avhsy=i%2+b=i_g',
    DEBUG=True,
    ROOT_URLCONF='sitebuilder.urls',
    ALLOWED_HOSTS=[],

    # Application definition
    INSTALLED_APPS=[
        # 'django.contrib.admin',
        # 'django.contrib.auth',
        # 'django.contrib.contenttypes',
        # 'django.contrib.sessions',
        # 'django.contrib.messages',
        'sitebuilder',
        'django.contrib.staticfiles',
    ],
    MIDDLEWARE=[
        # 'django.middleware.security.SecurityMiddleware',
        # 'django.contrib.sessions.middleware.SessionMiddleware',
        # 'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',
        # 'django.contrib.auth.middleware.AuthenticationMiddleware',
        # 'django.contrib.messages.middleware.MessageMiddleware',
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            # 'OPTIONS': {
            #     'context_processors': [
            #         'django.template.context_processors.debug',
            #         'django.template.context_processors.request',
            #         'django.contrib.auth.context_processors.auth',
            #         'django.contrib.messages.context_processors.messages',
            #     ],
            # },
        },
    ],
    WSGI_APPLICATION='sitebuilder.wsgi.application',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
    STIE_OUTPUT_DIRECTORY=os.path.join(BASE_DIR, '_build'),  ##生成的静态文件存放路径
    STATIC_URL='/static/',
    STATIC_ROOT=os.path.join(BASE_DIR, '_build', 'static'),

    # # Database
    # # https://docs.djangoproject.com/en/2.1/ref/settings/#databases

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # }

    # # Password validation
    # # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

    # AUTH_PASSWORD_VALIDATORS = [
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    #     },
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #     },
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    #     },
    #     {
    #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    #     },
    # ]
)

if __name__ == '__main__':

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?") from exc
    execute_from_command_line(sys.argv)
