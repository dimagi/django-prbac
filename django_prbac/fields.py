from django.db import models

import django_prbac.csv
from django_prbac.forms import StringListFormField


class StringListField(models.TextField):
    """
    A Django field for lists of strings
    """

    def is_string_list(self, value):
        return isinstance(value, list) and all([isinstance(v, str) for v in value])

    def to_python(self, value):
        """
        Best-effort conversion of "any value" to a string list.

        It does not try that hard, because curious values probably indicate
        a mistake and we should fail early.
        """

        # Already the appropriate python type
        if self.is_string_list(value):
            return value
        elif isinstance(value, str):
            return django_prbac.csv.parse_line(value)
        else:
            raise ValueError('Invalid value for StringListField: %r is neither the correct type nor deserializable' % value)

    def get_prep_value(self, value):
        """
        Converts the value, which must be a string list, to a comma-separated string,
        quoted appropriately. This format is private to the field type so it is not
        exposed for customization or any such thing.
        """

        if not self.is_string_list(value):
            raise ValueError('Invalid value for StringListField: %r' % value)
        else:
            return django_prbac.csv.line_to_string(value, lineterminator='')

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        """
        The default form field is a StringListFormField.
        """

        defaults = {'form_class': StringListFormField}
        defaults.update(kwargs)
        return super(StringListField, self).formfield(**defaults)

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        return self.to_python(value)


class StringSetField(StringListField):
    """
    A Django field for set of strings.
    """

    # TODO thought: If Python had polymorphism this ought be "Serialize a => Field (List a)"

    def is_string_set(self, value):
        return isinstance(value, set) and all([isinstance(v, str) for v in value])

    def to_python(self, value):
        """
        Best-effort conversion of "any value" to a string set. Mostly strict,
        but a bit lenient to allow lists to be passed in by form fields.
        """

        # Already the appropriate python type
        if self.is_string_set(value):
            return value

        # If it is a string list, we will turn it into a set; this lenience let's us
        # re-use the form field easily
        if self.is_string_list(value):
            return set(value)

        # First let StringListField do whatever it needs to do; this will now be a string list
        try:
            value = super(StringSetField, self).to_python(value)
        except ValueError:
            raise ValueError('Invalid value for StringSetField: %r' % value)

        return set(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if not self.is_string_set(value):
            raise ValueError('Invalid value %r for StringSetField' % value)
        else:
            return super(StringSetField, self).get_prep_value(sorted(value))

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        return self.to_python(value)
