#!/usr/bin/env python3
'''
Hydronaut subclass for creating predictors for molecular properties.
'''

import enum
import logging
import pathlib

import mlflow.artifacts
import pandas as pd
import yaml

from simple_file_lock import MultiFileLock

from chemfeat.database import FeatureDatabase
from chemfeat.features.manager import FeatureManager
from chemfeat.version import VERSION as CHEMFEAT_VERSION
from hydra.utils import to_absolute_path, get_original_cwd
from hydronaut.experiment import Experiment
from hydronaut.hydra.omegaconf import get_container

from molpred.data.common import missing_or_older, tag_path
from molpred.data.column_specifier import ColumnSpecifier
from molpred.data.features_and_targets import FeaturesAndTargets
from molpred.data.inchi_loader import INCHI_COLUMN, InChILoader
from molpred.data.train_test_split import get_train_test_split_paths
from molpred.model.base import get_model_class
from molpred.plot import plot_features
from molpred.version import VERSION as MOLPRED_VERSION

LOGGER = logging.getLogger(__name__)


@enum.unique
class OperationMode(enum.Enum):
    '''
    Operation mode for MolPredExperiment.
    '''
    TRAIN = enum.auto()
    TEST = enum.auto()
    PREDICT = enum.auto()


class MolPredExperiment(Experiment):
    '''
    Predict molecular properties using molecular feature vectors.
    '''

    CHEMFEAT_CONFIG_REL_PATH = 'chemfeat_config.yaml'

    def __init__(self, *args, **kwargs):
        '''
        The configuration object passed through to the parent Experiment class
        should contain the following fields under experiment.params:

            InChILoader:
                A dict containing valid parameters for
                :meth:`molpred.data.inchi_loader.InChILoader.__init__`.

            model:
                A dict containing requirement parameters for ModelBase. See the
                ModelBase documentation for details.

        Args:
            `*args`, `**kwargs`:
                Positional and keyword arguments passed through to the parent
                class.
        '''
        super().__init__(*args, **kwargs)

        self._orig_dir = pathlib.Path(get_original_cwd()).resolve()

        data_dir = self.config.experiment.params.get('data_dir', 'data')
        self.data_dir = pathlib.Path(to_absolute_path(data_dir)).resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.feat_man = None
        self._paths = {}
        self._column_specifier = None

        self._inchi_loader = None
        self._model = None

        LOGGER.info('ChemFeat version: %s', CHEMFEAT_VERSION)
        LOGGER.info('MolPred version: %s', MOLPRED_VERSION)

    @property
    def inchi_loader(self):
        '''
        Set the input data loader.
        '''
        if self._inchi_loader is None:
            params = self.config.experiment.params
            loader_params = get_container(params, 'InChILoader', default={}, resolve=True)
            loader_params['path'] = to_absolute_path(loader_params['path'])
            inchi_loader = InChILoader(**loader_params)
            self.log_path_param('input', inchi_loader.path)
            LOGGER.info('Input data: %s', inchi_loader.path)
            self._inchi_loader = inchi_loader
        return self._inchi_loader

    @property
    def model_cls(self):
        '''
        The configured model class.
        '''
        model_params = self.config.experiment.params.model
        return get_model_class(model_params.name)

    @property
    def model(self):
        '''
        The model.
        '''
        if self._model is None:
            self._model = self.model_cls(self)
        return self._model

    @property
    def model_rel_path(self):
        '''
        The relative path of the model for logging and reloading training models.
        '''
        return self.model_cls.with_model_file_ext('model')

    def log_path_param(self, name, path):
        '''
        Log a path as a parameter. Paths within the original working directory
        will be logged as relative paths.

        Args:
            name:
                The name under which to log the path. It will appear as an
                MLflow parameter with the prefix "path/".

            path:
                The path to log.
        '''
        path = pathlib.Path(to_absolute_path(str(path))).resolve()
        if path.is_relative_to(self._orig_dir):
            path = path.relative_to(self._orig_dir)
        self._paths[name] = path
        self.log_param(f'path/{name}', str(path))

    def get_path(self, name):
        '''
        Retrieve the value of a path logged with log_path_param.

        Args:
            name:
                The name under which the path was logged.

        Returns:
            The corresponding path, or None if the name has not been logged.
        '''
        path = self._paths.get(name)
        if not path:
            LOGGER.error('No path logged under the name "%s"', name)
            return None

        if not path.is_absolute():
            path = pathlib.Path(to_absolute_path(str(path)))
        return path

    @property
    def mode(self):
        '''
        The current operation mode.
        '''
        mode = self.config.experiment.params.get('mode', 'train').upper()
        try:
            return OperationMode[mode]
        except KeyError as err:
            choices = ', '.join(m.name for m in OperationMode)
            raise ValueError(
                f'Invalid mode specified [{mode}]: must be one of {choices}'
            ) from err

    @property
    def data_name(self):
        '''
        A name for generated files based on the input data path.
        '''
        return self.inchi_loader.path.stem

    @property
    def features_path(self):
        '''
        The path to the CSV features file.
        '''
        return self.data_dir / (
            f'{self.data_name}-features-{self.feat_man.feature_set_string}.csv'
        )

    def prepare_features(self):
        '''
        Prepare the features for the input data.

        Returns:
            The path to the features CSV file.
        '''
        LOGGER.info('Preparing molecular features')
        params = self.config.experiment.params
        features = get_container(params, 'chemfeat_features', default=[], resolve=True)
        self.log_dict(features, self.CHEMFEAT_CONFIG_REL_PATH)

        feat_db = FeatureDatabase(self.data_dir / 'features.sqlite')
        self.log_path_param('features_database', feat_db.path)

        self.feat_man = FeatureManager(
            feat_db,
            features,
            inchi_to_mol=params.get('inchi_to_mol')
        )
        self.log_dict(list(self.feat_man.get_feature_parameters()), 'data/feature_sets.yaml')
        feat_path = self.features_path

        if missing_or_older([feat_path], [feat_db.path, self.inchi_loader.path]):
            features = self.feat_man.calculate_features(
                self.inchi_loader.inchis,
                return_dataframe=True,
                n_jobs=params.get('n_jobs', -1)
            )
            features = self.inchi_loader.join(features)
            features.to_csv(feat_path, index=False)
        else:
            features = pd.read_csv(feat_path, nrows=1)

        self._set_column_specifier(features)
        self.log_path_param('feature_data', feat_path)

    def _set_column_specifier(self, features):
        '''
        Set the internal features and targets column specifier.
        '''
        # All features including those loaded from the input data.
        feature_names = features.columns.drop(
            labels=[
                INCHI_COLUMN,
                *self.inchi_loader.column_specifier.targets
            ]
        )

        # Features from input data, not from chemfeat.
        not_chem_feat = feature_names.isin(
            self.inchi_loader.column_specifier.features_and_targets
        )

        # Mask for all numeric features.
        num_feat_mask = pd.Series([False] * feature_names.size)
        num_feat_mask[not_chem_feat] = num_feat_mask[not_chem_feat].isin(
            self.inchi_loader.column_specifier.numeric_names
        )

        # Features from chemfeat, not from input data.
        chem_feat = ~not_chem_feat
        num_feat_mask[chem_feat] = self.feat_man.numeric_mask(feature_names[chem_feat])

        self._column_specifier = ColumnSpecifier(
            num_feats=feature_names[num_feat_mask],
            cat_feats=feature_names[~num_feat_mask],
            num_targets=self.inchi_loader.column_specifier.numeric_targets,
            cat_targets=self.inchi_loader.column_specifier.categoric_targets
        )

    def load_features_and_targets(self, name):
        '''
        Load the feature and target data from the given path.

        Args:
            name:
                The name of a path registered with log_path_param().

        Returns:
            The feature and target dataframes.
        '''
        return FeaturesAndTargets(
            self.get_path(name),
            self._column_specifier,
            column_bins=get_container(self.config.experiment.params, 'column_bins')
        )

    @property
    def numeric_feature_names(self):
        '''
        The numeric feature names.
        '''
        return self._column_specifier.numeric_features

    @property
    def categoric_feature_names(self):
        '''
        The categoric feature names.
        '''
        return self._column_specifier.categoric_features

    def _plot_feature_paths_and_calcs(self, name):
        '''
        Iterate over 2-tuples of feature plot image paths and corresponding
        feature calculators.
        '''
        path = self.get_path(name)
        for identifier, feat_calc in self.feat_man.feature_calculators.items():
            img_path = tag_path(path, f'-plot-{identifier}', suffix='.png')
            yield img_path, feat_calc

    def plot_features(self, name):
        '''
        Plot features.

        Args:
            name:
                The name of a logged path containing features.
        '''
        path = self.get_path(name)
        paths_and_feat_calcs = dict(self._plot_feature_paths_and_calcs(name))

        with MultiFileLock([path, *paths_and_feat_calcs.keys()]):
            if missing_or_older(paths_and_feat_calcs.keys(), [path]):
                LOGGER.info('Plotting feature data: %s', name)
                features_and_targets = self.load_features_and_targets(name)
                # TODO
                # Maybe parallelize.
                for path, calc in paths_and_feat_calcs.items():
                    plot_features(path, calc, features_and_targets)

        for path, _calc in paths_and_feat_calcs.items():
            self.log_artifact(path, 'img')

    def _maybe_reload_artifacts(self):
        '''
        Retrieve artifacts from a previous run and update the current run's
        configuration to re-use the Chemfeat configuration and trained model
        from the previous one. This is only done in non-TRAIN modes.
        '''
        if self.mode is not OperationMode.TRAIN:
            run_id = self.config.experiment.params.mlflow_run_id
            LOGGER.info('Retrieving artifacts from previous MLflow run: %s', run_id)

            # Retrieve the model and update the model path so that it is
            # reloaded when the model is instantiated.
            model_path = str(self.model_rel_path)
            model_path = mlflow.artifacts.download_artifacts(
                run_id=run_id,
                artifact_path=model_path,
                dst_path=model_path
            )
            self.config.experiment.params.model.path = model_path

            # Retrieve the Chemfeat feature configuration and re-use it.
            chemfeat_config_path = self.CHEMFEAT_CONFIG_REL_PATH
            chemfeat_config_path = mlflow.artifacts.download_artifacts(
                run_id=run_id,
                artifact_path=chemfeat_config_path,
                dst_path=chemfeat_config_path
            )
            with pathlib.Path(chemfeat_config_path).open('rb') as handle:
                self.config.experiment.params.chemfeat_features = yaml.safe_load(handle)

    def setup(self):
        '''
        Prepare the input files.
        '''
        self._maybe_reload_artifacts()

        LOGGER.info('Preparing data')
        params = self.config.experiment.params
        self.prepare_features()
        features_and_targets = self.load_features_and_targets('feature_data')

        plottable_features = []
        mode = self.mode
        if mode is OperationMode.TRAIN:
            LOGGER.info('Creating train and test data sets')
            train_path, test_path = get_train_test_split_paths(
                features_and_targets,
                **get_container(params, 'train_test_split', default={}, resolve=True)
            )
            self.log_path_param('train_data', train_path)
            self.log_path_param('test_data', test_path)
            plottable_features = ['feature_data', 'train_data', 'test_data']

        else:
            self.log_path_param('test_data', features_and_targets.path)
            plottable_features = ['test_data']

        if self.config.experiment.params.get('plot_features', False):
            for name in plottable_features:
                self.plot_features(name)

        self.model.visualize_data()

    def __call__(self):
        mode = self.mode
        model = self.model

        if mode is OperationMode.TRAIN:
            train_score = model.train(
                *self.load_features_and_targets('train_data').features_and_targets
            )
            self.log_metric('train_score', train_score)
            # Save the model. This may be redundant when autologging is enabled
            # but this ensures a consistent location for reloading models from
            # artifacts.
            model_path = model.with_model_file_ext('model')
            model.save(model_path)
            self.log_artifact(model_path)

        features, targets = self.load_features_and_targets('test_data').features_and_targets

        if mode in (OperationMode.TRAIN, OperationMode.TEST):
            model.score_predictions(features, targets)
            model.visualize_prediction_metrics(features, targets)

            names = get_container(
                self.config.experiment.params,
                'objective_values',
                default=[]
            )
            if not names:
                LOGGER.error('No objective values specified, returning 0')
                return 0

            runner = self.mlflow_runner
            values = tuple(runner.get_metric(name) for name in names)
            if len(values) > 1:
                return values
            return values[0]

        # Prediction
        pred_path = 'prediction.csv'
        columns = [self.inchi_loader.inchis]
        if self.inchi_loader.column_specifier.extra:
            columns.append(self.inchi_loader[self.inchi_loader.column_specifier.extra])
        columns.extend([
            model.predict(features),
            model.predict_proba(features)
        ])
        columns = (col.reset_index(drop=True) for col in columns)
        pd.concat(columns, axis=1).to_csv(pred_path, index=False)
        self.log_artifact(pred_path)
        return 0
