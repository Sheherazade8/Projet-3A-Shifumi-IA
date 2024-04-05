# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
from warnings import warn

import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model \
    import SGDClassifier, PassiveAggressiveClassifier, Perceptron
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier

from ...base import RpsAgent, ROCK, PAPER, SCISSORS, get_game_features
from ..random_player import RandomPlayer
from .utils import get_gesture_with_best_gain_expectation


class SklearnAgent(RpsAgent, BaseEstimator, ClassifierMixin):
    def __init__(self, feature_size=3):
        RpsAgent.__init__(self)
        self.feature_size = feature_size

    def record(self, last_round):
        if len(self.game) >= self.feature_size:
            X = get_game_features(self.game[-self.feature_size:])
            X = X.reshape((1, -1))
            y = np.array([last_round.opponent])
            self.partial_fit(X, y,
                             classes=np.array([ROCK, PAPER, SCISSORS]))
        RpsAgent.record(self, last_round)

    def predict_agent_gesture(self):
        if len(self.game) >= self.feature_size+1:
            X = get_game_features(self.game[-self.feature_size:])
            X = X.reshape((1, -1))
            if hasattr(self, 'predict_proba'):
                y = self.predict_proba(X)
                p_rps = {
                    str(ROCK): y[0, 0],
                    str(PAPER): y[0, 1],
                    str(SCISSORS): y[0, 2],
                }
            else:
                # TODO rename predict_agent_gesture method in API in order to avoid
                # conflict with sklearn (e.g. predict_opponent_gesture)
                y = self.predict(X)
                p_rps = {
                    str(ROCK): 0,
                    str(PAPER): 0,
                    str(SCISSORS): 0,
                }
                if y == 0:
                    p_rps[str(ROCK)] = 1
                elif y == 1:
                    p_rps[str(PAPER)] = 1
                else:
                    p_rps[str(SCISSORS)] = 1
            return get_gesture_with_best_gain_expectation(p_rps)
        else:
            rp = RandomPlayer()
            return rp.predict_agent_gesture()

class MultinomialNBAgent(SklearnAgent, MultinomialNB):
    """
    Online learning agent based on sklearn.naive_bayes.MultinomialNB

    Parameters
    ----------
    feature_size : int
        Number of rounds to be considered in feature vectors
    alpha : float
        Additive (Laplace/Lidstone) smoothing parameter
        (0 for no smoothing). See documentation of
        `sklearn.naive_bayes.MultinomialNB`
    fit_prior : boolean
        Whether to learn class prior probabilities or not. If false,
        a uniform prior will be used. See documentation of
        `sklearn.naive_bayes.MultinomialNB`
    """
    def __init__(self, alpha=1., feature_size=3, fit_prior=True):
        SklearnAgent.__init__(self, feature_size=feature_size)
        MultinomialNB.__init__(self, alpha=alpha, fit_prior=fit_prior)

    @staticmethod
    def load():
        return MultinomialNBAgent()


class SgdSvmAgent(SklearnAgent, SGDClassifier):
    """
    Online learning agent based on sklearn.linear_model.SGDClassifier with
    hinge loss (SVM)

    Parameters
    ----------
    feature_size : int
        Number of rounds to be considered in feature vectors
    """
    def __init__(self, feature_size=3):
        SklearnAgent.__init__(self, feature_size=feature_size)
        SGDClassifier.__init__(self, loss='hinge')

    @staticmethod
    def load():
        return SgdSvmAgent()


class SgdLogRegAgent(SklearnAgent, SGDClassifier):
    """
    Online learning agent based on sklearn.linear_model.SGDClassifier with
    log loss (logistic regression)

    Parameters
    ----------
    feature_size : int
        Number of rounds to be considered in feature vectors
    """
    def __init__(self, feature_size=3):
        SklearnAgent.__init__(self, feature_size=feature_size)
        SGDClassifier.__init__(self, loss='log')

    @staticmethod
    def load():
        return SgdLogRegAgent()


class PerceptronAgent(SklearnAgent, Perceptron):
    """
    Online learning agent based on sklearn.linear_model.Perceptron

    Parameters
    ----------
    feature_size : int
        Number of rounds to be considered in feature vectors
    """
    def __init__(self, feature_size=3):
        SklearnAgent.__init__(self, feature_size=feature_size)
        Perceptron.__init__(self)

    @staticmethod
    def load():
        return PerceptronAgent()


class PassiveAggressiveClassifierAgent(SklearnAgent,
                                       PassiveAggressiveClassifier):
    """
    Online learning agent based on sklearn.linear_model.PassiveAggressiveClassifier

    Parameters
    ----------
    feature_size : int
        Number of rounds to be considered in feature vectors
    """
    def __init__(self, feature_size=3):
        SklearnAgent.__init__(self, feature_size=feature_size)
        PassiveAggressiveClassifier.__init__(self)

    @staticmethod
    def load():
        return PassiveAggressiveClassifierAgent()


class MLPClassifierAgent(SklearnAgent, MLPClassifier):
    """
    Online learning agent based on sklearn.neural_networks.MLPClassifier

    Parameters
    ----------
    feature_size : int
        Number of rounds to be considered in feature vectors
    """
    def __init__(self, feature_size=3):
        SklearnAgent.__init__(self, feature_size=feature_size)
        MLPClassifier.__init__(self)

    @staticmethod
    def load():
        return MLPClassifierAgent()
