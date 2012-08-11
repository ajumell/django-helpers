"""
    This file has the settings for sending sms from send grid addon
    of heroku. just import * from this file and start sending mails.
"""
from os import environ
if environ.has_key('SENDGRID_USERNAME') and environ.has_key('SENDGRID_PASSWORD'):
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = environ.get('SENDGRID_USERNAME')
    EMAIL_HOST_PASSWORD = environ.get('SENDGRID_PASSWORD')