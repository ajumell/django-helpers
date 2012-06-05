from django import forms
from django.utils.translation import ugettext_lazy as _
from widgets import DateInput
from django_helpers.autocomplete import fields
from django_helpers.autocomplete.widgets import AutoCompleteWidget, SimpleAutoCompleteWidget

def set_property(field, args, name, target):
    if name in args:
        val = args[name]
        setattr(field, target, val)


def update_class_name(field, class_name):
    if class_name is not None:
        attr = field.widget.attrs
        old_class = attr.get('class', '')
        attr['class'] = class_name if old_class == '' else "%s %s" % (old_class, class_name)


def factory(field, help_text=None, required=None,
            label=None, error_messages=None, initial_value=None,
            class_name=None, container_class=None, label_class=None,
            class_names=None, extra_options=None, widget_options=None
):
    widget = field.widget

    if label is not None:
        field.label = _(label)

    if container_class is not None:
        field.container_class = container_class

    if label_class is not None:
        field.label_class = label_class

    if help_text is not None:
        field.help_text = help_text

    if class_name is not None:
        update_class_name(field, class_name)

    if error_messages is not None:
        field.error_messages.update(error_messages)

    if required is not None:
        field.required = required

    if initial_value is not None:
        field.initial = initial_value

    if extra_options is not None:
        #print extra_options.values()
        for key, value in extra_options.items():
            setattr(field, key, value)

    if class_names is not None:
        for class_name in class_names:
            update_class_name(field, class_name)

    if widget_options is not None:
        for key, value in widget_options.items():
            setattr(widget, key, value)

    field.localize = False
    field.required = required

    return field


def CharField(label=None, max_length=None, min_length=None,
              required=None, class_names=None, class_name=None):
    return factory(
        forms.CharField(),
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names,
        extra_options={
            "max_length": max_length,
            "min_length": min_length,
            }
    )


def PasswordField(label=None, max_length=None, min_length=None,
                  required=None, class_names=None, class_name=None):
    return factory(
        forms.CharField(widget=forms.PasswordInput()),
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names,
        extra_options={
            "max_length": max_length,
            "min_length": min_length,
            }
    )


def EmailField(label=None, max_length=None, min_length=None,
               required=None, class_names=None, class_name=None):
    return factory(
        forms.EmailField(),
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names,
        extra_options={
            "max_length": max_length,
            "min_length": min_length,
            "email": True
        }
    )


def IntegerField(label=None, max_value=None, min_value=None,
                 required=None, class_names=None, class_name=None, initial_value=None):
    if class_names is None:
        class_names = []
    class_names.append('spin')
    return factory(
        forms.IntegerField(min_value=min_value, max_value=max_value),
        initial_value=initial_value,
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names,
        extra_options={
            "integer": True
        }
    )


def DateField(label=None, format=None, max_date=None,
              min_date=None, change_year=None, change_month=None,
              required=None, class_names=None, class_name=None):
    return factory(
        forms.DateField(widget=DateInput(
            max_date=max_date,
            min_date=min_date,
            format=format,
            change_year=change_year,
            change_month=change_month
        )),
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names
    )


def AutoCompleteField(lookup, label=None, min_length=2, delay=0,
                      required=None, class_names=None, class_name=None):
    widget = AutoCompleteWidget(delay=delay, min_length=min_length,
                                lookup=lookup)
    return factory(
        fields.AutoCompleteField(lookup=lookup, widget=widget),
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names
    )


def SimpleAutoCompleteField(lookup, label=None, min_length=2, delay=0,
                            required=None, class_names=None, class_name=None):
    widget = SimpleAutoCompleteWidget(delay=delay, min_length=min_length,
                                      lookup=lookup)
    return factory(
        fields.SimpleAutoCompleteField(widget=widget),
        label=label,
        required=required,
        class_name=class_name,
        class_names=class_names
    )
