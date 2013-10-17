from __future__ import unicode_literals

from django.db import models

import six
import simplejson

class StringListField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """
    A Django field for lists of strings
    """

    # TODO thought: If Python had polymorphism this ought be "Serialize a => Field (List a)"

    def is_already_python(self, value):
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
        if self.is_already_python(value):
            return value

        # First let TextField do whatever it needs to do
        value = super(StringListField, self).to_python(value)

        if isinstance(value, six.string_types):
            deserialized = simplejson.loads(value)
            if self.is_already_python(deserialized):
                return deserialized
            else:
                raise ValueError('Invalid value for StringListField: %r does not deserialize to strin glist' % value)
        else:
            raise ValueError('Invalid value for StringListField: %r is neither the write type nor deserializable' % value)

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

    def is_already_python(self, value):
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
        if self.is_already_python(value):
            return value

        # First let StringListField do whatever it needs to do; this will now be a string list
        try:
            value = super(StringListField, self).to_python(value)
        except ValueError:
            raise ValueError('Invalid value for StringSetField: %r' % value)

        return set(value)

    def get_prep_value(self, value):
        if not isinstance(value, set) or any([not isinstance(v, six.string_types) for v in value]):
            raise ValueError('Invalid value %r for StringSetField' % value)
        else:
            return super(StringSetField, self).get_prep_value(list(value))
