# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

from rl.core import Env
from gym import spaces
import numpy as np

from shifumy_player.base import Round, ROCK, PAPER, SCISSORS


class rps_env(Env):
    def __init__(self, opponent_constructor, feature_size=3):
        self.opponent_constructor = opponent_constructor
        self.feature_size = feature_size
        self._opponent = None
        self._game = None

    def reset(self):
        # self._opponent = self.opponent_constructor()
        self._opponent.reset_game()
        self._game = []

    @property
    def action_space(self):
        return spaces.Discrete(3)

    @property
    def observation_space(self):
        return spaces.Discrete(9**self.feature_size)

    def step(self, action):
        ga = action_to_gesture(action)
        go = self._opponent.predict_agent_gesture()
        r = Round(ga, go)
        self._opponent.record(r)
        self._game.append(r)

        observation = self._game[-self.feature_size:]
        reward = r.get_agent_gain()
        done = False
        info = dict()
        return observation, reward, done, info


def action_to_gesture(action):
    assert np.issubdtype(type(action), np.integer)
    assert 0 <= action < 3
    if action == 0:
        return ROCK
    elif action == 1:
        return PAPER
    else: return SCISSORS


def gesture_to_action(g):
    assert g in {ROCK, PAPER, SCISSORS}
    if g == ROCK:
        return 0
    elif g == PAPER:
        return 1
    else:
        return 2


def game_to_obs(game):
    actions = []
    for r in game:
        actions.append(gesture_to_action(r.opponent))
        actions.append(gesture_to_action(r.agent))
    obs = np.ravel_multi_index(actions, [3,] * len(actions))
    return obs


def obs_to_game(obs, feature_size):
    actions = np.unravel_index(obs, [3,] * 2 * feature_size)
    game = []
    for i in range(0, len(actions), 2):
        go = action_to_gesture(actions[i])
        ga = action_to_gesture(actions[i+1])
        game.append(Round(agent=ga, opponent=go))
    return game
