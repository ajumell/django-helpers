import time

from django.core.urlresolvers import reverse
from urls import  urlpatterns
from django.db.models import Q
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.simplejson import dumps
from django.template import Template, loader, RequestContext, Context


__author__ = "ajumell"

tables = dict()

class DataTableColoum(object):
    def __init__(self, field, title, searchable, sortable):
        self.field = field
        self.title = title
        self.searchable = searchable
        self.sortable = sortable

    def get_html(self, request, object):
        value = getattr(object, self.field)
        return value


    def need_related(self):
        return self.field.find('__') > -1


class DataTableClientRenderedColoum(DataTableColoum):
    """
    This class is still under planning.
    """
    pass


class DataTableTemplateColoum(DataTableColoum):
    """
    A Data table coloum which will return a rendered
    a template insted of a database field.
    """

    def __init__(self, field, title, searchable, sortable, template,
                 load_template=True, width=None, value_name='value'):
        """
        @param field: The name of the field to be passed to the template.
        @param title: Title of the coloum which will be displayed in the table header.
        @param searchable: jQuery data table option searchable
        @param sortable: jQuery data table option sortable
        @param template: Template to be rendered as the return value.
        This can be either a django.template.Template object or a sting.
        If a string is passed then that template has to be loaded by give
        load_template parameter as True.
        @param load_template: If this parameter is true the template will
        be loaded.
        @param width: Width of the coloum
        @param value_name: name of the variable that has to be passed to the template.
        Its default value is "value"
        """
        DataTableColoum.__init__(self, field, title, searchable, sortable)
        if load_template:
            template = loader.get_template(template)
        self.template = template
        self.width = width
        self.value_name = value_name

    def get_html(self, request, object):
        value = getattr(object, self.field)
        template = self.template

        if not isinstance(template, Template):
            template = Template(self.template)

        context = RequestContext(request, {
            self.value_name: value,
            "width": self.width
        })

        return template.render(context)


class DataTable(object):
    query = None
    url_search_parameters = None

    width = None
    class_name = ""
    name = None
    coloums = []
    table_id = None
    display_length = 10
    ajax_source = ''
    loading_message = 'Please wait while data is loading'

    dom = '<f>t<plir>'
    template = 'data_tables/table.html'

    def __unicode__(self):
        template = loader.get_template(self.template)
        context = Context({
            'display_length': self.display_length,
            'dom': self.dom,
            'ajax_source': reverse(self.table_id),
            'coloums': self.coloums,
            "table_id": self.table_id,
            'loading_message': self.loading_message
        })
        return template.render(context)

    def get_data(self, request, kwargs):
        GET = request.GET
        gt = GET.get

        coloums = self.coloums
        query = self.query.filter()
        extra_params = self.url_search_parameters
        if extra_params is not None:
            filter_dict = {}
            for param_name in extra_params:
                param_value = kwargs.get(param_name, '')
                if param_value != '':
                    filter_dict[param_name] = param_value
            query = query.filter(**filter_dict)

        echo = gt('sEcho')
        start_pos = int(gt('iDisplayStart'))
        max_items = int(gt('iDisplayLength'))
        search_term = gt('sSearch')

        total_length = query.count()
        need_related = False

        fields, sortings, search, i = [], [], None, -1
        for coloum in coloums:
            fields.append(coloum.field)
            i += 1
            need_related = need_related or coloum.need_related()

            if coloum.sortable:
                field = coloum.field
                if gt("sSortDir_%d" % i) == "desc":
                    field = "-" + field
                sortings.append(field)

            if coloum.searchable and search_term != "":
                field = coloum.field + "__contains"
                kwargs = {field: search_term}
                if search is None:
                    search = Q(**kwargs)
                else:
                    search = search | Q(**kwargs)

        fields = tuple(fields)
        if need_related:
            query = query.select_related()
        query = query.order_by(*sortings)
        if search is not None:
            query = query.filter(search)
        query = query.only(*fields)

        current_length = query.count()
        query = query[start_pos:start_pos + max_items]
        datas = []

        for record in query:
            data = []
            for coloum in coloums:
                data.append(coloum.get_html(request, record))
            datas.append(data)

        result = {
            "aaData": datas,
            "sEcho": echo,
            "iTotalRecords": total_length,
            "iTotalDisplayRecords": current_length,
            }
        return HttpResponse(dumps(result))


def get_data(request, name, **kwargs):
    if not tables.has_key(name):
        return HttpResponse()

    table = tables[name]

    results = table.get_data(request, kwargs)
    return results


def create_reg(name):
    return "(?P<%s>.*)/" % name

url_prefix = 'data-table-'

def register(data_table):
    if isinstance(data_table, DataTable):
        raise Exception("DataTable class is required not instance.")

    if not issubclass(data_table, DataTable):
        raise Exception("A Sub class of DataTable is required.")

    if not hasattr(data_table, 'table_id'):
        name = str(time.time())
        name = name.replace('.', '')
    else:
        name = getattr(data_table, 'table_id')

    if not name.startswith(url_prefix):
        name = url_prefix + name

    setattr(data_table, 'table_id', name)
    data_table = data_table()
    tables[name] = data_table
    reg = "%s/" % name
    extra_url_parameters = data_table.url_search_parameters
    if extra_url_parameters is not None:
        for parameter in extra_url_parameters:
            reg += create_reg(parameter)
    reg += "$"

    pattern = url(r"%s" % reg, get_data, name=name, kwargs={
        "name": name
    })

    urlpatterns.append(pattern)
    return data_table
