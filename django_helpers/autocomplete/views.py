import simplejson
from django.db.models import Q
from django.http import HttpResponse
from django_helpers.autocomplete import lookups, format_value

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



def autocomplete_lookup(request, name):
    # If lookup does not exists then return blank array.
    # This is prevent any exceptions at runtime.
    if not lookups.has_key(name):
        return HttpResponse("[]")

    lookup = lookups[name]
    formatter = lookup['display']
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