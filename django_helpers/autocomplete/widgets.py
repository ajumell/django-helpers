from django.core.urlresolvers import reverse
from django.forms import fields
from django.template.loader import render_to_string
from django_helpers.forms.widgets import Widget

class AutoCompleteWidget(Widget, fields.TextInput):
    formatted_value = None

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
        self.input_type = "text"
        display = fields.TextInput.render(self, name + "_display", self.formatted_value, attrs)
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