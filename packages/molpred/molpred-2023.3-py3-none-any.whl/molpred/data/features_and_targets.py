#!/usr/bin/env python3

'''
Load features and targets from CSV files.
'''


import logging
import pathlib

import pandas as pd


LOGGER = logging.getLogger(__name__)


def bin_targets(targets, column_bins=None, default_bins=10):
    '''
    Return the name and a categorical representation of the values in each
    column in the targets dataframe.

    Args:
        targets:
            The dataframe of targets.

        column_bins:
            A optional dict mapping column names to positive integers. The
            numeric values in the corresponding columns will be split into this
            many bins.

        default_bins:
            An integer number of bins. Numeric columns with more unique values
            than this and for which no bins have been specified in column_bins
            will will be split into this number of bins. To avoid binning a
            column, set the value to 0 in column_bins.

    Returns:
        A iterator over 2-tuples of column names and a Pandas Series containing
        their categorical values.
    '''
    if column_bins is None:
        yield from targets.items()
        return

    if not isinstance(column_bins, dict):
        column_bins = dict(column_bins)

    for name, values in targets.items():
        n_bins = column_bins.get(name)
        if n_bins is None \
                and pd.api.types.is_numeric_dtype(values)\
                and values.unique().size > default_bins:
            n_bins = default_bins
        if n_bins > 0:
            yield name, pd.cut(values, n_bins)
        else:
            yield name, values


class FeaturesAndTargets():
    '''
    Convenience class for working with features and targets.
    '''
    def __init__(self, path, column_specifier, column_bins=None):
        '''
        Args:
            path:
                The path to the CSV file with the features and targets. It will
                be lazily loaded when the data is required.

            column_specifier:
                A ColumnSpecifier instance specifying the feature and target
                columns to load.

            column_bins:
                Passed through to binned_targets to retrieve binned targets.
        '''
        path = pathlib.Path(path).resolve()
        self.path = path
        self.column_specifier = column_specifier
        self.column_bins = column_bins
        self._data = None
        self._binned_data = None
        self._binned_targets = None

    @property
    def data(self):
        '''
        The CSV data.
        '''
        # Lazily load the data.
        if self._data is None:
            LOGGER.debug('Loading data from %s', self.path)
            self._data = pd.read_csv(self.path, usecols=self.column_specifier.names)
        return self._data

    @property
    def columns(self):
        '''
        The Pandas series of column names.
        '''
        return self.data.columns.to_series()

    @property
    def feature_names(self):
        '''
        The Pandas series of feature names.
        '''
        cols = self.columns
        return cols[cols.isin(self.column_specifier.features)]

    @property
    def target_names(self):
        '''
        The Pandas series of target names.
        '''
        cols = self.columns
        return cols[cols.isin(self.column_specifier.targets)]

    @property
    def features(self):
        '''
        The features dataframe.
        '''
        return self.data[self.feature_names]

    @property
    def targets(self):
        '''
        The targets dataframe.
        '''
        return self.data[self.target_names]

    @property
    def features_and_targets(self):
        '''
        The features and targets as a 2-tuple.
        '''
        return self.features, self.targets

    @property
    def n_targets(self):
        '''
        The number of different target columns.
        '''
        return self.targets.shape[1]

    @property
    def binned_targets(self):
        '''
        The binned targets.
        '''
        if self._binned_targets is None:
            binned_series = list(
                zip(
                    *bin_targets(
                        self.targets,
                        column_bins=self.column_bins
                    )
                )
            )[1]
            self._binned_targets = pd.concat(binned_series, axis=1)
        return self._binned_targets

    @property
    def binned_data(self):
        '''
        The dataframe with the features and the binned targets.
        '''
        if self._binned_data is None:
            self._binned_data = pd.concat([self.features, self.binned_targets], axis=1)
        return self._binned_data
