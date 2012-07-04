from django.forms import fields
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

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


class MaskedInput(Widget, fields.TextInput):
    def __init__(self, mask, placeholder="_", *args, **kwargs):
        fields.TextInput.__init__(self, *args, **kwargs)
        self.mask = mask
        self.placeholder = placeholder

    def render_js(self):
        return render_to_string('xs-forms/js/mask-input.js', {
            "mask": self.mask,
            "id": self.html_id,
            "placeholder": self.placeholder
        })


class SpinnerInput(Widget, fields.TextInput):
    def __init__(self, min_value=None, max_value=None, places=None, prefix="",
                 step=1, largeStep=10, *args, **kwargs):
        # TODO: Add more options from plugin
        fields.TextInput.__init__(self, *args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.places = places
        self.prefix = prefix
        self.step = step
        self.largeStep = largeStep

    def render(self, name, value, attrs=None):
        self.value = value
        return fields.TextInput.render(self, name, self.prefix + str(value), attrs)

    def render_js(self):
        return render_to_string('xs-forms/js/mask-input.js', {
            "min": self.min_value,
            "max": self.max_value,
            "prefix": self.prefix,
            "places": self.places,
            "value": self.value,
            "step": self.step,
            "largeStep": self.largeStep,
            "id": self.html_id
        })


class RatingWidget(Widget, fields.TextInput):
    def __init__(self, number=5, cancel=False, half=False, size=16, *args, **kwargs):
        # TODO: Add more options from plugin
        fields.TextInput.__init__(self, *args, **kwargs)
        self.number = number
        self.cancel = cancel
        self.half = half
        self.size = size

    def render(self, name, value, attrs=None):
        if value is None:
            value = 0

        self.input_type = "hidden"
        hidden = fields.TextInput.render(self, name, value)
        final_attrs = self.build_attrs(attrs)
        self.value = value
        self.name = name
        return mark_safe(u'<div%s></div>' % flatatt(final_attrs)) + hidden

    def render_js(self):
        return render_to_string('xs-forms/js/raty.js', {
            "number": self.number,
            "half": self.half,
            "size": self.size,
            "name": self.name,
            "id": self.html_id,
            "score": self.value,
            "cancel": self.cancel
        })
