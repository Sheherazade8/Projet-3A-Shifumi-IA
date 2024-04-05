# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Mathias Aloui
inspired by Michael B. Jordan : An actuarial artificial intelligence for the game
rock-paper-scissors
"""
import numpy as np
from ..base import ROCK, PAPER, SCISSORS, RpsAgent
from .pst_player.defs import beats

class ActuarialPlayer(RpsAgent):

    def __init__(self, c = 50, f = 5, scale = 10):
        RpsAgent.__init__(self)
        self.repeatStyleWin  = 0
        self.repeatStyleLose = 0
        self.repeatStyleDraw = 0
        self.alterStyleWin   = 0
        self.alterStyleLose  = 0
        self.alterStyleDraw  = 0
        self.confidence  = c/100
        self.forgetLimit = f
        self.scale = scale/100
        self.lastpredict_go = None

    def record(self, last_round):
        if len(self.game) > 1:
            go = self.game[-1].opponent
            result = self.game[-1].get_opponent_gain()
            if result == 1:
                if go == last_round.opponent:
                    if self.repeatStyleWin < self.alterStyleWin + self.forgetLimit:
                        self.repeatStyleWin += 1
                else:
                    if self.alterStyleWin < self.repeatStyleWin + self.forgetLimit:
                        self.alterStyleWin += 1
            elif result == 0:
                if go == last_round.opponent:
                    if self.repeatStyleDraw < self.alterStyleDraw + self.forgetLimit:
                        self.repeatStyleDraw += 1
                else:
                    if self.alterStyleDraw < self.repeatStyleDraw + self.forgetLimit:
                        self.alterStyleDraw += 1
            else:
                if go == last_round.opponent:
                    if self.repeatStyleLose < self.alterStyleLose + self.forgetLimit:
                        self.repeatStyleLose += 1
                else:
                    if self.alterStyleLose < self.repeatStyleLose + self.forgetLimit:
                        self.alterStyleLose += 1
            if self.lastpredict_go == last_round.opponent:
                if self.confidence < (100-self.scale):
                    self.confidence += self.scale
                else:
                    if self.confidence > self.scale:
                        self.confidence -= self.scale
        super().record(last_round)

    def predict_agent_gesture(self):
        proba = {ROCK : 1/3, PAPER : 1/3, SCISSORS : 1/3}
        value = np.random.random()
        if len(self.game) > 0:
            result = self.game[-1].get_opponent_gain()
            go = self.game[-1].opponent
            if result == 1:
                if self.repeatStyleWin > self.alterStyleWin:
                    proba[beats[go]] +=  2/3 * self.confidence
                    proba[beats[beats[go]]] -= 2/3 * self.confidence
                elif self.alterStyleWin > self.repeatStyleWin:
                    proba[beats[go]] -= 2/3 * self.confidence
                    proba[beats[beats[go]]] += 2/3 * self.confidence
            elif result == 0:
                if self.repeatStyleDraw > self.alterStyleDraw:
                    proba[beats[go]] += 2/3 * self.confidence
                    proba[beats[beats[go]]] -= 2/3 * self.confidence
                if self.alterStyleDraw > self.repeatStyleDraw:
                    proba[beats[go]] -= 2/3 * self.confidence
                    proba[beats[beats[go]]] += 2/3 * self.confidence
            else:
                if self.repeatStyleLose > self.alterStyleLose:
                    proba[beats[go]] += 2/3 * self.confidence
                    proba[beats[beats[go]]] -= 2/3 * self.confidence
                if self.alterStyleLose > self.repeatStyleLose:
                    proba[beats[go]] -= 2/3 * self.confidence
                    proba[beats[beats[go]]] += 2/3 * self.confidence
        print(proba)
        if proba[ROCK] == proba[PAPER] == proba[SCISSORS]:
            self.old_go = None
        elif proba[ROCK] > max(proba[PAPER],proba[SCISSORS]):
            self.old_go = ROCK
        elif proba[PAPER] > max(proba[ROCK],proba[SCISSORS]):
            self.old_go = PAPER
        else:
            self.old_go = SCISSORS
        if value < proba[ROCK]:
            return ROCK
        if value < proba[ROCK] + proba[PAPER]:
            return PAPER
        return SCISSORS

    def load(filename=None):
        assert filename is None
        return ActuarialPlayer()
