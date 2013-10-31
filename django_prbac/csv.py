# Use Modern Python
from __future__ import unicode_literals, absolute_import, print_function

# System imports
import csv

# External libraries
import six

def parse_line(value, **kwargs):
    """
    A simple wrapper to parse a single CSV value
    """

    for row in csv.reader([value], **kwargs):
        return [s.decode('utf-8') for s in row]

def line_to_string(value, **kwargs):
    """
    A simple wrapper to write one CSV line
    """

    fh = six.StringIO()
    csv.writer(fh, **kwargs).writerow(value)
    return fh.getvalue()
