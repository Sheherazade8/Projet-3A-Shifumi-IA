# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import matplotlib.pyplot as plt

from shifumy_player.experiments.agent_vs_agent \
    import run_agent_vs_agent
from shifumy_player.experiments.utils \
    import plot_rps
from shifumy_player.players.ve_players.sklearn_agents \
    import MultinomialNBAgent, SgdSvmAgent, SgdLogRegAgent, PerceptronAgent, \
    PassiveAggressiveClassifierAgent, MLPClassifierAgent
from shifumy_player.players.ve_players.naive_players \
    import SwitchStrategyAgent

n_rounds = 10000
feature_size = 3
n_defeats_before_switch = 5

for agent in [MLPClassifierAgent(feature_size=feature_size),
              PassiveAggressiveClassifierAgent(feature_size=feature_size),
              PerceptronAgent(feature_size=feature_size),
              SgdSvmAgent(feature_size=feature_size),
              SgdLogRegAgent(feature_size=feature_size),
              MultinomialNBAgent(feature_size=feature_size, alpha=1000),
              ]:
    opponent = SwitchStrategyAgent(n_defeats_before_switch=n_defeats_before_switch)
    score = run_agent_vs_agent(agent, opponent, n_rounds=n_rounds)
    print('Number of switches (opponent):', opponent.n_switch)
    plot_rps(score, filename='images/demo_{}'.format(agent), title=agent)

plt.show()


