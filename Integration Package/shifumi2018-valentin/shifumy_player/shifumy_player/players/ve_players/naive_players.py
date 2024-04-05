# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
from ...base import RpsAgent, ROCK, PAPER, SCISSORS
from ..random_player import RandomPlayer


class WinOnPreviousNaiveAgent(RpsAgent):
    """ Naive strategy where the agent plays what would win against the
    opponent's last gesture """
    def predict_agent_gesture(self):
        """
        Return the next gesture the agent will play
        """
        if len(self.game) == 0:
            rp = RandomPlayer()
            return rp.predict_agent_gesture()

        last_round = self.game[-1]
        if last_round.opponent == ROCK:
            return PAPER
        elif last_round.opponent == SCISSORS:
            return ROCK
        else:
            return SCISSORS

    @staticmethod
    def load():
        """
        Load and return an instance of the agent from a file in resources/data/models.
        Use the variable RESOURCES_PATH which is your absolute path to the resources folder.
        """
        return WinOnPreviousNaiveAgent()


class LoseOnPreviousNaiveAgent(RpsAgent):
    """ Naive strategy where the agent plays what would lose against the
    opponent's last gesture """
    def predict_agent_gesture(self):
        """
        Return the next gesture the agent will play.
        """
        if len(self.game) == 0:
            rp = RandomPlayer()
            return rp.predict_agent_gesture()

        last_round = self.game[-1]
        if last_round.opponent == PAPER:
            return ROCK
        elif last_round.opponent == ROCK:
            return SCISSORS
        else:
            return PAPER

    @staticmethod
    def load():
        """
        Load and return an instance of the agent from a file in resources/data/models.
        Use the variable RESOURCES_PATH which is your absolute path to the resources folder.
        """
        return LoseOnPreviousNaiveAgent()


class RepeatPreviousNaiveAgent(RpsAgent):
    """ Naive strategy where the agent plays the opponent's last gesture """
    def predict_agent_gesture(self):
        """
        Return the next gesture the agent will play.
        """
        if len(self.game) == 0:
            rp = RandomPlayer()
            return rp.predict_agent_gesture()

        last_round = self.game[-1]
        return last_round.opponent

    @staticmethod
    def load():
        """
        Load and return an instance of the agent from a file in resources/data/models.
        Use the variable RESOURCES_PATH which is your absolute path to the resources folder.
        """
        return LoseOnPreviousNaiveAgent()


class SwitchStrategyAgent(RpsAgent):
    """
    Parameters
    ----------
    agents : list of RpsAgent
        List of agent to be played alternatively and cyclicly
    n_defeats_before_switch : int
        Number of consecutive defeats to switch to the next agent
    """
    def __init__(self,
                 agents=[WinOnPreviousNaiveAgent(),
                         RepeatPreviousNaiveAgent(),
                         LoseOnPreviousNaiveAgent()],
                 n_defeats_before_switch=3
                 ):
        """

        """
        RpsAgent.__init__(self)
        self.agents = agents
        self.current_agent_id = 0
        self.n_defeats_before_switch = n_defeats_before_switch
        # This counter prevents switching before performing n_switch round
        # with the same agent
        self._start_switch_counter = 0
        self.n_switch = 0  # Counter for number of switches performed

    def reset_game(self):
        for a in self.agents:
            a.reset_game()

    def record(self, last_round):
        RpsAgent.record(self, last_round)
        for a in self.agents:
            a.record(last_round)

    def predict_agent_gesture(self, verbose=False):
        cum_gain = sum([r.get_opponent_gain()
                        for r in self.game[-self.n_defeats_before_switch:]])
        self._start_switch_counter += 1
        n_defeats = min(self._start_switch_counter, cum_gain)
        if n_defeats >= self.n_defeats_before_switch:
            self.n_switch += 1
            self._start_switch_counter = 0
            self.current_agent_id += 1
            self.current_agent_id %= len(self.agents)
            if verbose:
                print('Switch to {}'.format(self.current_agent_id))
        return self.agents[self.current_agent_id].predict_agent_gesture()

    def __repr__(self):
        return 'SwitchStrategyAgent(n_defeats_before_switch={})'\
            .format(self.n_defeats_before_switch)

    def __str__(self):
        return self.__repr__()