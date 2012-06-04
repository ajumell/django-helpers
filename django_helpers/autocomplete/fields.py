from django import forms
from django_helpers.autocomplete import get_instance, get_instances, format_value, get_formatter
from widgets import AutoCompleteWidget

class AutoCompleteField(forms.Field):
    widget = AutoCompleteWidget

    def __init__(self, lookup, *args, **kwargs):
        forms.Field.__init__(self, *args, **kwargs)
        self.lookup = lookup

    def clean(self, value):
        value = forms.Field.clean(self, value)
        try:
            if not value: raise
            instance = get_instance(self.lookup, value)
            formatter = get_formatter(self.lookup)
            self.widget.formatted_value = format_value(formatter, instance)
            return instance
        except Exception:
            self.widget.formatted_value = ""
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None


class SimpleAutoCompleteField(forms.Field):
    widget = AutoCompleteWidget

    def clean(self, value):
        value = forms.Field.clean(self, value)
        self.widget.formatted_value = value
        return value


class ManyToManyAutoCompleteField(forms.Field):
    def __init__(self, lookup, *args, **kwargs):
        self.lookup = lookup
        forms.Field.__init__(self, *args, **kwargs)

    def clean(self, value):
        value = forms.Field.clean(self, value)
        try:
            if not value:
                raise
            value = value.split(',')
            instances = get_instances(self.lookup, value)
            self.widget.instances = instances
            return instances
        except Exception:
            self.widget.formatted_value = ""
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None