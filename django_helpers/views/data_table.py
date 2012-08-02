from django.http import HttpResponse
from django.db.models import Q
from django.utils.simplejson import dumps

def data_table(request, query, fields, extra_params=None, **kwargs):
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
    }, name='students-data-table')


    @param request: A HttpRequest object
    @type request: django.http.HttpRequest

    @param fields: A array of fields to be returned as response
    @type fields: list

    @param query: Query for which filters has to be applied.
    @type query: django.db.models.query.QuerySet

    """
    # TODO: Latest docs of url params


    # Perform extra filtering from named url parameters
    # send from url dispatcher.
    if extra_params is not None:
        filter_dict = {}
        for param_name in extra_params:
            param_value = kwargs.get(param_name, '')
            if param_value != '':
                filter_dict[param_name] = param_value
        query = query.filter(**filter_dict)

    GET = request.GET
    gt = GET.get

    no_of_coloums = int(gt('iColumns'))
    echo = gt('sEcho')
    start_pos = int(gt('iDisplayStart'))
    max_items = int(gt('iDisplayLength'))
    search_term = gt('sSearch')
    total_length = query.count()
    need_related = False

    # Collect sort fields and apply sorts
    sorts, i = [], 0
    while i < no_of_coloums:
        # Detect if select_related is needed.
        try:
            if not need_related and fields[i].find('__') > -1:
                need_related = True
        except Exception:
            pass

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

    # Select related fields if necessary
    if need_related:
        query = query.select_related()

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
    result = {
        "aaData": list(query),
        "sEcho": echo,
        "iTotalRecords": total_length,
        "iTotalDisplayRecords": current_length,
        }
    return HttpResponse(dumps(result))
