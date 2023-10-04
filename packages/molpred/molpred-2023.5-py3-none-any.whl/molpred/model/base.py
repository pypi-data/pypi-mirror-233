#!/usr/bin/env python3
'''
Base class for other models.
'''

import enum
import logging
import pathlib

from hydronaut.hydra.omegaconf import get, get_container
from chemfeat.modules import import_modules

from molpred.decorators import caching_method, caching_class
from molpred.model.scoring import get_scorer

LOGGER = logging.getLogger(__name__)


# Dict mapping model names to subclasses of ModelBase.
# It is populated by modules that define these subclasses and call their
# register method when they are dynamically loaded
MODEL_CLASSES = {}


def import_models(paths):
    '''
    Import the ModelBase subclasses.

    Args:
        paths:
            An list of paths to external modules with ModelBase subclasses. The
            register method of each ModelBase subclass should be called by the
            module after the subclass is defined to register the model globally.

            File paths will import single modules while directory paths will
            recursively import all modules contained in the directory.
    '''
    import_modules(
        paths,
        path_log_msg='Model import path: %s'
    )


def get_model_class(name):
    '''
    Get the model class registered under the given name.

    Args:
        name:
            The registered name of the model class to return.

    Returns:
        A subclass of ModelBase.

    Raises:
        ValueError:
            The name is not registered.
    '''
    try:
        return MODEL_CLASSES[name]
    except KeyError as err:
        raise ValueError(f'The model name "{name}" is not registered.') from err


@enum.unique
class ModelType(enum.Enum):
    '''
    Model types for determining which common data and metric visualizations to
    use.
    '''
    OTHER = enum.auto()
    CLASSIFIER = enum.auto()
    BINARY_CLASSIFIER = enum.auto()
    REGRESSOR = enum.auto()


