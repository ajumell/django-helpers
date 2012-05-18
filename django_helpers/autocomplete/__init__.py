lookups = dict()
has_initialized = False

def register(name, queryset, search_fields, display=None, replace=False):
    """
    @param name: name of the lookup
    @param queryset: A Queryset to which filtering has to be applied
    @param search_fields: A set of fields where searching has to be done
    @param display: What should be the label of the auto complete field.s
    @param replace: Should replace already existing lookup, default is False
    @return: Returns none
    """
    if replace and lookups.has_key(name):
        raise Exception("Lookup with name %s already exists", name)
    lookups[name] = {
        "queryset": queryset,
        "search-fields": search_fields,
        "display": display
    }


def get_queryset(name):
    if not lookups.has_key(name):
        raise Exception("Lookup with name %s does not exists", name)
    return lookups[name]["queryset"]


def get_instance(name, id):
    queryset = get_queryset(name)
    return queryset.get(pk=id)


def get_formatter(name):
    if not lookups.has_key(name):
        raise Exception("Lookup with name %s does not exists", name)
    return lookups[name]["display"]


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


def get_value(name, id):
    obj = get_instance(name, id)
    formatter = get_formatter(name)
    return format_value(formatter, obj)


if not has_initialized:
    from django.conf import settings

    print settings.ROOT_URLCONF
    has_initialized = True