# Use Modern Python
from __future__ import unicode_literals, absolute_import, print_function

# System imports

# Django imports
from django.db import models

# External libraries
import six
import simplejson
from south.modelsinspector import add_introspection_rules

# Make South understand these fields; no special treatment
add_introspection_rules([], ["^django_prbac\.fields\.StringListField"])
add_introspection_rules([], ["^django_prbac\.fields\.StringSetField"])

class StringListField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """
    A Django field for lists of strings
    """

    # TODO thought: If Python had polymorphism this ought be "Serialize a => Field (List a)"

    def is_string_list(self, value):
        return isinstance(value, list) and all([isinstance(v, six.string_types) for v in value])

    def to_python(self, value):
        """
        Handles exactly two cases:
        1. The value is already a (unicode, not bytes) string list.
           - then it is returned as-is
        2. The value is a string (not super sure how Django deals w/ database fields w.r.t. unicode)
           - then it is deserialized and return if and only if it is a string list
        """

        # Already the appropriate python type
        if self.is_string_list(value):
            return value

        # First let TextField do whatever it needs to do
        value = super(StringListField, self).to_python(value)

        if isinstance(value, six.string_types):
            deserialized = simplejson.loads(value)
            if self.is_string_list(deserialized):
                return deserialized
            else:
                raise ValueError('Invalid value for StringListField: %r does not deserialize to string list' % value)
        else:
            raise ValueError('Invalid value for StringListField: %r is neither the correct type nor deserializable' % value)

    def get_prep_value(self, value):
        if not isinstance(value, list):
            raise ValueError('Invalid value for StringListField: %r' % value)
        else:
            return simplejson.dumps(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class StringSetField(six.with_metaclass(models.SubfieldBase, StringListField)):
    """
    A Django field for set of strings.
    """

    # TODO thought: If Python had polymorphism this ought be "Serialize a => Field (List a)"

    def is_string_set(self, value):
        return isinstance(value, set) and all([isinstance(v, six.string_types) for v in value])

    def to_python(self, value):
        """
        Handles exactly two cases:
        1. The value is already a (unicode, not bytes) string set.
           - then it is returned as-is
        2. The value is a string (not super sure how Django deals w/ database fields w.r.t. unicode)
           - then it is deserialized and returned as a set if and only if it is a string list
        """

        # Already the appropriate python type
        if self.is_string_set(value):
            return value

        # First let StringListField do whatever it needs to do; this will now be a string list
        try:
            oldval = value
            value = super(StringSetField, self).to_python(value)
        except ValueError as exc:
            raise ValueError('Invalid value for StringSetField: %r' % value)

        return set(value)

    def get_prep_value(self, value):
        if not isinstance(value, set) or any([not isinstance(v, six.string_types) for v in value]):
            raise ValueError('Invalid value %r for StringSetField' % value)
        else:
            return super(StringSetField, self).get_prep_value(sorted(value))
