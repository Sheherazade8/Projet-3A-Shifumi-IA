# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import numpy as np
import matplotlib.pyplot as plt

from shifumy_player.experiments.agent_vs_agent \
    import run_agent_vs_agent
from shifumy_player.players.ve_players.naive_players \
    import SwitchStrategyAgent
from shifumy_player.players.ve_players.ve_online_pst \
    import OnlinePstAgent
from shifumy_player.players.ve_players.sklearn_agents \
    import MultinomialNBAgent, SgdLogRegAgent, SgdSvmAgent, PerceptronAgent, \
    PassiveAggressiveClassifierAgent, MLPClassifierAgent

n_rounds = 10000
n_defeats_list = 2**np.arange(6)
agents = {
    'OnlinePstAgent': OnlinePstAgent,
    'MultinomialNBAgent1': MultinomialNBAgent,
    'MultinomialNBAgent1000': MultinomialNBAgent,
    'SgdLogRegAgent': SgdLogRegAgent,
    'SgdSvmAgent': SgdSvmAgent,
    'PerceptronAgent': PerceptronAgent,
    'PassiveAggressiveClassifierAgent': PassiveAggressiveClassifierAgent,
    'MLPClassifierAgent': MLPClassifierAgent,
}
agent_params = {
    'OnlinePstAgent': {'max_depth':1},
    'MultinomialNBAgent1': {'alpha': 1},
    'MultinomialNBAgent1000': {'alpha': 1000},
    'SgdLogRegAgent': dict(),
    'SgdSvmAgent': dict(),
    'PerceptronAgent': dict(),
    'PassiveAggressiveClassifierAgent': dict(),
    'MLPClassifierAgent': dict(),
}
scores = dict()
for k_agent in agents.keys():
    scores[k_agent] = np.empty((n_defeats_list.size))
n_switches = dict()
for k_agent in agents.keys():
    n_switches[k_agent] = np.empty((n_defeats_list.size))
for i_defeats, n_defeats_before_switch in enumerate(n_defeats_list):
    print('*' * 80)
    print('n_defeats_before_switch =', n_defeats_before_switch)
    for k_agent in agents.keys():
        agent = agents[k_agent](**agent_params[k_agent])
        print('Agent', agent)
        opponent = SwitchStrategyAgent(n_defeats_before_switch=10)
        score = run_agent_vs_agent(agent, opponent, n_rounds=n_rounds)
        scores[k_agent][i_defeats] = np.mean(score)
        n_switches[k_agent][i_defeats] = opponent.n_switch

plt.figure()
for k_agent in agents.keys():
    plt.plot(n_defeats_list, scores[k_agent], label=k_agent)
plt.grid()
plt.legend()
plt.xlabel('n_defeats_before_switch')
plt.ylabel('Average score ({} rounds)'.format(n_rounds))
plt.savefig('images/script_sklearn_demo_scores')

plt.figure()
for k_agent in agents.keys():
    plt.plot(n_defeats_list, n_switches[k_agent], label=k_agent)
plt.grid()
plt.legend()
plt.xlabel('n_defeats_before_switch')
plt.ylabel('Number of switches ({} rounds)'.format(n_rounds))
plt.savefig('images/script_sklearn_demo_switches')

plt.show()
