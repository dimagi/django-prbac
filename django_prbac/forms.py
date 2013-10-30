# Use Modern Python
from __future__ import unicode_literals, absolute_import, print_function

# System imports

# Django imports
from django.forms import ValidationError, Field

# External libraries
import six
import csv
import simplejson

class StringListFormField(Field):
    """
    A Django form field for lists of strings separated by commas, quotes optional
    """
    def __init__(self, quotechar=None, skipinitialspace=None, *args, **kwargs):
        self.quotechar = (quotechar or '"').encode('utf-8') # csv requires bytes, not a string
        self.skipinitialspace = True if skipinitialspace is None else skipinitialspace
        super(StringListFormField, self).__init__(*args, **kwargs)

    def is_string_list(self, value):
        return isinstance(value, list) and all([isinstance(v, six.string_types) for v in value])

    def clean(self, value):
        if self.is_string_list(value):
            return value

        elif not isinstance(value, six.string_types):
            raise ValidationError('%r cannot be converted to a string list' % value)

        else:
            try:
                for row in csv.reader([value], quotechar=self.quotechar, skipinitialspace=self.skipinitialspace):
                    return [s.decode('utf-8') for s in row]
            except ValueError:
                raise ValidationError('%r cannot be converted to a string list' % value)
