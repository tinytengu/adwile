from os import getenv

from .settings import *

DEBUG = False

SECRET_KEY = getenv("SECRET_KEY")
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "*").split(";")

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "PORT": getenv("DB_PORT"),
    }
}
