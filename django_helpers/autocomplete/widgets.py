from django.core.urlresolvers import reverse
from django.forms import fields
from django.template.loader import render_to_string
from django_helpers.autocomplete import  get_formatter, format_value, get_instance, get_instances
from django_helpers.forms.widgets import Widget

class AutoCompleteWidget(Widget, fields.TextInput):
    formatted_value = None
    template = 'xs-forms/js/auto-complete.js'

    def __init__(self, attrs=None, delay=0, min_length=1, lookup=None):
        fields.TextInput.__init__(self, attrs)

        self.min_length = min_length
        self.delay = delay
        self.lookup = lookup

    def get_formatted_value(self, value):
        if not value:
            return ""

        # Edit mode in model field.
        if self.formatted_value is None:
            instance = get_instance(self.lookup, value)
            formatter = get_formatter(self.lookup)
            val = format_value(formatter, instance)
        else:
            val = self.formatted_value
        self.formatted_value = val
        self.value = value
        return val

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        self.value = value

        self.input_type = "hidden"
        hidden = fields.TextInput.render(self, name, value)
        self.name = name
        self.input_type = "text"
        value = self.get_formatted_value(value)
        display = fields.TextInput.render(self, name + "_display", value, attrs)
        return display + hidden

    def id_for_label(self, id_):
        return '%s_display' % id_

    def render_js(self):
        source = reverse("lookup-%s" % self.lookup)
        value = self.value or ""
        op = render_to_string(self.template, {
            "min_length": self.min_length,
            "delay": self.delay,
            "source": source,
            "id": self.html_id,
            "name": self.name,
            "label": self.formatted_value,
            "value": value
        })
        return op


class SimpleAutoCompleteWidget(AutoCompleteWidget):
    template = 'xs-forms/js/auto-complete-simple.js'

    def get_formatted_value(self, value):
        return value


class TokenInputWidget(Widget, fields.TextInput):
    instances = None

    def __init__(self, lookup, hint_text=None, no_result_text=None, searching_text=None, delay=0,
                 min_chars=1, limit=None, prevent_duplicates=True, theme=None, *args, **kwargs):
        fields.TextInput.__init__(self, *args, **kwargs)
        self.lookup = lookup
        self.hint_text = hint_text
        self.no_result_text = no_result_text
        self.searching_text = searching_text
        self.delay = delay
        self.min_chars = min_chars
        self.limit = limit
        self.prevent_duplicates = prevent_duplicates
        self.theme = theme

    def render(self, name, value, attrs=None):
        self.name = name
        if self.instances is None:
            self.instances = get_instances(self.lookup, value)
        return fields.TextInput.render(self, name, "", attrs)


    def render_js(self):
        source = reverse("lookup-%s" % self.lookup)
        instances = self.instances
        formatter = get_formatter(self.lookup)
        formatted_values = []
        if instances:
            for instance in instances:
                formatted_values.append({
                    "name": format_value(formatter, instance),
                    "id": instance.pk
                })

        op = render_to_string('xs-forms/js/token-input.js', {
            "hint_text": self.hint_text,
            "no_result_text": self.no_result_text,
            "searching_text": self.searching_text,
            "delay": self.delay,
            "min_chars": self.min_chars,
            "limit": self.limit,
            "theme": self.theme,
            "prevent_duplicates": self.prevent_duplicates,
            "source": source,
            "id": self.html_id,
            "name": self.name,
            "values": formatted_values
        })
        return op