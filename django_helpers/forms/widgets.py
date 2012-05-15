from django.core.urlresolvers import reverse
from django.forms import fields
from django.template.loader import render_to_string

class Widget:
    attrs = None
    has_js = True

    def build_attrs(self, extra_attrs=None, **kwargs):
        """
        This function has to be updated when the corresponding
        django function changes.
        """
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)

        if attrs.has_key("id"):
            self.html_id = attrs["id"]
        return attrs


class DateInput(Widget, fields.DateInput):
    def __init__(self, attrs=None, format=None, max_date=None,
                 min_date=None, change_year=None, change_month=None):
        fields.DateInput.__init__(self, attrs, format)

        self.min_date = min_date
        self.max_date = max_date
        self.change_month = change_month
        self.change_year = change_year

    def render_js(self):
        return render_to_string('xs-forms/js/date-field.js', {
            "max_date": self.max_date,
            "min_date": self.min_date,
            "change_year": self.change_year,
            "change_month": self.change_month,
            "id": self.html_id,
            "date_format": self.format
        })


class AutoCompleteWidget(Widget, fields.TextInput):
    current_value = None

    def __init__(self, attrs=None, delay=None, min_length=None, source=None, queryset=None):
        fields.TextInput.__init__(self, attrs)

        self.min_length = min_length
        self.delay = delay
        self.source = source
        self.queryset = queryset

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""

        self.input_type = "hidden"
        hidden = fields.TextInput.render(self, name, value)
        self.name = name

        if value is not "":
            obj = self.queryset.get(id=value)
            try:
                obj = obj.autocomplete()
            except Exception:
                obj = str(obj)
        else:
            obj = ""

        self.input_type = "text"
        display = fields.TextInput.render(self, name + "_display", obj, attrs)
        return display + hidden

    def render_js(self):
        source = reverse(self.source)
        op = render_to_string('xs-forms/js/auto-complete.js', {
            "min_length": self.min_length,
            "delay": self.delay,
            "source": source,
            "id": self.html_id,
            "name": self.name
        })
        return op