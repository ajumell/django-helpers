import simplejson
from django.db.models import Q
from django.http import HttpResponse
from django_helpers.autocomplete import lookups

def search(name, term):
    # If lookup does not exists then return blank array.
    # This is prevent any exceptions at runtime.
    if not lookups.has_key(name):
        return []

    lookup = lookups[name]
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


def lookup(request, name):
    term = request.GET.get("term")
    query = search(name, term)
    results = []
    for result in query:
        results.append({
            "id": result.id,
            "value": result.name,
            "label": result.name
        })
    return HttpResponse(simplejson.dumps(results))