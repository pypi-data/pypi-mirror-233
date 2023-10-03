#!/usr/bin/env python3
'''
Database functions.
'''

import json
import logging
import pathlib
import sqlite3

import pandas as pd

from chemfeat.csv_wrapper import CSVWrapper
from chemfeat.features.calculator import PREFIX_SEPARATOR


LOGGER = logging.getLogger(__name__)


def dict_factory(cursor, row):
    '''
    Row factor for SQLite to convert rows to dicts.
    '''
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


class FeatureDatabase():
    '''
    Database for saving features.
    '''
    INCHI_COLUMN_NAME = 'InChi'
    INCHI_COLUMN_INFO = (INCHI_COLUMN_NAME, 'TEXT', False, None, True)
    FEATURE_NAMES_TABLE_NAME = 'feature_names'
    FEATURE_NAMES_TABLE_INFO = [
        ('table', 'TEXT', False, None, True),
        ('feature_names', 'TEXT', False, None, False),
    ]
    FEATURES_COLUMN_NAME = 'features'
    NO_SUCH_TABLE_ERROR = 'no such table:'

    def __init__(self, path):
        self.path = pathlib.Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        LOGGER.info('Using database at %s', self.path)
        self.conn = sqlite3.Connection(str(self.path))

    def _get_table_info(self, table):
        '''
        Get the table information using the table_info pragma.

        Args:
            table:
                The name of the table.

        Returns:
            An iterator over the rows ("name", "type", "notnull", "dflt_value", "pk").

        https://www.sqlite.org/pragma.html#pragma_table_info
        '''
        with self.conn as conn:
            for row in conn.execute(f'PRAGMA table_info("{table}")'):
                # Skip the index.
                yield (row[1], row[2], bool(row[3]), row[4], bool(row[5]))

    @staticmethod
    def _col_info_to_col_def(col_info):
        '''
        Create a column definition from a row of table information.

        Args:
            col_info:
                The row of column information.

        Returns:
            A string with the column definition for a CREATE TABLE statement.
        '''
        name = col_info[0]
        typ = col_info[1].upper()
        notnull = ' NOT NULL' if col_info[2] else ''
        default = f' DEFAULT {col_info[3]}' if col_info[3] is not None else ''
        prim_key = ' PRIMARY KEY' if col_info[4] else ''
        return f'"{name}" {typ}{prim_key}{notnull}{default}'

    @classmethod
    def _table_info_to_col_def(cls, table_info):
        '''
        Convert table information to column definitions.

        Args:
            table_info:
                The rows of column information.

        Returns:
            A string with the column definitions for a CREATE TABLE statement.
        '''
        return ', '.join(cls._col_info_to_col_def(row) for row in table_info)

    def create_table_from_info(self, name, table_info):
        '''
        Create a table using the given table info. If the table already exists
        with the given info then no action is performed. If a table of the same
        name already exists with mismatched info then it is dropped and
        recreated.

        Args:
            name:
                The table name.

            table_info:
                The rows of table info.
        '''
        existing_info = list(self._get_table_info(name))
        if existing_info:
            if existing_info == table_info:
                return
            LOGGER.warning('Dropping table %s due to mismatched columns', name)
            with self.conn as conn:
                conn.execute(f'DROP TABLE "{name}"')

        LOGGER.info('Creating table %s', name)
        col_def = self._table_info_to_col_def(table_info)
        with self.conn as conn:
            conn.execute(f'CREATE TABLE IF NOT EXISTS "{name}" ({col_def})')

    @staticmethod
    def _group_features(features):
        '''
        Group sets of features by name.

        Args:
            features:
                A dictionary mapping features to values. All feature names must
                include a feature set prefix that ends with the
                chemfeat.features.calculator.PREFIX_SEPARATOR value. The prefix
                will be used as the feature set names.

        Returns:
            A dict mapping feature set names to the sorted names of the features in the
            set (e.g. {"foo": ["foo__feat1", "foo__feat2"]}).
        '''
        groups = {}
        for feat_name in features.keys():
            group_name = feat_name.split(PREFIX_SEPARATOR, 1)[0]
            groups.setdefault(group_name, set()).add(feat_name)
        return {name: sorted(feats) for (name, feats) in groups.items()}

    def create_feature_table(self, table_name):
        '''
        Create a table for holding a feature set. The features will be held in a
        blob due to default limits on the number of columns in an SQLite
        database.

        Args:
            table_name:
                The table name.
        '''
        table_info = [
            self.INCHI_COLUMN_INFO,
            (self.FEATURES_COLUMN_NAME, 'BLOB', False, None, False)
        ]
        self.create_table_from_info(table_name, table_info)

    def create_required_tables(self):
        '''
        Create the required tables.
        '''
        self.create_table_from_info(self.FEATURE_NAMES_TABLE_NAME, self.FEATURE_NAMES_TABLE_INFO)

    def insert_feature_names(self, set_name, feature_names):
        '''
        Insert the feature names into the database.

        Args:
            set_name:
                The feature set name.

            feature_names:
                The list of feature names.
        '''
        with self.conn as conn:
            conn.execute(
                f'REPLACE INTO {self.FEATURE_NAMES_TABLE_NAME} VALUES(?, ?)',
                [set_name, '\n'.join(feature_names)]
            )

    def get_feature_names(self, set_name):
        '''
        Get the list of feature names for the given feature set.
        '''
        try:
            with self.conn as conn:
                for row in conn.execute(
                    f'SELECT {self.FEATURE_NAMES_TABLE_INFO[1][0]} '
                    f'FROM {self.FEATURE_NAMES_TABLE_NAME} '
                    f'WHERE {self.FEATURE_NAMES_TABLE_INFO[0][0]}=?',
                    [set_name]
                ):
                    return row[0].splitlines()
        except sqlite3.OperationalError as err:
            if not err.args[0].startswith(self.NO_SUCH_TABLE_ERROR):
                LOGGER.error('%s', err)
        return None

    def get_all_feature_names(self):
        '''
        Get a dict mapping feature sets to feature names.
        '''
        feature_names = {}
        try:
            with self.conn as conn:
                for row in conn.execute(f'SELECT * FROM {self.FEATURE_NAMES_TABLE_NAME}'):
                    feature_names[row[0]] = row[1].splitlines()
        except sqlite3.OperationalError as err:
            if not err.args[0].startswith(self.NO_SUCH_TABLE_ERROR):
                LOGGER.error('%s', err)
        return feature_names

    def _parse_inserts(self, items):
        '''
        Internal generator for inserting features into table. This is used to
        accumulate rows for chunked insertion with executemany().

        Args:
            items:
                Same as insert_features.

        Returns:
            A generator over 3-tuples of database names, InChi strings and
            feature objects as JSON strings.
        '''
        is_first = True
        for inchi, features in items:
            if not features:
                LOGGER.warning('No features for %s', inchi)
                continue
            grouped_features = self._group_features(features)
            features[self.INCHI_COLUMN_NAME] = inchi

            # Ensure that the expected tables exist.
            if is_first:
                self.create_required_tables()
                all_existing_feature_names = self.get_all_feature_names()

                for name, feat_names in grouped_features.items():
                    existing_feature_names = all_existing_feature_names.get(name)
                    if existing_feature_names:
                        if existing_feature_names != feat_names:
                            LOGGER.warning(
                                "Dropping table %s due to mismatched columns",
                                name
                            )
                            with self.conn as conn:
                                conn.execute(f'DROP TABLE IF EXISTS "{name}"')
                            self.insert_feature_names(name, feat_names)
                    else:
                        self.insert_feature_names(name, feat_names)
                    self.create_feature_table(name)
                is_first = False

            for name, feat_names in grouped_features.items():
                yield name, inchi, json.dumps([features[name] for name in feat_names])

    def _insert_rows(self, name, rows):
        '''
        Insert rows into feature set tables.

        Args:
            name:
                The feature set name.

            rows:
                An iterator of 2-tuples of InChi strings and JSON strings.
        '''
        LOGGER.info('Inserting %s row(s) into table %s.', len(rows), name)

        with self.conn as conn:
            conn.executemany(f'REPLACE INTO "{name}" VALUES(?, ?)', rows)

    def insert_features(self, items):
        '''
        Insert features into the database.

        Args:
            items:
                An iterator over 3-tuples of (<name>, <inchi>, <features>) where
                <name> is the feature set name, <inchi> is the molecule's InChi,
                and <features> is a dict mapping feature names to their values.

                This must be equivalent to the iterator returned by
                FeatureManager.calculate_features.
        '''
        # Chunk size for database insertion using executemany().
        chunksize = 1000

        all_rows = {}
        for name, inchi, feats in self._parse_inserts(items):
            rows = all_rows.setdefault(name, [])
            rows.append((inchi, feats))
            if len(rows) >= chunksize:
                self._insert_rows(name, rows)
                rows.clear()

        for name, rows in all_rows.items():
            if rows:
                self._insert_rows(name, rows)

    def is_inchi_in_table(self, inchi, name):
        '''
        Check if an InChi is already in a table.

        Args:
            inchi:
                The InChi.

            name:
                The table name.

        Returns:
            A boolean indicating if the InChi exists in the given table.
        '''
        with self.conn as conn:
            return bool(
                conn.execute(
                    f'SELECT 1 FROM "{name}" WHERE {self.INCHI_COLUMN_NAME}=?',
                    [inchi]
                )
            )

    def inchis_in_table(self, name):
        '''
        Return all the InChis in a given table.

        Args:
            name:
                The table name.

        Returns:
            A generator over the InChis in the given table.
        '''
        try:
            with self.conn as conn:
                for row in conn.execute(f'SELECT "{self.INCHI_COLUMN_NAME}" FROM "{name}"'):
                    yield row[0]
        except sqlite3.OperationalError as err:
            if not err.args[0].startswith(self.NO_SUCH_TABLE_ERROR):
                LOGGER.error('%s', err)

    def _execute_to_dicts(self, *args, **kwargs):
        '''
        Execute a query and return a generator that converts each row to a dict.

        Args:
            *args, **kwargs:
                Positional and keyword arguments passed through to execute().

        Returns:
            A generator of dicts.
        '''
        with self.conn as conn:
            conn.row_factory = dict_factory
            yield from conn.execute(*args, **kwargs)

    def get_features(self, inchi, name):
        '''
        Get the features for the InChi from the given table.

        Args:
            inchi:
                The InChi.

            name:
                The table name.

        Returns:
            A dict with the features, or None if the InChi was not found.
        '''
        keys = self.get_feature_names(name)
        if not keys:
            return None

        with self.conn as conn:
            for row in conn.execute(
                f'SELECT {self.FEATURES_COLUMN_NAME} '
                f'FROM "{name}" WHERE {self.INCHI_COLUMN_NAME}=?',
                [inchi]
            ):
                values = json.loads(row[0])
                return dict(zip(keys, values))
        return None

    def _get_join_sql_query(self, names):
        '''
        Get the SQL query to (inner) join the given table names. All tables will
        be joined on the InChi primary key.

        Args:
            names:
                The names of the tables to include.

        Returns:
            The SQL query as a string.
        '''
        first_name = names[0]

        tmp_col_names = ((name, self.FEATURES_COLUMN_NAME) for name in names)
        tmp_col_names = (
            f'"{tname}"."{cname}" AS "{tname}_{cname}"'
            for (tname, cname) in tmp_col_names
        )
        col_names = ', '.join((
            f'"{first_name}"."{self.INCHI_COLUMN_NAME}" AS "{self.INCHI_COLUMN_NAME}"',
            *tmp_col_names
        ))

        sql = f'SELECT {col_names} FROM "{first_name}"'
        for name in names[1:]:
            sql += (
                f' INNER JOIN "{name}" '
                f'ON "{name}"."{self.INCHI_COLUMN_NAME}" = '
                f'"{first_name}"."{self.INCHI_COLUMN_NAME}"'
            )
        LOGGER.debug('SQL INNER JOIN QUERY: %s', sql)
        return sql

    def _get_join_dicts(self, names):
        '''
        Get a generator over dicts of features created by joining the data from
        the given tables.

        Args:
            names:
                The tables to join.

        Returns:
            A generator over the dictionaries.
        '''
        sql = self._get_join_sql_query(names)
        inchi_col_name = self.INCHI_COLUMN_NAME
        suffix = f'_{self.FEATURES_COLUMN_NAME}'
        suffix_len = len(suffix)
        feat_names = self.get_all_feature_names()
        for row in self._execute_to_dicts(sql):
            features = {}
            for key, value in row.items():
                if key.endswith(suffix):
                    name = key[:-suffix_len]
                    features.update(zip(feat_names[name], json.loads(value)))
                elif key == inchi_col_name:
                    features[inchi_col_name] = value
            yield features

    def _filter_inchis(self, rows, inchis=None):
        '''
        Filter rows without selected inchis.j

        Args:
            rows:
                An iterator over dicts as returned by _get_join_dicts().

            inchis:
                An iterable of InChis. Only rows with InChis in this set will be
                included in the output. If None then all rows will be returned.

        Returns:
            A generator over the filtered dicts.
        '''
        if inchis is None:
            yield from rows
            return

        inchis = set(inchis)
        if not inchis:
            return

        for row in rows:
            if row[self.INCHI_COLUMN_NAME] in inchis:
                yield row

    def get_dataframe(self, names, inchis=None):
        '''
        Get a Pandas Dataframe with the features of the given tables.

        Args:
            names:
                The names of the tables to include.

            inchis:
                An optional iterable of InChis.

        Returns:
            The Pandas Dataframe.
        '''
        rows = self._get_join_dicts(names)
        rows = self._filter_inchis(rows, inchis)
        return pd.DataFrame(rows)

    def save_csv(self, path, names, inchis=None):
        '''
        Save features from the given tables to a CSV file.

        Args:
            path:
                The output path.

            names:
                The names of the tables to include.

            inchis:
                An optional iterable of InChis.
        '''
        if isinstance(inchis, pd.Series):
            inchis = inchis.values

        rows = self._get_join_dicts(names)
        rows = self._filter_inchis(rows, inchis)

        LOGGER.info('Saving features to %s', path)
        csv_wrapper = CSVWrapper(path)
        csv_wrapper.write_rows(rows)
