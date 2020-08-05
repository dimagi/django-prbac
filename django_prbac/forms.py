from django.forms import ValidationError, CharField, TextInput

import django_prbac.csv


class StringListInput(TextInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, str):
            return super(StringListInput, self).render(name, value)
        else:
            rendered_value = django_prbac.csv.line_to_string(list(value))
            return super(StringListInput, self).render(name, rendered_value)


class StringSetInput(TextInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, str):
            return super(StringSetInput, self).render(name, value)
        else:
            rendered_value = django_prbac.csv.line_to_string(sorted(list(value)))
            return super(StringSetInput, self).render(name, rendered_value)


class StringListFormField(CharField):
    """
    A Django form field for lists of strings separated by commas, quotes optional
    """
    def __init__(self, quotechar=None, skipinitialspace=None, *args, **kwargs):
        self.quotechar = (quotechar or '"')
        self.skipinitialspace = True if skipinitialspace is None else skipinitialspace
        defaults = {'widget': StringListInput}
        defaults.update(kwargs)
        super(StringListFormField, self).__init__(*args, **defaults)

    def is_string_list(self, value):
        return isinstance(value, list) and all([isinstance(v, str) for v in value])

    def clean(self, value):
        if self.is_string_list(value):
            return value

        elif not isinstance(value, str):
            raise ValidationError('%r cannot be converted to a string list' % value)

        else:
            try:
                return django_prbac.csv.parse_line(
                    value,
                    skipinitialspace=self.skipinitialspace,
                    quotechar=self.quotechar,
                )

            except ValueError:
                raise ValidationError('%r cannot be converted to a string list' % value)

