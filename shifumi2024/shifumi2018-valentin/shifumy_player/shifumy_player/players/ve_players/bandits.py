# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
from copy import deepcopy
import numpy as np

from ...base import RpsAgent
from ..random_player import RandomPlayer
from ..ve_players.sklearn_agents \
    import SgdLogRegAgent
from ..kilias_player import KiliasPlayer

class MetaAgent(RpsAgent):
    def __init__(self, agent_list=None):
        RpsAgent.__init__(self)
        if agent_list is None:
            agent_list = get_simple_agent_list()
        self.agent_list = agent_list
        self.agent_gain = np.zeros(self.n_agents)
        self.selected_agents = [] # track successive selection of agents

    @property
    def n_agents(self):
        return len(self.agent_list)

    def reset_game(self):
        """
        Reset the game by deleting all recorded rounds
        """
        RpsAgent.reset_game(self)
        self.selected_agents = []
        for a in self.agent_list:
            a.reset_game()

    def _get_best_agent(self):
        """ Best agent selection (to be implemented with specific criterion """
        raise NotImplementedError

    def predict_agent_gesture(self):
        """ Select best agent and return its prediction """
        i_agent = self._get_best_agent()
        return self.agent_list[i_agent].predict_agent_gesture()

    def record(self, last_round):
        RpsAgent.record(self, last_round=last_round)
        for a in self.agent_list:
            a.record(last_round=last_round)
        self.selected_agents.append(self._get_best_agent())

    def __str__(self):
        s = ''
        for i_agent in range(self.n_agents):
            s += str(repr(self.agent_list[i_agent])
                     + ': '
                     + str(self.agent_gain[i_agent])
                     + '\n')
        return s


class UpdateAllMetaAgent(MetaAgent):
    def __init__(self, agent_list=None):
        MetaAgent.__init__(self, agent_list=agent_list)

    def _get_best_agent(self):
        """ Select agent with best gain """
        return np.argmax(self.agent_gain)

    def record(self, last_round):
        """ Update all agents' gains with last round result """
        r = deepcopy(last_round)
        i_best = self._get_best_agent()
        for i_agent in range(self.n_agents):
            if i_agent == i_best:
                r.agent = last_round.agent
            else:
                r.agent = self.agent_list[i_agent].predict_agent_gesture()
            self._update_agent_gain(i_agent=i_agent, reward=r.get_agent_gain())

        # Record last_round
        MetaAgent.record(self, last_round=last_round)

    def _update_agent_gain(self, i_agent, reward):
        self.agent_gain[i_agent] += reward

    @staticmethod
    def load():
        return UpdateAllMetaAgent(agent_list=get_default_agent_list())


class UpdateAllNsMetaAgent(UpdateAllMetaAgent):
    def __init__(self, agent_list=None, alpha_ns=0.1):
        UpdateAllMetaAgent.__init__(self, agent_list=agent_list)
        self.alpha_ns = alpha_ns

    def _update_agent_gain(self, i_agent, reward):
        self.agent_gain[i_agent] += \
            self.alpha_ns * (reward - self.agent_gain[i_agent])

    @staticmethod
    def load():
        return UpdateAllNsMetaAgent(agent_list=get_default_agent_list())


class UcbMetaAgent(MetaAgent):
    def __init__(self, agent_list=None, alpha_ucb=1):
        MetaAgent.__init__(self, agent_list=agent_list)
        self.alpha_ucb = alpha_ucb
        self.agent_counter = np.zeros(self.n_agents)

    def _get_best_agent(self):
        """ Select agent according to UCB criterion """
        eps = np.finfo(float).eps
        ucb = self.agent_gain + self.alpha_ucb * \
              np.sqrt(np.log(len(self.game) + eps)
                      / (self.agent_counter + eps))
        return np.argmax(ucb)

    def _update_agent_gain(self, i_agent, reward):
        self.agent_gain[i_agent] += \
            (reward - self.agent_gain[i_agent]) / (len(self.game)+1)
        self.agent_counter[i_agent] += 1

    def record(self, last_round):
        # Update selected agent's gain with last round result
        i_agent = self._get_best_agent()
        self._update_agent_gain(i_agent=i_agent,
                                reward=last_round.get_agent_gain())

        # Record last_round
        MetaAgent.record(self, last_round=last_round)

    @staticmethod
    def load():
        return UcbMetaAgent(agent_list=get_default_agent_list())


def get_default_agent_list():
    from .ve_online_pst import OnlinePstAgent, OnlinePstAgentNS
    agent_list = []
    agent_list.append(RandomPlayer())
    agent_list.append(KiliasPlayer.load())
    agent_list.append(SgdLogRegAgent(feature_size=3))
    agent_list.append(SgdLogRegAgent(feature_size=8))
    agent_list.append(OnlinePstAgent())
    agent_list.append(OnlinePstAgent.load())
    agent_list.append(OnlinePstAgent(max_depth=8))
    agent_list.append(OnlinePstAgent.load(max_depth=8))
    a_load = OnlinePstAgentNS.load()
    for max_depth in [3, 5, 8]:
        for alpha in [0.001, 0.1, 0.5, 0.9]:
            a = OnlinePstAgentNS(max_depth=max_depth)
            a.set_alpha(alpha)
            agent_list.append(a)

            a = deepcopy(a_load)
            a.max_depth = max_depth
            a.set_alpha(alpha)
            agent_list.append(a)

    return agent_list


def get_simple_agent_list():
    return [RandomPlayer(),
            RandomPlayer(n_rps=[4, 3, 3]),
            RandomPlayer(n_rps=[3, 4, 3]),
            RandomPlayer(n_rps=[3, 3, 4]),]