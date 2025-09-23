from django.test import TestCase

from django_prbac.fields import StringListField, StringSetField


class TestStringListField(TestCase):
    """
    Test suite for django_prbac.fields.StringListField
    """

    def test_is_string_list(self):
        field = StringListField('testing')

        self.assertTrue(field.is_string_list([]))
        self.assertTrue(field.is_string_list(["hello", "goodbye"]))

        self.assertFalse(field.is_string_list("boo"))
        self.assertFalse(field.is_string_list(3))
        self.assertFalse(field.is_string_list('"A","B"'))

    def test_to_python_convert(self):
        field = StringListField('testing')
        self.assertEqual(field.to_python(''), [])
        self.assertEqual(field.to_python('"A","B","C"'), ['A', 'B', 'C'])

    def test_to_python_already_done(self):
        field = StringListField('testing')
        self.assertEqual(field.to_python([]), [])
        self.assertEqual(field.to_python(["A", "B", "C"]), ['A', 'B', 'C'])

        with self.assertRaises(ValueError):
            field.to_python(4)

        with self.assertRaises(ValueError):
            field.to_python([1, 2, 3])

        with self.assertRaises(ValueError):
            field.to_python(None)

    def test_get_prep_value_convert(self):
        field = StringListField('testing')

        self.assertEqual(field.get_prep_value(["A", "B", "C"]), 'A,B,C')
        self.assertEqual(field.get_prep_value(["A", "B,C", "D"]), 'A,"B,C",D')

        with self.assertRaises(ValueError):
            field.get_prep_value(5)


class TestStringSetField(TestCase):
    """
    Test suite for django_prbac.fields.StringSetField
    """

    def test_is_string_set(self):
        field = StringSetField('testing')

        self.assertTrue(field.is_string_set(set([])))
        self.assertTrue(field.is_string_set(set(["hello", "goodbye"])))

        self.assertFalse(field.is_string_set(["A", "B"]))
        self.assertFalse(field.is_string_set("boo"))
        self.assertFalse(field.is_string_set(3))
        self.assertFalse(field.is_string_set('["A", "B"]'))

    def test_to_python_convert(self):
        field = StringSetField('testing')

        # This that are legitimate to store in the DB
        self.assertEqual(field.to_python(''), set())
        self.assertEqual(field.to_python('"A","B","C"'), set(['A', 'B', 'C']))

    def test_to_python_already_done(self):
        field = StringSetField('testing')
        self.assertEqual(field.to_python([]), set())
        self.assertEqual(field.to_python(set(["A","B","C"])), set(['A', 'B', 'C']))

        with self.assertRaises(ValueError):
            field.to_python(4)

        with self.assertRaises(ValueError):
            field.to_python([1, 2, 3])

        with self.assertRaises(ValueError):
            field.to_python(None)

    def test_get_prep_value_convert(self):
        field = StringSetField('testing')

        self.assertEqual(field.get_prep_value(set(["A", "B", "C"])), 'A,B,C')
        self.assertEqual(field.get_prep_value(set(["C", "B", "A"])), 'A,B,C')

        with self.assertRaises(ValueError):
            field.get_prep_value(5)
