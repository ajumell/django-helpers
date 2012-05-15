from django import forms

class AutoCompleteField(forms.ModelChoiceField):
    def to_python(self, value):
        """
        This function is used to set value to the
        widget to set value to hidden field.
        """
        val = forms.ModelChoiceField.to_python(self, value)
        self.widget.current_value = value
        return val