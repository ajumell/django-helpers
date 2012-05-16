from django import forms
from django_helpers.autocomplete import get_instance

class AutoCompleteField(forms.CharField):
    def __init__(self, lookup, *args, **kwargs):
        self.lookup = lookup
        forms.CharField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """
        This function is used to set value to the
        widget to set value to hidden field.
        """
        val = forms.CharField.to_python(self, value)
        try:
            val = get_instance(self.lookup, val)
            self.widget.current_value = value
            return val
        except Exception:
            self.widget.current_value = ""
            return ""