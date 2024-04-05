# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
from random import random
import numpy as np
from ..base import ROCK, PAPER, SCISSORS, RpsAgent


class RandomPlayer(RpsAgent):
    def __init__(self, n_rps=[1, 1, 1]):
        RpsAgent.__init__(self)
        self.n_rps = n_rps

    def predict_agent_gesture(self):
        sum_rps = np.sum(self.n_rps)
        x = random()
        if x < self.n_rps[0] / sum_rps:
            return ROCK
        elif x < (self.n_rps[0] + self.n_rps[1]) / sum_rps:
            return PAPER
        else:
            return SCISSORS

    def load(filename=None):
        assert filename is None
        return RandomPlayer()
