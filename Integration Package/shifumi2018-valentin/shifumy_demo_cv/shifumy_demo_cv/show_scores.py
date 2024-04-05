# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

from shifumy_demo_cv.main import load_games, print_all_scores

game_file = '2018-09-28_NuitChercheurs_recorded_games.pickle'
recorded_games, score_rounds, score_games = load_games(game_file)
print_all_scores(score_games, score_rounds)
