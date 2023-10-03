#!/usr/bin/env python3

'''
Visualize data.
'''

import logging
import re

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from pandas.api.types import CategoricalDtype


LOGGER = logging.getLogger(__name__)


def plot_text(ax, text):  # pylint: disable=invalid-name
    '''
    Plot text in the center of an axis.

    Args:
        ax:
            The axis object.

        test:
            The text to display.
    '''
    ax.text(0.5, 0.5, text, horizontalalignment='center', verticalalignment='center')


def group_names_by_prefix(names):
    '''
    Group names by common prefixes when they follow the pattern
    "<prefix><integer>". Such groups are expected to represent fingerprints.

    Args:
        names:
            An iterable of names to group.

    Returns:
        A generator over Pandas Series with the names of each group.
    '''
    # Collect and sort for deterministic ordering.
    groups = {}
    regex = re.compile(r'^(.*?)(\d+)$')
    for name in names:
        match = regex.match(name)
        if match:
            name = match.group(1)
            index = match.group(2)
            n_digits = len(str(index))
            groups.setdefault((name, n_digits), []).append(index)
        else:
            groups[name] = [name]

    for key, ids in sorted(groups.items()):
        if isinstance(key, str):
            continue

        prefix = key[0]
        ids = sorted(ids)
        indices = np.asarray(ids).astype('int')
        prefixed_ids = [f'{prefix}{i}' for i in ids]
        del groups[key]
        if (indices == np.arange(indices.min(), indices.max() + 1)).all():
            groups[prefix] = prefixed_ids
        else:
            groups.update((i, [i]) for i in prefixed_ids)

    for _name, item in sorted(groups.items()):
        yield pd.Series(item)


class CategoryCounter():
    '''
    Count occurences of categorical data across different dimensions.
    '''
    def __init__(self, data, target_name):
        self.data = data
        self.target_name = target_name

        self.feature_names = self.data.columns.difference([self.target_name])
        self.value_categories = np.sort(
            np.unique(
                self.data[self.feature_names].to_numpy().ravel()
            )
        )
        self.is_binary = sorted(self.value_categories) in ([0, 1], [False, True])
        self.feature_type = CategoricalDtype(categories=self.value_categories, ordered=True)
        self.categoric_targets = self.data[self.target_name].astype('category')
        self._array = None
        self._counts = None

    @property
    def array(self):
        '''
        A 3D numpy array containing the counts of each value per feature, value,
        and target.
        '''
        if self._array is None:
            data = self.data

            target_cats = self.categoric_targets.cat.categories

            columns = [
                col.cat.codes
                for (_name, col) in data[self.feature_names].astype(self.feature_type).items()
            ]
            columns.append(self.categoric_targets.cat.codes)
            idx = pd.concat(columns, axis=1).to_numpy()

            val_idx = idx[:, :-1]
            feat_idx = np.arange(val_idx.shape[1])
            targ_idx = idx[:, -1]
            feat_idx, targ_idx = np.meshgrid(feat_idx, targ_idx)
            idx = np.dstack([feat_idx, val_idx, targ_idx]).reshape(-1, 3)

            uniqs, counts = np.unique(idx, axis=0, return_counts=True)

            array = np.zeros(
                (self.feature_names.size, self.value_categories.size, target_cats.size),
                dtype=int
            )
            array[uniqs[:, 0], uniqs[:, 1], uniqs[:, 2]] = counts
            # Subtract the number of common values across target categories to
            # highlight differences.
            axis = 1
            array -= np.expand_dims(array.min(axis=axis), axis=axis)
            self._array = array
        return self._array

    @property
    def counts(self):
        '''
        The dataframe of value counts for the scatterplot.
        '''
        if self._counts is None:
            array = self.array
            target_name = self.target_name

            midx = pd.MultiIndex.from_product(
                [range(s) for s in array.shape],
                names=['feat_idx', 'val_idx', 'targ_idx']
            )
            data = pd.DataFrame({'count': array.flatten()}, index=midx)['count'].unstack(
                level='feat_idx'
            ).swaplevel().reset_index()

            data = pd.melt(data, id_vars=['targ_idx', 'val_idx']) .rename(
                columns={
                    'targ_idx': target_name,
                    'val_idx': 'value',
                    'value': 'count'
                }
            )
            data = data[data['count'] > 0]
            if self.is_binary:
                data = data[data['value'] > 0]

            # Emulate hue separation of stripplot but stagger points along the y
            # axis for better visibility on large fingerprints..
            targets = data[target_name].to_numpy()
            radius = 0.25
            target_range = targets.max() - targets.min()
            y_offsets = (targets / (target_range) - 0.5) * radius
            jitter = np.arange(y_offsets.size) % 5
            jitter = (jitter / jitter.max() - 0.5) * (0.8 * radius / target_range)
            y_offsets += jitter
            data['value'] -= y_offsets

            data[target_name] = self.categoric_targets.cat.categories[data[target_name]]

            self._counts = data

        return self._counts

    def plot(self, ax):  # pylint: disable=invalid-name
        '''
        Plot the counts to the given axis.
        '''
        sns.despine(left=True, bottom=True, ax=ax)
        sns.scatterplot(
            data=self.counts,
            ax=ax,
            x='feat_idx',
            y='value',
            hue=self.target_name,
            size='count',
            alpha=0.25,
            sizes=(0, 250),
            linewidth=0
        )

        n_feat_names = len(self.feature_names)
        xticks = np.linspace(0, n_feat_names - 1, 5).astype(int) \
            if n_feat_names > 10 \
            else range(n_feat_names)
        ax.set_xticks(xticks)
        ax.set_xlabel('index')
        ax.set_title(
            f'Categorical Values By {self.target_name}: '
            f'{self.feature_names[0]} to {self.feature_names[-1]}'
        )

        yticks = range(1 if self.is_binary else 0, len(self.value_categories))
        ax.set_yticks(yticks, [self.value_categories[i] for i in yticks])

        sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))