@caching_class
class ModelBase():
    '''
    Base class for other models.
    '''

    # The file extension for the saved model file.
    MODEL_EXT = '.pkl'

    def __init__(self, experiment):
        '''
        Args:
            experiment:
                The MolPredExperiment instance that is using this model. It
                should be a subclass of hydronaut.experiment.Experiment and the
                contained OmegaConf configuration object should contain a dict
                under experiment.params.model with the following fields:

                    name:
                        The registered name of the model to use.

                    parameters:
                        Arbitrary model-specific parameters.

                    path:
                        The path to a saved model that should be reloaded.

                    scorers:
                        A list of registered scorer names to use when logging
                        metrics. The first will be used as the main test score

                    image_subdirectory:
                        The subdirectory under which to log images with MLflow.

                Additional fields may also be specified, such as values for
                cross-validation. Subclasses should specify which additional
                fields they support.
        '''
        self.experiment = experiment
        path = self.experiment.config.experiment.params.model.get('path')
        if path is None:
            self.initialize()
        else:
            self.load(path)

    @classmethod
    def register(cls, name=None):
        '''
        Register a subclass of ModelBase in the global model register.
        '''
        if name is None:
            name = cls.__name__
        old_cls = MODEL_CLASSES.get(name)
        if old_cls:
            LOGGER.warning(
                'Re-registering model "%s": %s -> %s',
                name,
                MODEL_CLASSES[name],
                cls
            )
        else:
            LOGGER.debug('Registering model "%s": %s', name, cls)
        MODEL_CLASSES[name] = cls

    def config_get(self, name, default=None):
        '''
        Convenience method for retrieving configuration values from
        self.experiment.config.experiment.params.model.

        Args:
            name:
                A field name. It may contain a "." if there are nested values in
                the model configuration (e.g. "foo.bar").

            default:
                The default value to return if the requested name is not found.

        Returns:
            The requested value or the default if the value was not found.
        '''
        return get(
            self.experiment.config.experiment.params.model,
            name,
            default=default
        )

    def config_get_container(self, name, default=None):
        '''
        Similar to config_get but returns a Python container (e.g. a dict) when
        a nested OmegaConf configuration object is found.

        Accepts the same arguments as config_get and returns the requested value
        if found else the provided default.
        '''
        return get_container(
            self.experiment.config.experiment.params.model,
            name,
            default=default,
            resolve=True
        )

    def param_get(self, name, default=None):
        '''
        A wrapper around config_get for retrieving entries under
        self.experiment.config.experiment.params.model.params.
        '''
        return self.config_get(f'params.{name}', default=default)

    def param_get_container(self, name, default=None):
        '''
        A wrapper around config_get_container for retrieving entries under
        self.experiment.config.experiment.params.model.params.
        '''
        return self.config_get_container(f'params.{name}', default=default)

    @property
    def image_subdirectory(self):
        '''
        The subdirectory under which to log image artifacts with MLflow.
        '''
        img_dir = pathlib.Path(self.config_get('image_subdirectory', 'img').strip('/'))
        if img_dir.is_absolute():
            rel_img_dir = img_dir.relative_to(img_dir.anchor)
            LOGGER.warning(
                'Converting absolute image_subdirectory %s to %s',
                img_dir,
                rel_img_dir
            )
            img_dir = rel_img_dir
        return img_dir

    def initialize(self):
        '''
        Initialize a new model and store it in this object's "model" attribute.
        '''
        raise NotImplementedError('initialize method is not implemented')

    @classmethod
    def with_model_file_ext(cls, path):
        '''
        Ensure that a path has the correct extension for a model file.
        '''
        path = pathlib.Path(path)
        return path.with_suffix(cls.MODEL_EXT)

    def load(self, path):
        '''
        Load a model from a file and store it in this object's "model"
        attribute.

        Args:
            path:
                The path to the model to load.
        '''
        raise NotImplementedError('load method is not implemented')

    def save(self, path):
        '''
        Save a model to a file.

        Args:
            path:
                The path to which to save the model. 
        '''

    def train(self, data, targets):
        '''
        Train the model.

        Args:
            data:
                The training data as a Pandas Dataframe.

            targets:
                The training targets as a Pandas DataFrame. How many columns
                there are depends on the configuration of the input data loader.

        Returns:
            A training score.
        '''
        raise NotImplementedError('train method is not implemented')

    @caching_method
    def predict(self, data):
        '''
        Make a prediction with the model.

        The method should be decorated with @caching_method.

        Args:
            data:
                The input data.

        Returns:
            The predictions as a Pandas series.
        '''
        raise NotImplementedError('predict method is not implemented')

    @caching_method
    def predict_proba(self, data):
        '''
        Emulate the predict_proba method of sklearn estimators:
        https://scikit-learn.org/stable/search.html?q=predict_proba

        The method should be decorated with @caching_method.

        Args:
            data:
                The input data.

        Returns:
            The prediction probabilities as a Pandas dataframe.
        '''
        raise NotImplementedError('predict_proba method is not implemented')

    def score_predictions(self, data, targets, prefix=''):
        '''
        Score a prediction by comparing it to the target. The resulting scores
        are logged with MLflow.

        Args:
            data:
                The input data as a Pandas Dataframe.

            targets:
                The target (true) values as a Pandas DataFrame. How many columns
                there are depends on the configuration of the input data loader.

            prefix:
                A prefix to use when logging the different scores as metrics.
                The name of each metric will be the prefix prepended to the name
                of the scorer. The scorers are configured via the configuration
                file as detailed in the __init__ method.
        '''
        exp = self.experiment
        for name in self.config_get_container('scorers', default=[]):
            scorer = get_scorer(name)
            score = scorer(self, data, targets)
            exp.log_metric(f'{prefix}{name}', score)

    def visualize_data(self):
        '''
        Visualize input data and the train-test split. The raw input data is
        accessible via self.inchi_loader, the full feature data via the logged
        'feature_data' path, and the train and test data via the logged
        'train_data' and 'test_data' paths.

        Depending on settings in the configuration file. this data may be
        plotted automatically by the parent experiment class. This method should
        be used for custom input data plotting.
        '''

    def visualize_prediction_metrics(self, data, target):
        '''
        Visualize the prediction's performance using model-appropriate figures
        such as confusion matrices. The figures are logged with MLflow.

        Args:
            data:
                The input data.

            target:
                The target (true) values.

            subdir:
                The artifact subdirectory under which to log the images with
                MLflow.
        '''
