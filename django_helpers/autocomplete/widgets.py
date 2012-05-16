from django.core.urlresolvers import reverse
from django.forms import fields
from django.template.loader import render_to_string
from django_helpers.forms.widgets import Widget
from django_helpers.autocomplete import get_value

class AutoCompleteWidget(Widget, fields.TextInput):
    current_value = None

    def __init__(self, attrs=None, delay=0, min_length=1, lookup=None):
        fields.TextInput.__init__(self, attrs)

        self.min_length = min_length
        self.delay = delay
        self.lookup = lookup

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""

        self.input_type = "hidden"
        hidden = fields.TextInput.render(self, name, value)
        self.name = name

        try:
            obj = get_value(self.lookup, value)
            try:
                obj = obj.autocomplete()
            except Exception:
                obj = str(obj)
        except  Exception:
            obj = ""

        self.input_type = "text"
        display = fields.TextInput.render(self, name + "_display", obj, attrs)
        return display + hidden

    def render_js(self):
        source = reverse("auto-complete-lookup", kwargs={
            "name": self.lookup
        })

        op = render_to_string('xs-forms/js/auto-complete.js', {
            "min_length": self.min_length,
            "delay": self.delay,
            "source": source,
            "id": self.html_id,
            "name": self.name
        })
        return op