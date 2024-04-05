# -*- coding: utf-8 -*-
"""
Base elements for the Shifumi 2018 Qarma project
"""
import os
import sys
from pathlib import Path
import numpy as np

ROCK = np.uint8(0)
PAPER = np.uint8(1)
SCISSORS = np.uint8(2)

# RESOURCES_PATH = os.path.abspath(
#   Path(os.path.abspath(__file__)).parent / '../../resources')

if(sys.platform == "win32"):
    splitted_current_absolute_path = os.path.abspath(__file__).split("/")
    index_root = splitted_current_absolute_path[0].index("shifumy_player")
    RESOURCES_PATH = os.path.join(splitted_current_absolute_path[0][:index_root], "resources")
else:
    splitted_current_absolute_path = os.path.abspath(__file__).split("/")
    index_root = splitted_current_absolute_path.index("shifumy_player")
    RESOURCES_PATH = os.path.abspath("/".join(splitted_current_absolute_path[:index_root] + ["resources"]))


def str_rps(gesture, language='FR'):
    assert gesture in {ROCK, PAPER, SCISSORS}
    if language == 'FR':
        if gesture == ROCK:
            return 'Pierre'
        elif gesture == PAPER:
            return 'Papier'
        else:
            return 'Ciseaux'
    else:
        if gesture == ROCK:
            return 'Rock'
        elif gesture == PAPER:
            return 'Paper'
        else:
            return 'Scissors'


def rps_from_str(s, language='FR'):
    if language == 'FR':
        if s == 'Pierre':
            return ROCK
        elif s == 'Papier':
            return PAPER
        elif s == 'Ciseaux':
            return SCISSORS
        else:
            raise ValueError('Unknown gesture: {}.'.format(s))
    else:
        if s == 'Rock':
                return ROCK
        elif s == 'Paper':
            return PAPER
        elif s == 'Scissors':
            return SCISSORS
        else:
            raise ValueError('Unknown gesture: {}.'.format(s))


def get_rps_feature(gesture):
    assert gesture in {ROCK, PAPER, SCISSORS}
    if gesture == ROCK:
        return np.array([1, 0, 0])
    elif gesture == PAPER:
        return np.array([0, 1, 0])
    else:
        return np.array([0, 0, 1])


def get_game_features(game):
    assert isinstance(game, list)
    return np.array([r.features for r in game]).reshape((-1))

class Round():
    def __init__(self, opponent, agent):
        """
        A round composed of the opponent's and the agent's gestures

        Parameters
        ----------
        opponent : {ROCK, PAPER, SCISSORS}
            Opponent's gesture
        agent : {ROCK, PAPER, SCISSORS}
            Agent's gesture
        """
        assert opponent in {ROCK, PAPER, SCISSORS}
        assert agent in {ROCK, PAPER, SCISSORS}
        self.opponent = opponent
        self.agent = agent

    def get_agent_gain(self):
        """
        Gain of the agent

        Returns
        -------
        int
            The gain is 1 for the agent's victory, -1 for the agent's defeat
            and 0 otherwise
        """
        if self.opponent == self.agent:
            return 0
        elif (self.agent == ROCK and self.opponent == SCISSORS) \
                or (self.agent==PAPER and self.opponent == ROCK) \
                or (self.agent==SCISSORS and self.opponent == PAPER):
            return 1
        else:
            return -1

    def get_opponent_gain(self):
        return -self.get_agent_gain()

    @property
    def key(self):
        return str(self.opponent) + str(self.agent)

    def __repr__(self):
        return "opponent={}, agent={}".format(str_rps(self.opponent), \
                                              str_rps(self.agent))
    @property
    def features(self):
        return np.concatenate((get_rps_feature(self.opponent),
                               get_rps_feature(self.agent)))

class RpsAgent():
    """
    Abstract class for any RPS artifical player
    """
    def __init__(self):
        self.game = []

    def reset_game(self):
        """
        Reset the game by deleting all recorded rounds
        """
        self.game = []

    def record(self, last_round):
        """
        Record the last played round in the current game

        The round composed of opponent gesture and the predicted gesture is
        appended to the game.

        Parameters
        ----------
        last_round : Round
            Last played round to be recorded

        """
        assert isinstance(last_round, Round)
        self.game.append(last_round)

    def predict_agent_gesture(self):
        """
        Return the next gesture the agent will play.
        """
        raise NotImplementedError

    @staticmethod
    def load():
        """
        Load and return an instance of the agent from a file in resources/data/models.
        Use the variable RESOURCES_PATH which is your absolute path to the resources folder.
        """
        raise NotImplementedError
