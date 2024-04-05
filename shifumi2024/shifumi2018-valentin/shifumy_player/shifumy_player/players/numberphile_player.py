# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Mathias Aloui
"""
from random import randint
from ..base import ROCK, PAPER, SCISSORS, RpsAgent
from .pst_player.defs import beats

class NumberphilePlayer(RpsAgent):

    def __init__(self):
        RpsAgent.__init__(self)

    def predict_agent_gesture(self):
        if len(self.game) == 0:
            return SCISSORS
        go = self.game[-1].opponent
        ga = self.game[-1].agent
        if ga == beats[go]:
            return go
        if go == beats[ga]:
            return beats[go]
        gestures = [ROCK, PAPER, SCISSORS]
        return gestures[randint(0, 2)]
        
    def load(filename=None):
        assert filename is None
        return NumberphilePlayer()
