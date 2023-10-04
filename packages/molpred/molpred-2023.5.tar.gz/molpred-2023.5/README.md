---
title: README
author: Jan-Michael Rye
---

![MolPred logo](https://gitlab.inria.fr/jrye/molpred/-/raw/main/img/molpred_logo.svg)

# Synopsis

MolPred is a [Hydronaut](https://gitlab.inria.fr/jrye/hydronaut)-based framework for building machine- and deep-learning predictors for molecular characteristics using [Chemfeat](https://gitlab.inria.fr/jrye/chemfeat). It has the advantages of both along with several others:

* All hyperparameters are managed via YAML configuration files, including selection of user-supplied models, molecular feature sets and metrics, with full support for command-line overrides.
* Hyperparameters can be explored using systematic sweeps or optimizing algorithms. In particular, optimization can be tracked in real time with [Optuna Dashboard](https://optuna-dashboard.readthedocs.io/en/latest/) when using [Hydra's Optuna sweeper plugin](https://hydra.cc/docs/plugins/optuna_sweeper/).
* All parameters, metrics, models and other artifacts are tracked with MLflow.
* Tests and predictions can be performed by retrieving models and feature-set configurations from previous MLflow runs.
* Models can be easily added by registering user-supplied subclasses of a provided class. Registered classes can be selected by name from the configuration file.
* Custom metrics can also be define and registered for selection from the configuration file.
* New chemical/molecular feature-set calculators can be added and registered via simple subclasses.
* Feature calculations are cached in a local database to avoid redundant calculations.
* Numeric and categoric features are automatically plotted and further optional plots are supported via the model subclasses. These plots are automatically logged as MLflow artifacts.



# Links

* [Source code](https://gitlab.inria.fr/jrye/molpred)
* [Documentation](https://jrye.gitlabpages.inria.fr/molpred/)
* [Python Package](https://pypi.org/project/molpred/)
* [Hydronaut](https://gitlab.inria.fr/jrye/hydronaut)
* [Chemfeat](https://gitlab.inria.fr/jrye/chemfeat)



# Usage

The framework can train user-supplied models to predict features of molecules. To train a model, the user should provide a set of [International Chemical Identifiers (InChIs)](https://en.wikipedia.org/wiki/International_Chemical_Identifier) representing the molecules of the training set along with one or more features associated with these molecules. The user should then customize the [example configuration file](https://gitlab.inria.fr/jrye/molpred/-/blob/main/conf/config.yaml) to select their model and chemical feature sets.

All results are logged with MLflow and any trained model can be re-used for testing or prediction by altering the configuration file to set the operation mode (train, test or predict) and a previous MLflow run ID for reloading the model and feature set.

## Model

To create a model, the user must define a subclass of [molpred.model.base.ModelBase](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.base.ModelBase). Some methods such as [train](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.base.ModelBase.train) and [predict](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.base.ModelBase.predict) are required while others such as [visualize_data](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.base.ModelBase.visualize_data) and [visualize_prediction_metrics](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.base.ModelBase.visualize_prediction_metrics) are optional.

Once the model has been defined, it can be registered using the class's [register](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.base.ModelBase.register) method and then selected by name from the configuration file (`experiment.params.model.name`).

### Examples

* [A model to predict of a molecule will pass the blood-brain barrier (BBB)](https://gitlab.inria.fr/aistrosight/bbb-permeability-prediction/-/blob/main/src/bpp/models/model_sklearn_hgbc.py). Internally the model uses [sklearn.ensemble.HistGradientBoostingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html).


## Scoring

[molpred.model.scoring.register_scorer](https://jrye.gitlabpages.inria.fr/molpred/molpred.model.html#molpred.model.scoring.register_scorer) can be used to register custom [scikit-learn scorers created with make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html). These scorers can then be used by name in the configuration file (`experiment.params.model.scorers`) to calculate and log metrics for the model during training and testing.



# Visualization

All features calculated by Chemfeat are automatically plotted and logged for each run to provide insights into the correlation between the features and the target characteristics.

## Numeric Features

All numeric features for a feature set are plotted together using a [Seaborn stripplot](https://seaborn.pydata.org/generated/seaborn.stripplot.html) after normalization.

![Example of numeric feature plot](https://gitlab.inria.fr/jrye/molpred/-/raw/main/img/numeric_plot.png "Numeric Feature Plot")

## Categoric Features

Categoric features with common prefixes that only vary by a numeric suffix are grouped together and displayed as differential counts of each categoric value per target category. The data is displayed using a customized scatterplot that can visually separate data even for fingerprint features of up to 4096 bits. These plots attempt to highlight the indices of features that significantly vary per target category.

![Example of categoric feature plot](https://gitlab.inria.fr/jrye/molpred/-/raw/main/img/categoric_plot.png "Categoric Feature Plot")

