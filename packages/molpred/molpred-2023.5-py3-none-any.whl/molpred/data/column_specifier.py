#!/usr/bin/env python3

'''
Convenience class for working with feature and target columns.
'''


def _as_set(items):
    '''
    Convert an iterable to a set.

    Args:
        items:
            An iterable or None.

    Returns:
        The set of the input items. If None then an empty set it returned.
    '''
    return set(items) if items is not None else set()


class ColumnSpecifier():
    '''
    Specify numeric and categoric feature and target column names.
    '''
    def __init__(
        self,
        num_feats=None,
        cat_feats=None,
        num_targets=None,
        cat_targets=None,
        extra=None,
    ):
        '''
        Args:
            num_feats:
                An iterable of numeric feature names.

            cat_feats:
                An iterable of categoric feature names.

            num_targets:
                An iterable of numeric target names.

            cat_targets:
                An iterable of categoric target names.

            extra:
                Extra columns that will be passed through to output files.
        '''
        self.numeric_features = _as_set(num_feats)
        self.categoric_features = _as_set(cat_feats)
        self.numeric_targets = _as_set(num_targets)
        self.categoric_targets = _as_set(cat_targets)
        self.extra = _as_set(extra)

    @property
    def numeric_names(self):
        '''
        The set of all numeric names.
        '''
        return self.numeric_features | self.numeric_targets

    @property
    def categoric_names(self):
        '''
        The set of all categoric names.
        '''
        return self.categoric_features | self.categoric_targets

    @property
    def features(self):
        '''
        The set of feature names.
        '''
        return self.numeric_features | self.categoric_features

    @property
    def targets(self):
        '''
        The set of target names.
        '''
        return self.numeric_targets | self.categoric_targets

    @property
    def features_and_targets(self):
        '''
        The set of all feature and target names.
        '''
        return self.features | self.targets

    @property
    def names(self):
        '''
        The set of all feature, target and extra names.
        '''
        return self.features_and_targets | self.extra

    def is_numeric(self, name):
        '''
        True if the given name is one of the numeric features or targets.
        '''
        return name in self.numeric_names

    def is_categoric(self, name):
        '''
        True if the name is one of the categoric features or targets.
        '''
        return name in self.categoric_names

    def is_feature(self, name):
        '''
        True if the name is a feature.
        '''
        return name in self.features

    def is_target(self, name):
        '''
        True if the name is a target.
        '''
        return name in self.targets
