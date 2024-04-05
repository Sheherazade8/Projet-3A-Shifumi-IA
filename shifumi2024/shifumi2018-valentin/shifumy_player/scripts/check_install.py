# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import sys
sys.path.append('../../third_parties/')

from shifumy.random_player import RandomPlayer
from example_module.toto import hello

hello()
print(RandomPlayer().predict_agent_gesture())
