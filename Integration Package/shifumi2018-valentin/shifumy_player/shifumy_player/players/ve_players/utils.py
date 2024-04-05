# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import numpy as np

from ...base import ROCK, PAPER, SCISSORS


def get_gesture_with_best_gain_expectation(n_rps):
    """
    Gesture to be played with best gain expectation from opponent's statistics

    Parameters
    ----------
    n_rps : dict
        n_rps[str(ROCK)], n_rps[str(PAPER)], n_rps[str(SCISSORS)] are the
        counts or ratio of the opponent's gesture

    Returns
    -------
    {ROCK, PAPER, SCISSORS}
        Gesture to be played by the agent
    """
    sum_rps = np.sum(list(n_rps.values()))
    proba_r = n_rps[str(ROCK)]/sum_rps
    proba_p = n_rps[str(PAPER)]/sum_rps
    proba_s = n_rps[str(SCISSORS)]/sum_rps
    if proba_r > 1/3 and proba_s < 1/3:
        return PAPER
    elif proba_p > 1/3 and proba_r < 1/3:
        return SCISSORS
    else:
        return ROCK
