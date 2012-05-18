from django import forms
from django_helpers.autocomplete import get_instance, format_value, get_formatter

class AutoCompleteField(forms.Field):
    def __init__(self, lookup, *args, **kwargs):
        self.lookup = lookup
        forms.Field.__init__(self, *args, **kwargs)

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
