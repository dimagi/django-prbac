# Use Modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Django imports
from django.test import TestCase

# Local imports
from django_prbac.forms import StringListFormField


class TestStringListFormField(TestCase):
    """
    Test suite for django_prbac.fields.StringListField
    """

    def test_clean(self):
        field = StringListFormField(required=False, skipinitialspace=False)

        self.assertEqual(field.clean('hello, goodbye'), ['hello', ' goodbye'])
        self.assertEqual(field.clean('hello,goodbye'), ['hello', 'goodbye'])
        self.assertEqual(field.clean('"hello",    goodbye'), ['hello', '    goodbye'])
        self.assertEqual(field.clean('"hello"," oh no "'), ['hello', ' oh no '])
        self.assertEqual(field.clean('"hello","one,two"'), ['hello', 'one,two'])

    def test_quotechar(self):
        field = StringListFormField(required=False, quotechar='|')

        self.assertEqual(field.clean('hello, goodbye'), ['hello', 'goodbye'])
        self.assertEqual(field.clean('hello,goodbye'), ['hello', 'goodbye'])
        self.assertEqual(field.clean('hello,    goodbye'), ['hello', 'goodbye'])
        self.assertEqual(field.clean('"hello",    goodbye'), ['"hello"', 'goodbye'])
        self.assertEqual(field.clean('"hello","oh, no"'), ['"hello"', '"oh', 'no"'])
        self.assertEqual(field.clean('hello,|oh, no|'), ['hello', 'oh, no'])
