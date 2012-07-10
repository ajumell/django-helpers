from django.core.mail.message import EmailMultiAlternatives, EmailMessage
from django.conf import settings
from mimetypes import guess_type
from os.path import basename
from django.utils.html import strip_tags
from django_helpers.views.helpers import render_to_string

__author__ = 'ajumell'

from_email = "dummy"
if hasattr(settings, "EMAIL_HOST_USER"):
    from_email = settings.EMAIL_HOST_USER

def attach(mail, attachments):
    if attachments is not None:
        for attachment in attachments:
            file_pointer = open(attachment)
            contents = file_pointer.read()
            file_pointer.close()
            file_name = basename(attachment)
            file_type = None
            file_types = guess_type(file_name)
            for type in file_types:
                if type is not None:
                    file_type = type
                    break
            print file_name, file_type
            mail.attach(file_name, contents, file_type)


def send_text_mail(subject, contents, to, attachments=None):
    mail = EmailMessage(subject, contents, from_email, [to])
    attach(mail, attachments)
    mail.send()


def send_html_email(subject, text_content, html_content, to, attachments=None):
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
    mail.attach_alternative(html_content, "text/html")
    attach(mail, attachments)
    mail.send()


def render_template(subject, template, to, attachments=None, template_dict=None, request=None):
    html = render_to_string(template, template_dict, request)
    text = strip_tags(html)
    send_html_email(subject, text, html, to, attachments)