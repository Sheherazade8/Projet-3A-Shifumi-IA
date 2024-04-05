# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import matplotlib.pyplot as plt

from shifumy_player.experiments.agent_vs_agent \
    import run_agent_vs_agent
from shifumy_player.experiments.utils \
    import plot_rps
from shifumy_player.players.ve_players.naive_players \
    import WinOnPreviousNaiveAgent, LoseOnPreviousNaiveAgent, \
    RepeatPreviousNaiveAgent, SwitchStrategyAgent
from shifumy_player.players.ve_players.ve_online_pst import OnlinePstAgent


# Create agent
online_pst_agent = OnlinePstAgent(max_depth=1)

# Play against first player
score = run_agent_vs_agent(online_pst_agent, RepeatPreviousNaiveAgent(),
                           n_rounds=50)
online_pst_agent.root.print()
plot_rps(score, filename='images/OnlinePST_vs_Player1_RepeatPreviousNaiveAgent')

# Play against third player
score = run_agent_vs_agent(online_pst_agent, LoseOnPreviousNaiveAgent(),
                           n_rounds=300)
online_pst_agent.root.print()
plot_rps(score, filename='images/OnlinePST_vs_Player2_LoseOnPreviousNaiveAgent')

# Play against second player
score = run_agent_vs_agent(online_pst_agent, WinOnPreviousNaiveAgent(),
                           n_rounds=1500)
online_pst_agent.root.print()
plot_rps(score, filename='images/OnlinePST_vs_Player3_WinOnPreviousNaiveAgent')

# Create agent
online_pst_agent = OnlinePstAgent(max_depth=1)
opponent = SwitchStrategyAgent(n_defeats_before_switch=10)
score = run_agent_vs_agent(online_pst_agent,
                           opponent,
                           n_rounds=2000)
online_pst_agent.root.print()
print('Number of switches (opponent):', opponent.n_switch)
plot_rps(score, filename='images/OnlinePst_vs_Switch')

# Load learned agent
online_pst_agent = OnlinePstAgent.load()
opponent = SwitchStrategyAgent(n_defeats_before_switch=10)
score = run_agent_vs_agent(online_pst_agent,
                           opponent,
                           n_rounds=2000)
online_pst_agent.root.print()
print('Number of switches (opponent):', opponent.n_switch)
plot_rps(score, filename='images/LoadedOnlinePst_vs_Switch')

plt.show()
