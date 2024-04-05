# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import matplotlib.pyplot as plt

from shifumy_player.experiments.agent_vs_agent \
    import run_agent_vs_agent
from shifumy_player.experiments.utils \
    import plot_rps
from shifumy_player.players.ve_players.ve_online_pst \
    import OnlinePstAgent
from shifumy_player.players.random_player import RandomPlayer

# Create agent
online_pst_agent = OnlinePstAgent(max_depth=1)

# Play against first player
score = run_agent_vs_agent(online_pst_agent,
                           RandomPlayer(n_rps=[100, 10, 1]),
                           n_rounds=500)
online_pst_agent.root.print()
plot_rps(score, filename='images/OnlinePST_vs_UnbalancedRandom')
plt.show()


