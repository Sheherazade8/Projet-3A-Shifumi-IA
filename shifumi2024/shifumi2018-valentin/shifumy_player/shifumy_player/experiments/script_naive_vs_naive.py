# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import matplotlib.pyplot as plt

from shifumy_player.experiments.agent_vs_agent \
    import run_agent_vs_agent
from shifumy_player.experiments.utils \
    import plot_rps
from shifumy_player.players.random_player import RandomPlayer
from shifumy_player.players.ve_players.naive_players \
    import WinOnPreviousNaiveAgent, LoseOnPreviousNaiveAgent, RepeatPreviousNaiveAgent

score = run_agent_vs_agent(RandomPlayer(), RandomPlayer())
plot_rps(score=score, filename='images/RandomPlayer_vs_RandomPlayer')

score = run_agent_vs_agent(WinOnPreviousNaiveAgent(), RandomPlayer())
plot_rps(score=score, filename='images/WinOnPreviousNaiveAgent_vs_RandomPlayer')

score = run_agent_vs_agent(WinOnPreviousNaiveAgent(),
                           RepeatPreviousNaiveAgent())
plot_rps(score=score,
         filename='images/WinOnPreviousNaiveAgent_vs_RepeatPreviousNaiveAgent')

score = run_agent_vs_agent(LoseOnPreviousNaiveAgent(),
                          RepeatPreviousNaiveAgent())
plot_rps(score=score,
         filename='images/LoseOnPreviousNaiveAgent_vs_RepeatPreviousNaiveAgent')

score = run_agent_vs_agent(WinOnPreviousNaiveAgent(),
                           RandomPlayer(n_rps=[100, 10, 1]))
plot_rps(score=score,
         filename='images/WinOnPreviousNaiveAgent_vs_UnbalancedRandomPlayer')
plt.show()