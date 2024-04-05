# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import matplotlib.pyplot as plt

from shifumy_player.players.ve_players.bandits \
    import UcbMetaAgent, UpdateAllMetaAgent, UpdateAllNsMetaAgent, \
    get_simple_agent_list

from shifumy_player.players.ve_players.ve_online_pst import OnlinePstAgent
from shifumy_player.experiments.agent_vs_agent \
    import run_agent_vs_agent
from shifumy_player.experiments.utils \
    import plot_rps
from shifumy_player.players.ve_players.naive_players \
    import SwitchStrategyAgent

for k_agent, agent in {'UpdateAllMetaAgent': UpdateAllMetaAgent.load(),
                       'UcbMetaAgent': UcbMetaAgent.load(),
                       'UpdateAllNsMetaAgent': UpdateAllNsMetaAgent.load(),
                       }.items():
    print(k_agent)
    # agent = UpdateAllMetaAgent(agent_list=get_simple_agent_list())
    opponent = OnlinePstAgent.load()
    # opponent = SwitchStrategyAgent(n_defeats_before_switch=5)

    score = run_agent_vs_agent(agent,
                               opponent,
                               n_rounds=2000)
    print(agent)
    plot_rps(score, filename='images/OnlinePst_vs_Switch')
    plt.subplot(211)
    plt.title(k_agent)

    plt.figure()
    plt.plot(agent.selected_agents)
    plt.title('Selected agents for '+ k_agent)