def plot_numeric_features(ax, data, target_name):  # pylint: disable=invalid-name
    '''
    Args:
        ax:
            The Matplotlib axis on which to plot the features.

        data:
            A dataframe with features and a single target column.

        target_name:
            The name of the target column.
    '''
    feat_mask = data.columns.difference([target_name])
    feat_data = data[feat_mask]
    data[feat_mask] = (feat_data - feat_data.mean()) / feat_data.std()
    data = pd.melt(data, target_name, var_name='feature')
    sns.despine(bottom=True, left=True, ax=ax)
    sns.stripplot(
        data=data,
        ax=ax,
        x='value',
        y='feature',
        hue=target_name,
        dodge=True,
        alpha=0.25,
        zorder=1,
        legend=False
    )
    sns.pointplot(
        data=data,
        ax=ax,
        x='value',
        y='feature',
        hue=target_name,
        dodge=(0.8 - 0.8 / 3.0),
        palette='dark',
        markers='d',
        linestyle='none',
        errorbar=None
    )
    ax.set_title(f'Numeric Features By {target_name}')
    ax.set_xlabel('normalized value')


def group_numeric_and_categoric(calc, features_and_targets):
    '''
    Group feature names by type and category group.

    Args:
        calc:
            A feature calculator instance.

        features_and_targets:
            A FeaturesAndTargets instance.

    Returns:
        A generator over 2-tuples of Pandas series with feature names and a
        boolean to indicate if the names are numeric.
    '''
    # All fully qualfied feature names associated with this feature calculator.
    feat_names = features_and_targets.feature_names[
        features_and_targets.feature_names.str.startswith(calc.add_prefix(''), na=False)
    ]
    num_mask = feat_names.apply(calc.is_numeric)
    num_feat_names = feat_names[num_mask]
    if not num_feat_names.empty:
        yield num_feat_names, True

    cat_feat_names = feat_names[~num_mask]
    for group in group_names_by_prefix(cat_feat_names):
        yield group, False


def _remove_calc_prefixes(calc, names, data):
    '''
    Remove feature calculator prefixes from column names for plotting.

    Args:
        calc:
            A feature calculator instance.

        names:
            The names to deprefix.

        data:
            A dataframe.

    Returns:
        The renamed dataframe.
    '''
    display_names = names.apply(calc.remove_prefix)
    name_map = dict(zip(names, display_names))
    return data.rename(columns=name_map)


def _prepare_subplots(calc, features_and_targets, groups):
    '''
    Prepare data for subplots. This is necessary to calculate the number of
    value categories per category group in order to calculate the height ratios
    of the figure.

    Args:
        calc:
            A feature calculator instance.

        features_and_targets:
            A FeaturesAndTargets instance.

        groups:
            The return value of group_numeric_and_categoric()

    Returns:
        A generator over 5-tuples of row, col, is_numeric, data and a category counter.
    '''
    target_names = features_and_targets.target_names
    ncols = target_names.size

    for row, (names, is_numeric) in enumerate(groups):
        for col in range(ncols):
            target_name = target_names.iloc[col]
            data = features_and_targets.binned_data[[*names, target_name]]
            data = _remove_calc_prefixes(calc, names, data)

            cat_counter = None if is_numeric else CategoryCounter(data, target_name)
            yield row, col, is_numeric, data, cat_counter


def plot_features(path, calc, features_and_targets):
    '''
    Plot features generated by the given feature calculator.

    Args:
        path:
            The output image page.

        calc:
            A feature calculator instance.

        features_and_targets:
            A FeaturesAndTargets instance with the features to plot.
    '''
    groups = list(group_numeric_and_categoric(calc, features_and_targets))
    target_names = features_and_targets.target_names

    if not groups or target_names.empty:
        fig, ax = plt.subplots()  # pylint: disable=invalid-name
        ax.set_axis_off()
        plot_text(ax, 'No features.')

    else:
        ncols = target_names.size

        subplots = list(_prepare_subplots(calc, features_and_targets, groups))

        height_ratios = np.array([
            (data.shape[1] - 1 if is_numeric else len(cat_counter.value_categories))
            for _row, col, is_numeric, data, cat_counter in subplots
            if col == 0
        ], dtype=int)

        fig, axes = plt.subplots(
            nrows=height_ratios.size,
            ncols=ncols,
            squeeze=False,
            figsize=(12 * ncols, (height_ratios + 2).sum()),
            height_ratios=height_ratios
        )
        fig.suptitle(calc.identifier)

        for row, col, is_numeric, data, cat_counter in subplots:
            if is_numeric:
                plot_numeric_features(axes[row][col], data, target_names[col])
            else:
                cat_counter.plot(axes[row][col])

    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches='tight')
