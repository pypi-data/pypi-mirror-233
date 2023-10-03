#!/usr/bin/env python3
'''
Score models.
'''

import logging

from sklearn.metrics import get_scorer as sm_get_scorer

LOGGER = logging.getLogger(__name__)


# Map scorer names to sklearn scorer objects.
SCORERS = {}


def register_scorer(name, scorer):
    '''
    Register a scorer under the given name.

    Args:
        name:
            The name under which to register the scorer.

        scorer:
            The scorer created with sklearn.metrics.make_scorer.
    '''
    prev_scorer = SCORERS.get(name)
    if prev_scorer is None:
        LOGGER.debug('Registering scorer %s: %s', name, scorer)
    else:
        LOGGER.warning('Reregistering scorer %s: %s -> %s', name, prev_scorer, scorer)
    SCORERS[name] = scorer


def get_scorer(name):
    '''
    Get a registered scorer.

    Args:
        name:
            The name under which the scorer was registered.

    Returns:
        The scorer registered under the given name, or the name itself if the
        name has not been registered. This behavior enables names to be passed
        through to sklearn instead of an actual scorer object.
    '''
    try:
        return SCORERS[name]
    except KeyError:
        return sm_get_scorer(name)
