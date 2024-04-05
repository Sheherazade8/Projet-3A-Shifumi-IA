#-*- coding: utf-8 -*-

# Mac Donald  Kilian
# test_agent
# crée le 04/07/2018

#from base import *
#import sys
#sys.path.append('../../../resources/models')
from shifumy_player.players.hmm_player.Rps_HMM import  *

import random

hmm = Rps_HMM.load()

cp = [ROCK, PAPER, SCISSORS]
for i in range(60):
    a = hmm.predict_agent_gesture()
    o = random.randint(0,2)
    r = Round(cp[o], a)
    hmm.record(r)
    print(o, a)

"""
hmm = Rps_HMM.load('HMM_RPS')
won = 0
lost = 0
part = parties_to_donnees('dataverif')
cp = [ROCK, PAPER, SCISSORS]
for x in part:
    for c in x:
        ca = hmm.predict_agent_gesture()
        co = int(c/3)
        if ca == (co + 1) % 3:
            won += 1
        elif co == (ca + 1) % 3:
            lost += 1
        hmm.record(Round(cp[co], cp[ca]))
    hmm.reset_game()
print(won, lost, won/(won + lost) * 100)
"""
