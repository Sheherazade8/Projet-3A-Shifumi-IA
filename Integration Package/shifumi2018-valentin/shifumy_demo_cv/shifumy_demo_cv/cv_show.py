# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import cv2 as cv
from pathlib import Path
import numpy as np


from shifumy_player.base import \
    Round, str_rps, rps_from_str, ROCK, PAPER, SCISSORS, RESOURCES_PATH


background_colors = {'opponent_wins': (0, 191, 0),
                     'agent_wins': (0, 0, 191),
                     'draw': (191, 0, 0)}

class CvShow:
    def __init__(self, win_name, win_size, move_xy=None):
        self.agent_name = None
        # Load images
        self.images = {
            ROCK: cv.imread(
                str(Path(RESOURCES_PATH) / 'images/rock.jpg'),
                cv.IMREAD_GRAYSCALE),
            PAPER: cv.imread(
                str(Path(RESOURCES_PATH) / 'images/paper.jpg'),
                cv.IMREAD_GRAYSCALE),
            SCISSORS: cv.imread(
                str(Path(RESOURCES_PATH) / 'images/scissors.jpg'),
                cv.IMREAD_GRAYSCALE),
        }

        # for g in ROCK, PAPER, SCISSORS:
        #     cv.imshow(str_rps(g), self.images[g])
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     pass
        self.win_name = win_name
        # self.screen_size = np.array((900, 1440))
        # self.screen_size = np.array((1080, 1920))
        self.screen_size = win_size
        cv.namedWindow(self.win_name, cv.WINDOW_FULLSCREEN)
        cv.setWindowProperty(self.win_name,
                             cv.WND_PROP_FULLSCREEN,
                             cv.WINDOW_FULLSCREEN)
        if move_xy is not None:
            cv.moveWindow(self.win_name, move_xy[0], move_xy[1])
        self.screen = np.zeros((self.screen_size[0], self.screen_size[1], 3),
                               dtype=np.uint8)

        # Build dictionaries of resized images
        self.images_20 = dict()
        self.images_60 = dict()
        for g in self.images.keys():
            im = self.images[g]
            resize_ratio_20 = self.screen_size[0] * 0.20 / im.shape[0]
            self.images_20[g] = cv.resize(im,
                                          dsize=(0, 0),
                                          fx=resize_ratio_20,
                                          fy=resize_ratio_20,
                                          interpolation=cv.INTER_LANCZOS4)
            resize_ratio_60 = self.screen_size[0] * 0.6 / im.shape[0]
            self.images_60[g] = cv.resize(im,
                                          dsize=(0, 0),
                                          fx=resize_ratio_60,
                                          fy=resize_ratio_60,
                                          interpolation=cv.INTER_LANCZOS4)

        # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        # cv2.imshow("window", img)
        # self.screen = np.array()

    def _show_screen(self):
        cv.imshow(self.win_name, self.screen)
        if cv.waitKey(1) & 0xFF == ord('q'):
            pass
        # cv.waitKey(0)

    def _clear_screen(self, background_color=(0, 0, 0)):
        self.screen[:, :, :] = np.array(background_color)[None, None, :]

    def _put_score(self, scores, location='bottom', j_start=None):
        """ 20% bottom or top area """
        text_opponent = 'Vous: ' + str(scores['opponent'])
        text_agent = self.agent_name + ': ' + str(scores['agent'])
        if location in ('top', 'bottom'):
            if location == 'bottom':
                y = self.screen_size[0] * 0.9
            else:
                y = self.screen_size[0] * 0.1
            # Put opponent's score on the left
            cv.putText(img=self.screen,
                       text=text_opponent,
                       org=(int(self.screen_size[1] *0.6),
                            int(y)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)

            # Put agent's score on the right
            cv.putText(img=self.screen,
                       text=text_agent,
                       org=(int(self.screen_size[1] * 0.1),
                            int(y)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)
        elif location == 'right':
            cv.putText(img=self.screen,
                       text=text_opponent,
                       org=(int(self.screen_size[1] * 0.5),
                            int(self.screen_size[0] * 0.45)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)

            # Put agent's score on the right
            cv.putText(img=self.screen,
                       text=text_agent,
                       org=(int(self.screen_size[1] * 0.5),
                            int(self.screen_size[0] * 0.55)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)
        elif location == 'topleft':
            text = '{} {} - {} Humain'.format(self.agent_name,
                                              str(scores['agent']),
                                              str(scores['opponent']))
            # Put both scores
            cv.putText(img=self.screen,
                       text=text,
                       org=(int(j_start),
                            int(self.screen_size[0] * 0.1)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=1.5,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)
        else:
            raise ValueError('Unknown location: ' + location)

    def _put_n_rounds_left(self, n_round_left, location='topright',
                           j_start=None):
        if location == 'topright':
            if n_round_left == 1:
                s = '1 round restant'
            else:
                s = str(n_round_left) + ' rounds restants'
            cv.putText(img=self.screen,
                       text=s,
                       org=(int(self.screen_size[1] * 0.3),
                            int(self.screen_size[0] * 0.1)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=8,
                       lineType=cv.LINE_AA)
        elif location == 'bottomleft':
            # Add number of remaining rounds
            cv.putText(img=self.screen,
                       text=str(n_round_left) + ' round(s) restant(s)',
                       org=(j_start,
                            int(self.screen_size[0] * 0.9)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=1.5,
                       color=(255, 255, 255),
                       thickness=3,
                       lineType=cv.LINE_AA)
        else:
            raise ValueError('Unknown location: ' + location)

    def show_center_text(self, text, text2=None):
        self._clear_screen()
        if text2 is None:
            # Add text
            cv.putText(img=self.screen,
                       text=text,
                       org=(int(self.screen_size[1] * 0.1),
                            int(self.screen_size[0] * 0.5)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)
        else:
            # Add text
            cv.putText(img=self.screen,
                       text=text,
                       org=(int(self.screen_size[1] * 0.1),
                            int(self.screen_size[0] * 0.4)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)
            # Add text
            cv.putText(img=self.screen,
                       text=text2,
                       org=(int(self.screen_size[1] * 0.1),
                            int(self.screen_size[0] * 0.6)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=4,
                       lineType=cv.LINE_AA)

        self._show_screen()

    def show_choose_3_options(self, title, rps_options):
        self._clear_screen()

        # Add gesture images
        rps_img_v = np.concatenate((self.images_20[ROCK],
                                    self.images_20[PAPER],
                                    self.images_20[SCISSORS]),
                                   axis = 0)
        dx = rps_img_v.shape[1]
        dy = int(self.screen_size[0] * 0.1)
        self.screen[-rps_img_v.shape[0]-dy:-dy, dx:dx+rps_img_v.shape[1],:] = \
            rps_img_v[:, :, None]

        # Add text
        cv.putText(img=self.screen,
                   text=title,
                   org=(int(rps_img_v.shape[1]),
                        int(self.screen_size[0]*0.3/2)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=1.5,
                   color=(255, 255, 255),
                   thickness=2,
                   lineType=cv.LINE_AA)

        for i_g, g in enumerate([ROCK, PAPER, SCISSORS]):
            cv.putText(img=self.screen,
                       text=rps_options[g],
                       org=(int(rps_img_v.shape[1] * 1.25 + dx),
                            int(self.screen_size[0] *(0.4 + i_g * 0.2))),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=2,
                       color=(255, 255, 255),
                       thickness=2,
                       lineType=cv.LINE_AA)

        self._show_screen()

    def show_wait_gesture(self, scores, n_round_left, location="left"):
        self._clear_screen()
        if location == 'right':
            # Add text
            cv.putText(img=self.screen,
                       text="Jouez!",
                       org=(int(self.screen_size[1] * 0.4),
                            int(self.screen_size[0] * 0.5)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=2,
                       lineType=cv.LINE_AA)
            self._put_score(scores, location='bottom')
            self._put_n_rounds_left(n_round_left=n_round_left)
        elif location == 'left':
            # Add text
            cv.putText(img=self.screen,
                       text="Jouez!",
                       org=(int(self.screen_size[1] * 0.1),
                            int(self.screen_size[0] * 0.5)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3,
                       color=(255, 255, 255),
                       thickness=2,
                       lineType=cv.LINE_AA)
            self._put_score(scores, location='right')
            self._put_n_rounds_left(n_round_left=n_round_left)
        self._show_screen()

    def show_agent_result(self, round, scores, n_round_left):
        res = round.get_opponent_gain()
        if res == 1:
            background_color = background_colors['opponent_wins']
        elif res == -1:
            background_color = background_colors['agent_wins']
        else:
            background_color = background_colors['draw']
        self._clear_screen(background_color=background_color)

        # Add gesture images
        im = self.images_60[round.agent]
        i_start = int(self.screen_size[0] / 2 - im.shape[0] / 2)
        i_end = i_start + im.shape[0]
        j_start = int(self.screen_size[1] / 4 - im.shape[1] / 2)
        j_end = j_start + im.shape[1]
        self.screen[i_start:i_end, j_start:j_end, :] = im[:, :, None]

        # Add scores
        self._put_score(scores, location='right')
        self._put_n_rounds_left(n_round_left=n_round_left,
                                location='topright')

        self._show_screen()

    def show_backstage(self, agent_gesture, scores, n_round_left,
                       score_games, score_rounds):
        self._clear_screen()

        # Add agent's gesture images
        im = self.images_60[agent_gesture]
        i_start = int(self.screen_size[0] / 2 - im.shape[0] / 2)
        i_end = i_start + im.shape[0]
        j_start = int(self.screen_size[1] / 4 - im.shape[1] / 2)
        j_end = j_start + im.shape[1]
        self.screen[i_start:i_end, j_start:j_end, :] = im[:, :, None]

        # Add text "Prochain coup"
        cv.putText(img=self.screen,
                   text="Prochain coup",
                   org=(int(self.screen_size[1] * 0.1),
                        int(self.screen_size[0] * 0.75)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=2,
                   color=(0, 0, 0),
                   thickness=3,
                   lineType=cv.LINE_AA)

        # Add number of remaining rounds
        self._put_n_rounds_left(n_round_left=n_round_left,
                                location='bottomleft',
                                j_start=j_start)
        # cv.putText(img=self.screen,
        #            text=str(n_round_left) + ' round(s) restant(s)',
        #            org=(j_start,
        #                 int(self.screen_size[0] * 0.1)),
        #            fontFace=cv.FONT_HERSHEY_SIMPLEX,
        #            fontScale=1.5,
        #            color=(255, 255, 255),
        #            thickness=3,
        #            lineType=cv.LINE_AA)

        self._put_score(scores=scores, location='topleft', j_start=j_start)

        self._put_stats(scores=scores,
                        score_games=score_games,
                        score_rounds=score_rounds)
        self._show_screen()

    def show_round_result(self, round, scores, n_round_left,
                          score_games, score_rounds):
        res = round.get_opponent_gain()
        if res == 1:
            background_color = background_colors['opponent_wins']
        elif res == -1:
            background_color = background_colors['agent_wins']
        else:
            background_color = background_colors['draw']
        self._clear_screen(background_color=background_color)

        # Add gesture images
        for i, im in enumerate((self.images_60[round.opponent],
                                self.images_60[round.agent])):
            i_start = int(self.screen_size[0] / 2 - im.shape[0] / 2)
            i_end = i_start + im.shape[0]
            if i == 0:
                j_start = int(self.screen_size[1] * 3 / 4 - im.shape[1] / 2)
            else:
                j_start = int(self.screen_size[1] / 4 - im.shape[1] / 2)
                j_start0 = j_start
            j_end = j_start + im.shape[1]
            self.screen[i_start:i_end, j_start:j_end, :] = \
                im[:, :, None]

        # Add nb remaining rounds
        self._put_n_rounds_left(n_round_left=n_round_left,
                                location='bottomleft',
                                j_start=j_start0)
        # Add scores
        self._put_score(scores, location='topleft', j_start=j_start0)

        self._show_screen()

        # a = np.zeros((100, self.screen_size[1], 3))
        # a = np.arange(self.screen_size[1])/self.screen_size[1]*255
        # cv.imshow('toto',
        #     ([None, :, None])
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     pass

    def show_end_of_game(self, scores, display_wait_text):
        if scores['agent'] > scores['opponent']:
            self._clear_screen(background_colors['agent_wins'])
            text = 'Dommage!'
        elif scores['agent'] < scores['opponent']:
            self._clear_screen(background_colors['opponent_wins'])
            text = 'Bravo!'
        else:
            self._clear_screen(background_colors['draw'])
            text = 'Match nul!'
        cv.putText(img=self.screen,
                   text=text,
                   org=(int(self.screen_size[1] / 3),
                        int(self.screen_size[0] / 2)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=4,
                   color=(255, 255, 255),
                   thickness=4,
                   lineType=cv.LINE_AA)

        self._put_score(scores, location='top')

        if display_wait_text:
            cv.putText(img=self.screen,
                       text="(faites un geste pour lancer une nouvelle partie)",
                       org=(int(self.screen_size[1] * 0.1),
                            int(self.screen_size[0] * 0.9)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=2,
                       color=(255, 255, 255),
                       thickness=2,
                       lineType=cv.LINE_AA)

        self._show_screen()

    def show_back_end_of_game(self, scores, score_games, score_rounds,
                              recorded_games):
        if scores['agent'] > scores['opponent']:
            self._clear_screen(background_colors['agent_wins'])
            text = 'Perdu!'
        elif scores['agent'] < scores['opponent']:
            self._clear_screen(background_colors['opponent_wins'])
            text = 'Bravo!'
        else:
            self._clear_screen(background_colors['draw'])
            text = 'Match nul!'
        j_start = int(self.screen_size[1] * 0.1)
        cv.putText(img=self.screen,
                   text=text,
                   org=(j_start,
                        int(self.screen_size[0] * 0.5)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=2,
                   color=(255, 255, 255),
                   thickness=3,
                   lineType=cv.LINE_AA)
        self._put_score(scores,
                        location='topleft',
                        j_start=j_start)

        self._put_stats(scores=scores,
                        score_games=score_games,
                        score_rounds=score_rounds,
                        recorded_games=recorded_games)
        self._show_screen()

    def _put_stats(self, scores, score_games, score_rounds,
                   recorded_games=None):
        glob_score_games = {'agent': 0, 'opponent': 0, 'draw': 0}
        glob_score_rounds = {'agent': 0, 'opponent': 0}
        for k in score_games.keys():
            glob_score_games['agent'] += score_games[k]['agent']
            glob_score_games['opponent'] += score_games[k]['opponent']
            glob_score_games['draw'] += score_games[k]['draw']
        for k in score_rounds.keys():
            glob_score_rounds['agent'] += score_rounds[k]['agent']
            glob_score_rounds['opponent'] += score_rounds[k]['opponent']

        cv.putText(img=self.screen,
                   text='Totaux',
                   org=(int(self.screen_size[1] * 0.6),
                        int(self.screen_size[0] * 0.15)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=3,
                   color=(255, 255, 255),
                   thickness=3,
                   lineType=cv.LINE_AA)
        # Add score_games
        fontScale = 1.5
        thickness = 2
        n_played_games = glob_score_games['agent'] \
                         + glob_score_games['opponent']
        if n_played_games == 0:
            # First time we record games!
            n_played_games = -1
        ic = np.sqrt(np.log10(2/0.05)/(2*n_played_games))
        s = '{} parties gagnantes:'.format(n_played_games)
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.25)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)
        s = '  Humain {:.1%}    [{:.2f}]'\
            .format(glob_score_games['opponent'] / n_played_games,
                    ic*100)
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.35)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)
        s = '  Machine {:.1%}'\
            .format(glob_score_games['agent'] / n_played_games)
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.45)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)
        s = ' ' * 5 + '({} matchs nuls)'.format(glob_score_games['draw'])
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.55)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)

        # Add score_rounds
        fontScale = 1.5
        thickness = 2
        total_scores = {k: glob_score_rounds[k]+scores[k]
                        for k in scores.keys()}
        n_played_rounds = total_scores['agent'] + total_scores['opponent']
        ic = np.sqrt(np.log10(2/0.05)/(2*n_played_rounds))
        if n_played_rounds == 0:
            n_played_rounds = -1
        s = '{} rounds gagnants:'.format(n_played_rounds)
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.65)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)
        s = '  Humain {:.1%}    [{:.2f}]'.format(
            total_scores['opponent'] / n_played_rounds,
            ic * 100)
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.75)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)
        s = '  Machine {:.1%}'\
            .format(total_scores['agent'] / n_played_rounds)
        cv.putText(img=self.screen,
                   text=s,
                   org=(int(self.screen_size[1] * 0.5),
                        int(self.screen_size[0] * 0.85)),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=fontScale,
                   color=(255, 255, 255),
                   thickness=thickness,
                   lineType=cv.LINE_AA)
        if recorded_games is not None:
            # TODO update with number of draws in current game (refactor
            # this function?)
            n_draws = np.sum([1
                              for g in recorded_games
                              for r in g
                              if r.get_agent_gain() == 0])
            s = ' ' * 5 + '({} rounds nuls)'.format(n_draws)
            cv.putText(img=self.screen,
                       text=s,
                       org=(int(self.screen_size[1] * 0.5),
                            int(self.screen_size[0] * 0.95)),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=fontScale,
                       color=(255, 255, 255),
                       thickness=thickness,
                       lineType=cv.LINE_AA)

if __name__ == '__main__':
    import time
    from shifumy_demo_cv.main import load_games, print_all_scores

    game_file = '2018-09-28_NuitChercheurs_recorded_games.pickle'
    recorded_games, score_rounds, score_games = load_games(game_file)

    scores = {'opponent': 10, 'agent': 15}
    # score_games = {'opponent': 20, 'agent': 30}
    # score_rounds = {'opponent': 200, 'agent': 300}
    reverse_scores = {'opponent': scores['agent'], 'agent': scores['opponent']}
    n_round_left = 24
    main_window = CvShow(win_name='Main window', win_size=(900, 1440))
    main_window.agent_name = 'Oliv-IA'

    main_window.show_back_end_of_game(scores=scores,
                                      score_games=score_games,
                                      score_rounds=score_rounds,
                                      recorded_games=recorded_games)
    time.sleep(100)

    main_window.show_agent_result(Round(opponent=ROCK, agent=ROCK),
                                  scores=scores,
                                  n_round_left=n_round_left)
    time.sleep(2)

    main_window.show_center_text('Bonjour!')
    time.sleep(2)

    nb_round_choice = {ROCK: 20, PAPER: 40, SCISSORS: 60,}
    nb_round_choice_str = {k: '{} rounds'.format(v)
                           for k, v in nb_round_choice.items()}
    main_window.show_choose_3_options(
        title="Faites un geste pour choisir le nombre de rounds",
        rps_options=nb_round_choice_str)
    time.sleep(2)

    rps_players_names = {ROCK: 'Oliv-IA',
                         PAPER: 'KilIAs',
                         SCISSORS: 'AI-Capone'}
    main_window.show_choose_3_options(
        title="Faites un geste pour choisir votre adversaire",
        rps_options=rps_players_names)
    time.sleep(2)

    main_window.show_wait_gesture(scores=scores, n_round_left=n_round_left)
    time.sleep(2)
    main_window.show_round_result(Round(opponent=ROCK, agent=PAPER),
                                  scores=scores,
                                  n_round_left=n_round_left,
                                  score_games=score_games,
                                  score_rounds=score_rounds)

    time.sleep(2)
    main_window.show_round_result(Round(opponent=PAPER, agent=ROCK),
                                  scores=scores,
                                  n_round_left=n_round_left,
                                  score_games=score_games,
                                  score_rounds=score_rounds)

    time.sleep(2)
    main_window.show_round_result(Round(opponent=ROCK, agent=ROCK),
                                  scores=scores,
                                  n_round_left=n_round_left,
                                  score_games=score_games,
                                  score_rounds=score_rounds)


    time.sleep(2)
    main_window.show_end_of_game(scores=scores)

    time.sleep(2)
    main_window.show_end_of_game(scores=reverse_scores)


