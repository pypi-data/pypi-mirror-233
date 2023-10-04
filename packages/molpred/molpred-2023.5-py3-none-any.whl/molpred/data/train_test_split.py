#!/usr/bin/env python3

'''
Split data into train and test sets.
'''

import logging

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from simple_file_lock import FileLock

from molpred.data.common import missing_or_older, tag_path


LOGGER = logging.getLogger(__name__)


def balanced_train_test_split(
    features_and_targets,
    train_size=None,
    test_size=None
):
    '''
    Create a test-train split that balances the classes in the train set. This
    uses np.random.choice so it will be pseudo-random unless the random state is
    set beforehand with np.random.set_state.

    If multiple targets are given then the set of unique target combinations
    present in the data is used to balanced the train-test split.

    Args:
        features_and_targets:
            An instance of FeaturesAndTargets with the data to split.

        train_size, test_size:
            Same as :func:`sklearn.model_selection.train_test_split`.

    Returns:
        Train data, test data, train target, test target.
    '''
    if train_size is None:
        train_size = 0.75 if test_size is None else (1.0 - test_size)

    features = features_and_targets.features
    targets = features_and_targets.targets
    binned_targets = features_and_targets.binned_targets
    unique_targets = set(binned_targets.itertuples(index=False, name=None))

    masks = [(binned_targets == uniq_targ).all(axis=1) for uniq_targ in unique_targets]

    # Determine the least represented class and set the number of each class in
    # the training set to the requested test fraction of this size.
    n_train = int(min(mask.sum() for mask in masks) * train_size)
    if n_train == 0:
        raise ValueError(
            'Not enough values available for balanced train-test '
            f'split with train size {train_size:0.2f}'
        )

    train_mask = np.zeros(features.shape[0], dtype=bool)
    train_indices = np.arange(0, train_mask.shape[0])

    for mask in masks:
        selected = np.random.choice(train_indices[mask], n_train, replace=False)
        train_mask[selected] = True

    test_mask = ~train_mask

    return features[train_mask], features[test_mask], targets[train_mask], targets[test_mask]


def get_train_test_split_paths(
    features_and_targets,
    balanced=True,
    train_size=0.75
):
    '''
    Get the paths to the train and test data. If the files do not yet exist
    then they will be created from the input data.

    Args:
        features_and_targets:
            A FeaturesAndTargets instance with the data to split.

        column_specifier:
            A ColumnSpecifier instance for specifying feature and target columns.

        balanced:
            If True, ensure that the classes are balanced in the training set.

        train_size:
            The proportion of the data to use for the training set. It should
            lie in the interval (0.0, 1.0) and will be rounded to the nearest
            hundred i.e. the nearest percent).

        column_bins:
            Passed through to balanced_train_test_split().
    '''
    try:
        train_size = float(train_size)
    except ValueError as err:
        raise ValueError('train_size must be an int or float') from err

    # Round to nearest percent.
    train_size = round(100 * train_size) / 100.

    if not 0. < train_size < 1.:
        raise ValueError('train_size must be greater than 0 and less than 1')

    data_path = features_and_targets.path.resolve()
    tag = f'{"-balanced" if balanced else ""}-{int(100 * train_size):02d}'
    train_path = tag_path(data_path, f'{tag}-train')
    test_path = tag_path(data_path, f'{tag}-test')

    with FileLock(data_path), FileLock(train_path), FileLock(test_path):
        if missing_or_older([train_path, test_path], [data_path]):
            if balanced:
                splits = balanced_train_test_split(
                    features_and_targets,
                    train_size=train_size
                )
            else:
                splits = train_test_split(
                    features_and_targets.features,
                    features_and_targets.targets,
                    train_size=train_size,
                    stratify=list(zip(*features_and_targets.targets))
                )

            train_data = pd.concat(splits[0::2], axis=1, join='inner')
            train_data.to_csv(train_path, index=False)

            test_data = pd.concat(splits[1::2], axis=1, join='inner')
            test_data.to_csv(test_path, index=False)

        return train_path, test_path
