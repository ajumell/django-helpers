"""
This file provide database settings for clear db
database heroku addon.
Example
-------
from django_helpers.heroku.clear_db_settings import DATABASES
"""
__author__ = 'ajumell'

import database

if database.has_clear_db():
    DATABASES = {
        'default': database.parse_clear_db()
    }
