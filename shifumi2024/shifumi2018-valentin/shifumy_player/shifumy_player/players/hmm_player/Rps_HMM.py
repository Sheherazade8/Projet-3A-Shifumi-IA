#-*- coding: utf-8 -*-

# Mac Donald  Kilian
# RpsAgent_HMM
# crée le 28/06/2018

from shifumy_player.players.hmm_player.classe2 import *
from shifumy_player.players.hmm_player.fonctions_2 import *
from shifumy_player.base import *

#
# from classe2 import *
# from fonctions_2 import *
from shifumy_player.base import *


class Rps_HMM(RpsAgent):
    def __init__(self, hmm = None, filename = None):
        super().__init__()
        self.hmm = hmm
        self.filename = filename

    def predict_agent_gesture(self):
        if self.game == []:
            return PAPER
        if len(self.game) >= 2:
            self.update()
        hist = ()
        for x in self.game:
            hist += (int(str(x.opponent) + str(x.agent), 3), )
        coup = self.hmm.predit_bat(hist)
        return coup

    def load(filename=None):
        path = os.path.join(RESOURCES_PATH,"data")
        path2 = os.path.join(path,"models")
        path3 = os.path.join(path2,"HMM")
        path4 = os.path.join(path3,"HMM_RPS")
        hmm = HMM.load(path4)
        return Rps_HMM(hmm, "HMM_RPS")

    def update(self):
        path = os.path.join(RESOURCES_PATH,"data")
        path2 = os.path.join(path,"models")
        path3 = os.path.join(path2,"HMM")
        path4 = os.path.join(path3,self.filename)
        self.hmm = HMM.load(path4)
        hist = ()
        for x in self.game:
            hist += (int(str(x.opponent) + str(x.agent), 3),)
        self.hmm.bw1([hist])
