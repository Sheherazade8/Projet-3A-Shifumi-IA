# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Mathias Aloui, Kilian McDonald
"""

from .stratego_player    import *
from .hmm_player.Rps_HMM import *
from shifumy_player.base import *

class KiliasPlayer(RpsAgent):

    def __init__(self):
        super().__init__()
        self.stratego = StrategoPlayer.load()
        self.hmm = Rps_HMM.load()

    def predict_agent_gesture(self):
        gesture = self.stratego.predict_agent_gesture()
        if self.stratego.confidence <= 50/100:
            gesture = self.hmm.predict_agent_gesture()
            print("~~~~~ HMM")
            return gesture
        print("~~~~~ Stratego")
        return gesture

    def record(self, last_round):
        if len(self.stratego.game) > 1:
            go = self.stratego.game[-1].opponent
            result = self.stratego.game[-1].get_opponent_gain()
            if result == 1:
                if last_round.opponent == go:
                    if self.stratego.repeatWin < max(self.stratego.upWin,self.stratego.downWin) + self.stratego.forget:
                        self.stratego.repeatWin += 1
                elif last_round.opponent == beats[go]:
                    if self.stratego.upWin < max(self.stratego.repeatWin,self.stratego.downWin) + self.stratego.forget:
                        self.stratego.upWin += 1
                else:
                    if self.stratego.downWin < max(self.stratego.repeatWin,self.stratego.upWin) + self.stratego.forget:
                        self.stratego.downWin += 1
            elif result == 0:
                if last_round.opponent == go:
                    if self.stratego.repeatDraw < max(self.stratego.upDraw,self.stratego.downDraw) + self.stratego.forget:
                        self.stratego.repeatDraw += 1
                elif last_round.opponent == beats[go]:
                    if self.stratego.upDraw < max(self.stratego.repeatDraw,self.stratego.downDraw) + self.stratego.forget:
                        self.stratego.upDraw += 1
                else:
                    if self.stratego.downDraw < max(self.stratego.repeatDraw,self.stratego.upDraw) + self.stratego.forget:
                        self.stratego.downDraw += 1
            else:
                if last_round.opponent == go:
                    if self.stratego.repeatLose < max(self.stratego.upLose,self.stratego.downLose) + self.stratego.forget:
                        self.stratego.repeatLose += 1
                elif last_round.opponent == beats[go]:
                    if self.stratego.upLose < max(self.stratego.repeatLose,self.stratego.downLose) + self.stratego.forget:
                        self.stratego.upLose += 1
                else:
                    if self.stratego.downLose < max(self.stratego.repeatLose,self.stratego.upLose) + self.stratego.forget:
                        self.stratego.downLose += 1
            if self.stratego.old_go == last_round.opponent:
                if self.stratego.confidence < (100-self.stratego.scale)/100:
                    self.stratego.confidence += self.stratego.scale
            elif self.stratego.old_go != None:
                if self.stratego.confidence > self.stratego.scale:
                    self.stratego.confidence -= self.stratego.scale
        self.stratego.confidence = round(self.stratego.confidence,6)
        print(self.stratego.confidence)
        self.game.append(last_round)
        self.stratego.game.append(last_round)
        self.hmm.game.append(last_round)

    def reset_game(self):
        self.stratego.reset_game()

    @staticmethod
    def load():
        agent = KiliasPlayer()
        return agent
