from django.utils.simplejson import dumps
import time
from urls import  urlpatterns
from django.db.models import Q
from django.conf.urls import url, import_module
from django.conf import settings
from django.http import HttpResponse


root_urls = import_module(settings.ROOT_URLCONF)
lookups = dict()

class AutoComplete(object):
    query_set = None
    search_fields = []
    url_search_parameters = None
    requires_auth = False

    __name__ = "__undefined__"

    def search_term(self, term):
        query = None
        queryset = self.query_set
        fields = self.search_fields
        for field in fields:
            kwargs = {field + "__contains": term}
            if query is None:
                query = Q(**kwargs)
            else:
                query = query | Q(**kwargs)
        return queryset.filter(query)

    def search_url_paramters(self, query, url_params):
        url_search_parameters = self.url_search_parameters
        if url_search_parameters is not None:
            for parameter in url_search_parameters:
                args_dict = {parameter: url_params.get(parameter, '')}
                query = query.filter(**args_dict)
        return query

    def search(self, term, url_params):
        query = self.search_term(term)
        return self.search_url_paramters(query, url_params)

    def get_instances(self, ids):
        return self.query_set.filter(pk__in=ids)

    def get_instance(self, id):
        return self.query_set.get(pk=id)

    def simple_format(self, instance, string, *fields):
        lst = []
        for term in fields:
            lst.append(getattr(instance, term))
        return string % tuple(lst)

    def format_value(self, instance):
        return str(instance)

    def get_search_term(self, request):
        term = request.GET.get("term")
        if term is None:
            term = request.GET.get("q")
        return term

    def get_results(self, request, params):
        term = self.get_search_term(request)
        query = self.search(term, params)
        results = []
        for result in query:
            val = self.format_value(result)
            # Renamed value for adding support for
            # jQuery toekn field. The value can be
            # controlled for jQuery auto complete.
            results.append({
                "id": result.id,
                "label": val,
                })
        return results


def autocomplete_lookup(request, lookup, **kwargs):
    # If lookup does not exists then return blank array.
    # This is prevent any exceptions at runtime.
    if not lookups.has_key(lookup):
        return HttpResponse("[]")

    auto_complete = lookups[lookup]()

    results = auto_complete.get_results(request, kwargs)
    return HttpResponse(dumps(results))


def create_reg(name):
    return "(?P<%s>.*)/" % name

url_prefix = 'auto-complete-'

def register(autocomplete_class):
    if isinstance(autocomplete_class, AutoComplete):
        raise Exception("AutoComplete class is required not instance.")

    if not hasattr(autocomplete_class, 'name'):
        name = str(time.time())
        name = name.replace('.', '')
    else:
        name = getattr(autocomplete_class, 'name')

    if not name.startswith(url_prefix):
        name = url_prefix + name
    setattr(autocomplete_class, 'name', name)

    lookups[name] = autocomplete_class
    reg = "%s/" % name
    extra_url_parameters = autocomplete_class.url_search_parameters
    if extra_url_parameters is not None:
        for parameter in extra_url_parameters:
            reg += create_reg(parameter)
    reg += "$"

    pattern = url(r"%s" % reg, autocomplete_lookup, name=name, kwargs={
        "lookup": name
    })
    urlpatterns.append(pattern)
