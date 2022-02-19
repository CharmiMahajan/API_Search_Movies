# !/usr/bin/env python

import os
from dotenv import load_dotenv
from decouple import config


load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings
    applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'Development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='S#perS3crEt_007')

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='mysql'),
        config('DB_USERNAME', default='Admin'),
        config('DB_PASS', default='Admin%40123'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=3306),
        config('DEV_DB_NAME', default='tms_dev')
    )

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.db')


class ProductionConfig(Config):
    FLASK_ENV = 'Production'

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='mysql'),
        config('DB_USERNAME', default='Admin'),
        config('DB_PASS', default='Admin%40123'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=3306),
        config('PROD_DB_NAME', default='tms_prod')
    )

    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


# Load all possible configurations
config_dict = {
    'Development': DevelopmentConfig,
    'Production': ProductionConfig,
    'Testing': TestingConfig
}
