__author__ = 'ajumell'

from django.core.urlresolvers import resolve

def menu(request):
    current_url = resolve(request.get_full_path()).url_name

