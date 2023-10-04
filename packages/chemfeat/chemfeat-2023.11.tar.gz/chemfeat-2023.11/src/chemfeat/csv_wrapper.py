#!/usr/bin/env python3

'''
Functions for working with CSV files.
'''

import csv
import logging
import pathlib


LOGGER = logging.getLogger(__name__)


class CSVWrapper():
    '''
    Wrapper around a CSV file to faciliate appending rows in real-time via an
    iterable of dictionaries.
    '''
    ENCODING = 'utf-8'

    def __init__(self, path, **kwargs):
        self.path = pathlib.Path(path).resolve()
        self.kwargs = kwargs

    @property
    def headers(self):
        '''
        The current headers from the CSV file, or None if they do not exist.

        This assumes that the first row contains the headers.
        '''
        try:
            with self.path.open('r', encoding=self.ENCODING) as csvfile:
                reader = csv.reader(csvfile, **self.kwargs)
                for row in reader:
                    return row
        except FileNotFoundError:
            pass
        return None

    def __iter__(self):
        try:
            with self.path.open('r', encoding=self.ENCODING) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    yield row
        except FileNotFoundError:
            pass

    def write_rows(self, rows, headers=None, append=False):
        '''
        Append rows to the CSV file.

        Args:
            rows:
                A generator of dicts.
        '''
        if append:
            existing_headers = self.headers
            if existing_headers is not None:
                if headers is not None and existing_headers != headers:
                    LOGGER.warning('Re-using existing headers: %s', existing_headers)
                headers = existing_headers

        first_row = None
        try:
            if headers is None:
                first_row = next(rows)
                headers = sorted(first_row)
        except StopIteration:
            LOGGER.warning('Attempting to append 0 rows to %s', self.path)

        mode = 'a' if append else 'w'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open(mode, encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, **self.kwargs)

            if first_row:
                writer.writeheader()
                writer.writerow(first_row)
                csvfile.flush()

            for row in rows:
                writer.writerow(row)
                csvfile.flush()
