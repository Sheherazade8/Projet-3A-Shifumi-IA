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
from shifumy_player.experiments.utils \
    import plot_rps
from shifumy_player.players.ve_players.sklearn_agents \
    import MultinomialNBAgent, SgdSvmAgent, SgdLogRegAgent, PerceptronAgent, \
    PassiveAggressiveClassifierAgent, MLPClassifierAgent
from shifumy_player.players.ve_players.naive_players \
    import SwitchStrategyAgent
from shifumy_player.players.ve_players.ve_online_pst import OnlinePstAgent

n_trials = 5
n_rounds = 1000
# n_rounds = 100
feature_size = 3
n_defeats_before_switch = 5

all_agents = [
    lambda: SwitchStrategyAgent(
        n_defeats_before_switch=n_defeats_before_switch),
    lambda: MLPClassifierAgent(feature_size=feature_size),
    lambda: PassiveAggressiveClassifierAgent(feature_size=feature_size),
    lambda: PerceptronAgent(feature_size=feature_size),
    lambda: SgdSvmAgent(feature_size=feature_size),
    lambda: SgdLogRegAgent(feature_size=feature_size),
    lambda: MultinomialNBAgent(feature_size=feature_size, alpha=1000),
    lambda: MultinomialNBAgent(feature_size=feature_size, alpha=1),
    lambda: OnlinePstAgent(max_depth=3),
    lambda: OnlinePstAgent(max_depth=2),
]
n_agents = len(all_agents)
scores = np.zeros((n_agents, n_agents, n_trials, n_rounds))

for i1, agent1 in enumerate(all_agents):
    for i2, agent2 in enumerate(all_agents):
        for i_trial in range(n_trials):
            if i2 < i1:
                scores[i1, i2, :, :] = -scores[i2, i1, :, :]
                continue
            a1 = agent1()
            a2 = agent2()
            print('{} vs {} ({}, {} / {}), trial {}/{}'
                  .format(a1, a2, i1, i2, len(all_agents), i_trial, n_trials))
            scores[i1, i2, i_trial, :] = \
                run_agent_vs_agent(a1, a2, n_rounds=n_rounds)

gamma = 0.9
g = gamma**np.arange(n_rounds)
G = g[None, None, None, :]
print(np.mean(np.sum(scores*G, axis=3), axis=2))
print(np.median(np.sum(scores*G, axis=3), axis=2))
print(np.min(np.sum(scores*G, axis=3), axis=2))
print(np.max(np.sum(scores*G, axis=3), axis=2))
print(np.std(np.sum(scores*G, axis=3), axis=2))
print(np.mean(np.mean(np.sum(scores*G, axis=3), axis=2), axis=1))

i_best = np.argmax(np.mean(np.mean(np.sum(scores*G, axis=3), axis=2), axis=1))
print('Best selected method:', all_agents[i_best]())

for i_best in range(n_agents):
    plt.figure(figsize=(10,10))
    for i_other in range(n_agents):
        y = np.cumsum(scores[i_best, i_other, :, :], axis=1) \
            / np.arange(1, n_rounds+1)[None, :]
        p = plt.plot(np.median(y, axis=0), label=str(all_agents[i_other]()))
        plt.fill_between(
            np.arange(n_rounds),
            np.min(y, axis=0),
            np.max(y, axis=0),
            color=p[0].get_color(),
            alpha=0.5,
        )
    plt.legend()
    plt.grid()
    plt.title('Performance of {} against other methods'
              .format(all_agents[i_best]()))
    plt.savefig('images/confusion_{}'.format(i_best))
