# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Mathias Aloui
"""
import numpy as np
from ..base import ROCK, PAPER, SCISSORS, RpsAgent
from .pst_player.defs import beats

class StrategoPlayer(RpsAgent):

    def __init__(self, c = 40, f = 2, scale = 20):
        RpsAgent.__init__(self)
        self.repeatWin  = 0
        self.repeatLose = 0
        self.repeatDraw = 0
        self.upWin   = 0
        self.upLose  = 0
        self.upDraw  = 0
        self.downWin   = 0
        self.downLose  = 0
        self.downDraw  = 0
        self.old_go = None
        self.confidence  = c/100
        self.forget = f
        self.scale = scale/100

    def reset_game(self):
        super().reset_game()
        self.repeatWin  = 0
        self.repeatLose = 0
        self.repeatDraw = 0
        self.upWin   = 0
        self.upLose  = 0
        self.upDraw  = 0
        self.downWin   = 0
        self.downLose  = 0
        self.downDraw  = 0
        self.old_go = None

    def record(self, last_round):
        if len(self.game) > 1:
            go = self.game[-1].opponent
            result = self.game[-1].get_opponent_gain()
            if result == 1:
                if last_round.opponent == go:
                    if self.repeatWin < max(self.upWin,self.downWin) + self.forget:
                        self.repeatWin += 1
                elif last_round.opponent == beats[go]:
                    if self.upWin < max(self.repeatWin,self.downWin) + self.forget:
                        self.upWin += 1
                else:
                    if self.downWin < max(self.repeatWin,self.upWin) + self.forget:
                        self.downWin += 1
            elif result == 0:
                if last_round.opponent == go:
                    if self.repeatDraw < max(self.upDraw,self.downDraw) + self.forget:
                        self.repeatDraw += 1
                elif last_round.opponent == beats[go]:
                    if self.upDraw < max(self.repeatDraw,self.downDraw) + self.forget:
                        self.upDraw += 1
                else:
                    if self.downDraw < max(self.repeatDraw,self.upDraw) + self.forget:
                        self.downDraw += 1
            else:
                if last_round.opponent == go:
                    if self.repeatLose < max(self.upLose,self.downLose) + self.forget:
                        self.repeatLose += 1
                elif last_round.opponent == beats[go]:
                    if self.upLose < max(self.repeatLose,self.downLose) + self.forget:
                        self.upLose += 1
                else:
                    if self.downLose < max(self.repeatLose,self.upLose) + self.forget:
                        self.downLose += 1
            if self.old_go == last_round.opponent:
                if self.confidence < (100-self.scale)/100:
                    self.confidence += self.scale
                elif self.confidence < (100-self.scale/10)/100:
                    self.confidence += self.scale
            elif self.old_go != None:
                if self.confidence > self.scale:
                    self.confidence -= self.scale
                elif self.confidence > self.scale/10:
                    self.confidence -= self.scale/10
        self.confidence = round(self.confidence,6)
        print(self.confidence)
        super().record(last_round)

    def predict_agent_gesture(self):
        proba = {ROCK : 1/3, PAPER : 1/3, SCISSORS : 1/3}
        value = np.random.random()
        if len(self.game) > 0:
            result = self.game[-1].get_opponent_gain()
            go = self.game[-1].opponent
            if result == 1:
                if self.repeatWin > max(self.upWin,self.downWin):
                    proba[beats[go]] +=  1/3 * self.confidence
                    proba[beats[beats[go]]] -= 1/3 * self.confidence
                elif self.upWin > max(self.repeatWin,self.downWin):
                    proba[beats[beats[go]]] += 1/3 * self.confidence
                    proba[go] -= 1/3 * self.confidence
                elif self.downWin > max(self.upWin,self.repeatWin):
                    proba[go] +=  1/3 * self.confidence
                    proba[beats[go]] -= 1/3 * self.confidence
            elif result == 0:
                if self.repeatDraw > max(self.upDraw,self.downDraw):
                    proba[beats[go]] +=  1/3 * self.confidence
                    proba[beats[beats[go]]] -= 1/3 * self.confidence
                elif self.upDraw > max(self.repeatDraw,self.downDraw):
                    proba[beats[beats[go]]] += 1/3 * self.confidence
                    proba[go] -= 1/3 * self.confidence
                elif self.downDraw > max(self.upDraw,self.repeatDraw):
                    proba[go] +=  1/3 * self.confidence
                    proba[beats[go]] -= 1/3 * self.confidence
            else:
                if self.repeatLose > max(self.upLose,self.downLose):
                    proba[beats[go]] +=  1/3 * self.confidence
                    proba[beats[beats[go]]] -= 1/3 * self.confidence
                elif self.upLose > max(self.repeatLose,self.downLose):
                    proba[beats[beats[go]]] += 1/3 * self.confidence
                    proba[go] -= 1/3 * self.confidence
                elif self.downLose > max(self.upLose,self.repeatLose):
                    proba[go] +=  1/3 * self.confidence
                    proba[beats[go]] -= 1/3 * self.confidence
        if proba[ROCK] == proba[PAPER] == proba[SCISSORS]:
            self.old_go = None
        elif proba[ROCK] > max(proba[PAPER],proba[SCISSORS]):
            self.old_go = SCISSORS
        elif proba[PAPER] > proba[SCISSORS]:
            self.old_go = ROCK
        else:
            self.old_go = PAPER
        if value < proba[ROCK]:
            return ROCK
        if value < proba[ROCK] + proba[PAPER]:
            return PAPER
        return SCISSORS

    def load(filename=None):
        assert filename is None
        return StrategoPlayer()
