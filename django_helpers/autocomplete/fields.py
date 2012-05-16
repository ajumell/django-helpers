from django import forms
from django_helpers.autocomplete import get_instance

class AutoCompleteField(forms.Field):
    def __init__(self, lookup, *args, **kwargs):
        self.lookup = lookup
        forms.Field.__init__(self, *args, **kwargs)

    def clean(self, value):
        value = forms.Field.clean(self, value)
        try:
            if not value: raise
            instance = get_instance(self.lookup, value)
            # TODO: Send formatted value to widget
            return instance
        except Exception:
            self.widget.current_value = ""
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None
