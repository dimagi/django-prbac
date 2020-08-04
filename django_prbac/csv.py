import csv
from io import StringIO


def parse_line(value, quotechar=None, **kwargs):
    """
    A simple wrapper to parse a single CSV value
    """
    quotechar = quotechar or '"'
    return next(csv.reader([value], quotechar=quotechar, **kwargs), None)


def line_to_string(value, **kwargs):
    """
    A simple wrapper to write one CSV line
    """
    fh = StringIO()
    csv.writer(fh, **kwargs).writerow(value)
    return fh.getvalue()
