import simplejson
from urls import  urlpatterns
from django.db.models import Q
from django.conf.urls import url
from django.http import HttpResponse

lookups = dict()
has_initialized = False


def search(lookup, term):
    queryset = lookup['queryset']
    fields = lookup['search-fields']
    query = None

    for field in fields:
        kwargs = {field + "__contains": term}
        if query is None:
            query = Q(**kwargs)
        else:
            query = query | Q(**kwargs)

    return queryset.filter(query)


def autocomplete_lookup(request, lookup):
    # If lookup does not exists then return blank array.
    # This is prevent any exceptions at runtime.
    if not lookups.has_key(lookup):
        return HttpResponse("[]")

    lookup = lookups[lookup]
    formatter = lookup['label_formatter']
    term = request.GET.get("term")
    query = search(lookup, term)
    results = []
    for result in query:
        val = format_value(formatter, result)
        results.append({
            "id": result.id,
            "value": val,
            "label": val
        })
    return HttpResponse(simplejson.dumps(results))


def register(name, queryset, search_fields, label_formatter=None, replace=False):
    """
    @param name: name of the lookup
    @param queryset: A Queryset to which filtering has to be applied
    @param search_fields: A set of fields where searching has to be done
    @param label_formatter: What should be the label of the auto complete field.s
    @param replace: Should replace already existing lookup, default is False
    @return: Returns none
    """
    if replace and lookups.has_key(name):
        raise Exception("Lookup with name %s already exists", name)
    lookups[name] = {
        "queryset": queryset,
        "search-fields": search_fields,
        "label_formatter": label_formatter
    }
    reg = r"lookups/%s/" % name
    pattern = url(reg, autocomplete_lookup, name="lookup-%s" % name, kwargs={
        "lookup": name
    })
    urlpatterns.append(pattern)


def get_queryset(name):
    if not lookups.has_key(name):
        raise Exception("Lookup with name %s does not exists", name)
    return lookups[name]["queryset"]


def get_instance(name, id):
    queryset = get_queryset(name)
    return queryset.get(pk=id)


def get_formatter(lookup, name='label'):
    if not lookups.has_key(lookup):
        raise Exception("Lookup with name %s does not exists", lookup)
    return lookups[lookup]["%s_formatter" % name]


def format_value(formatter, instance):
    if formatter is None:
        return str(instance)

    if hasattr(formatter, "__call__"):
        return formatter(instance)

    string, terms = formatter
    lst = []
    for term in terms:
        lst.append(getattr(instance, term))

    return string % tuple(lst)


def get_value(name, id, formatter='label'):
    obj = get_instance(name, id)
    formatter = get_formatter(name, name=formatter)
    return format_value(formatter, obj)


    #if not has_initialized:
    #    from django.core.urlresolvers import get_resolver, get_urlconf
    #
    #    try:
    #        url_conf = get_resolver(get_urlconf())
    #        print url_conf, url_conf.url_patterns
    #        for x in dir(url_conf):
    #            print x
    #    except Exception, data:
    #        print data
    #
    #    has_initialized = True