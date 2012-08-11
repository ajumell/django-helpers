"""
This file will help to generate settings for a
heroku based django application easily. import *
from this file will automatically generate database
and email settings for heroku.


Database Settings
=================
Database settings will be parsed from the
herok config files. There are many solutions
for databases in heroku. They will be used as
given below.

Order
-----
1. Clear DB Database
2. Heroku Shared PG Database

Email Settings
==============
Currently send grid settings will be generated
automatically.

"""
__author__ = 'ajumell'
from send_grid_settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT
from database import has_clear_db


if has_clear_db():
    from clear_db_settings import DATABASES
else:
    pass

__all__ = (
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    DATABASES
    )
