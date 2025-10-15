"""
Widget with two numeric fields:
- value
- error (always positive)
Displays the ± symbol between the fields.
"""

# Third-party libraries
from django import forms
from django.utils.safestring import mark_safe

# Custom widget that shows two number input fields side by side:
# - First field: value
# - Second field: positive error
# Inserts the '±' symbol between them in the rendered HTML.
class ValueWithErrorWidget(forms.MultiWidget):

    def __init__(self, attrs=None, value_attrs=None, error_attrs=None):
        # Default attributes for each input
        value_attrs = value_attrs or {'step': 'any', 'style': 'width:80px;'}
        error_attrs = error_attrs or {'step': 'any', 'min': 0, 'style': 'width:80px;'}

        # Define the two NumberInput widgets
        widgets = [
            forms.NumberInput(attrs=value_attrs),
            forms.NumberInput(attrs=error_attrs),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        # Converts the stored value into a list [value, error] for the widget.
        # Accepts:
        # - None -> [None, None]
        # - list/tuple -> [value, error]
        # - string like 'value ± error' -> [float(value), float(error)]
        if value is None:
            return [None, None]
        if isinstance(value, (list, tuple)):
            return list(value)
        if isinstance(value, str) and '±' in value:
            try:
                val, err = value.split('±')
                return [float(val.strip()), float(err.strip())]
            except Exception:
                return [None, None]
        return [value, None]

    def render(self, name, value, attrs=None, renderer=None):
        # Decompress value if needed
        if value is None:
            value = [None, None]
        elif isinstance(value, str) and '±' in value:
            value = self.decompress(value)
        else:
            value = self.decompress(value)

        # Render each widget individually
        rendered_widgets = []
        for i, widget in enumerate(self.widgets):
            widget_name = f"{name}_{i}"
            rendered_widgets.append(widget.render(widget_name, value[i], attrs=attrs, renderer=renderer))

        # Join the two widgets with ± symbol and return safe HTML
        return mark_safe(f"{rendered_widgets[0]} &nbsp;&plusmn;&nbsp; {rendered_widgets[1]}")

        
# Custom form field that always returns a list [value, error] in cleaned_data.
class ValueWithErrorField(forms.MultiValueField):

    widget = ValueWithErrorWidget

    # Define the two fields: value and positive error
    def __init__(self, *args, **kwargs):
        fields = (
            forms.FloatField(required=False),
            forms.FloatField(required=False, min_value=0),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        # Combine the two input values into a list [value, error].
        # Ensures error is always non-negative.
        if data_list:
            val = data_list[0]
            err = data_list[1] if data_list[1] is not None else 0
            if err is not None:
                err = abs(err)
            return [val, err]
        return [None, None]
