#!/usr/bin/env python3

'''
Class for loading CSV files with InChIs and associated data.
'''

import logging
import pathlib

import pandas as pd

from molpred.data.column_specifier import ColumnSpecifier


LOGGER = logging.getLogger(__name__)

# The default InChI column name.
INCHI_COLUMN = 'InChI'


class InChILoader():
    '''
    Convenience class for loading InChIs with optional target columns from CSV files.
    '''

    # Map of names to registered functions that can be used as column
    # transformers when loading data. This allows the transformers to be
    # specified using text configuration such as YAML files.
    TRANSFORMERS = {}

    def __init__(
        self,
        path,
        inchi_column=INCHI_COLUMN,
        column_specifier=None,
        transformers=None
    ):
        '''
        Args:
            path:
                The path to the CSV file.

            inchi_column:
                The name of the column containing the InChI strings. Defaults to
                the value of molpred.common.INCHI_COLUMN.

            column_specifier:
                An instance of ColumnSpecifier for specifying feature and target
                columns to load from the data, or a dict of keyword arguments
                that can be used to instantiate an instance of ColumnSpecifier.

            transformers:
                An optional dict mapping column names to functions that should
                be applied to the the values in the column. If functions have
                been registered with InChILoader.register_transformer then the
                registered name can be use in place of the function. It may also
                be specified as a list of 2-tuples which will be converted to a
                dict.
        '''
        self.path = pathlib.Path(path).resolve()
        self.inchi_column = inchi_column
        if isinstance(column_specifier, dict):
            column_specifier = ColumnSpecifier(**column_specifier)
        elif column_specifier is None:
            column_specifier = ColumnSpecifier()
        elif not isinstance(column_specifier, ColumnSpecifier):
            LOGGER.error('Invalid ColumnSpecifier argument: %s', column_specifier)
            LOGGER.warning('Defaulting to an empty ColumnSpecifier')
        self.column_specifier = column_specifier

        LOGGER.debug('InputLoader: loading %s', path)
        columns = sorted(column_specifier.names) if column_specifier else []
        self.data = pd.read_csv(
            path,
            usecols=[self.inchi_column, *columns]
        ).set_index(self.inchi_column)

        if transformers:
            if isinstance(transformers, dict):
                transformers = transformers.items()
            for name, func in transformers:
                if isinstance(func, str):
                    try:
                        func = self.TRANSFORMERS[func]
                    except KeyError as err:
                        raise ValueError(f'"{func} is not a registered function name') from err
                self.data[name] = self.data[name].apply(func)

    @classmethod
    def register_transformer(cls, name, func):
        '''
        Register a transformer function under the given name. The name can then
        be used as a value in the transformers dict passed to __init__.

        Args:
            name:
                The name under which to register the function.

            func:
                A function that accepts a value and returns a value, which can
                be applied to a column of a data frame.
        '''
        cls.TRANSFORMERS[name] = func

    @property
    def mtime(self):
        '''
        The last modification time of the data.
        '''
        return self.path.stat().st_mtime

    @property
    def inchis(self):
        '''
        The InChIs in the input data.
        '''
        return self.data.index.to_series(name=self.inchi_column)

    def __getitem__(self, key):
        '''
        Passthrough to underlying data.
        '''
        if isinstance(key, set):
            key = sorted(key)
        return self.data[key]

    def join(
        self,
        dataframe,
        columns=None,
        extra=False,
        inchi_column=None,
    ):
        '''
        Join columns from the loaded data to the given dataframe. This uses an
        inner join on the InChI column.


        Args:
            dataframe:
                The dataframe to which the target columns should be joined. It
                must contain an InChI column.

            columns:
                An iterable of column names to join from the loaded data. If
                None, then all of the loaded feature and target columns will be
                joined. To include extra columns, set "extra" to True when this
                is None.

            extra:
                If True, include extra columns when "columns" is None.

            inchi_column:
                The name of the passed dataframe's InChI column. If None, the
                default name will be used.

        Returns:
            The joined dataframe.
        '''
        if inchi_column is None:
            inchi_column = INCHI_COLUMN

        columns = sorted(
            (self.column_specifier.names if extra else self.column_specifier.features_and_targets)
            if columns is None else set(columns)
        )

        if columns:
            return dataframe.join(self.data[columns], on=inchi_column, how='inner')
        return dataframe
