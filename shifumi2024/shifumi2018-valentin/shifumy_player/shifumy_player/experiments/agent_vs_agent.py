# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import numpy as np

from ..base import Round, str_rps


def run_agent_vs_agent(agent1, agent2, n_rounds=1000, verbose=False):
    score_a1 = np.empty(n_rounds)
    score_a1.fill(np.nan)

    for i_round in range(n_rounds):
        # Play
        agent1_gesture = agent1.predict_agent_gesture()
        agent2_gesture = agent2.predict_agent_gesture()
        round_a = Round(agent=agent1_gesture, opponent=agent2_gesture)
        score_a1[i_round] = round_a.get_agent_gain()

        if verbose:
            print('Round {}: {} vs {} -> {}'.format(
                i_round,
                str_rps(round_a.opponent),
                str_rps(round_a.agent),
                round_a.get_agent_gain(),
            ))

        # Record
        agent1.record(round_a)
        agent2.record(Round(agent=agent2_gesture, opponent=agent1_gesture))

    return score_a1

