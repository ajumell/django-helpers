from django.http import HttpResponse
from django.db.models import Q
from simplejson import dumps

def data_table(request, query, fields):
    """
        A view to provide data to jQuery data table plugin. This plugin will
    automatically collect parameters send by the data table plugin and
    returns necessary data as json object. This function can be directly
    called from a urls file.

        The parameters required for this function are request, query and fields.

        Request is the http request send by the plugin. It contains the parameters
    for the data to be responded. This function will automatically collect the
    informations from the request.

        Query is the model query from which the filters has to be applied. It is
    given as query so that custom filters can be applied.

        Fileds are the fileds that has to be send as response in correct order. The
    data send by this function is array and not object so order is very important.

    Example 1
    data_table(request, User.objects.all(), ["username", "first_name", "last_name"])

    Example 2
    url(r'^students/ajax/$', data_table, kwargs={
        "query": Student.objects.all(),
        "fields" : [
            "id",
            "first_name",
            "last_name",
            "college__name",
            "course__name"
        ]
    }, name='students-data-table'),

    """
    GET = request.GET
    gt = GET.get

    no_of_coloums = int(gt('iColumns'))
    echo = gt('sEcho')
    start_pos = int(gt('iDisplayStart'))
    max_items = int(gt('iDisplayLength'))
    search_term = gt('sSearch')
    total_length = query.count()

    # Collect sort fields and apply sorts
    sorts, i = [], 0
    while i < no_of_coloums:
        col = gt("iSortCol_%d" % i)
        if col is not None:
            col = int(col)
            field = fields[col]
            if gt("sSortDir_%d" % i) == "desc":
                field = "-" + field
            sorts.append(field)
        i += 1
    sorts = tuple(sorts)
    query = query.order_by(*sorts)

    if search_term != "":
        # Collect sort fields and apply search
        searches, i = [], 0
        while i < no_of_coloums:
            if gt("bSearchable_%d" % i) == "true":
                field = fields[i] + "__contains"
                kwargs = {field: search_term}
                searches.append(Q(**kwargs))
            i += 1
        searches = tuple(searches)

        # Search
        i, q, search_length = 1, searches[0], len(searches)
        while i < search_length:
            q = q | searches[i]
            i += 1
        query = query.filter(q)

    current_length = query.count()
    query = query[start_pos:start_pos + max_items]
    query = query.values_list(*fields)
    print query, type(query)
    result = {
        "aaData": list(query),
        "sEcho": echo,
        "iTotalRecords": total_length,
        "iTotalDisplayRecords": current_length,
        }
    return HttpResponse(dumps(result))
