# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""
import pickle
import socket
import time
import threading
from pathlib import Path

from shifumy_player.base import \
    Round, str_rps, rps_from_str, ROCK, PAPER, SCISSORS, RESOURCES_PATH
from shifumy_player.players.kilias_player import KiliasPlayer
from shifumy_player.players.random_player import RandomPlayer
from shifumy_player.players.ve_players.bandits \
    import UpdateAllMetaAgent, UpdateAllNsMetaAgent

# DEFAULT_HOST = '169.254.64.201'  # Wifi
# DEFAULT_HOST = '169.254.11.179'  # Ehternet
DEFAULT_HOST = '0.0.0.0'  # Ehternet
DEFAULT_PORT = 50000
auto_play = False
n_games = 5


def load_games(filename):
    try:
        with open(str(Path(RESOURCES_PATH) / filename), 'rb') as file:
            data = pickle.load(file)
            games = data['games']
            score_rounds = data['score_rounds']
            score_games = data['score_games']
            print('{} anciennes parties chargées'.format(len(games)))
    except Exception as e:
        print('Remise à zéro des scores')
        games = []
        score_rounds = dict()  # {'agent': 0, 'opponent': 0}
        score_games = dict()  # {'agent': 0, 'opponent': 0, 'draw': 0}
    return games, score_rounds, score_games


def save_games(filename, games, score_rounds, score_games):
    data = {
        'games': games,
        'score_rounds': score_rounds,
        'score_games': score_games,
    }
    with open(str(Path(RESOURCES_PATH) / filename), 'wb') as file:
        pickle.dump(data, file)
        print('{} parties sauvegardées'.format(len(games)))


def play_one_game(player, n_rounds, gesture_recognition_server):
    # todo regrouper ceci avec play_one_game_cv
    score_agent = 0
    score_opponent = 0
    game = []
    for i_round in range(n_rounds):
        print('#' * 40)
        print('Round {} / {}'.format(i_round + 1, n_rounds))
        print('Jouez!')
        g_agent = player.predict_agent_gesture()
        if auto_play:
            g_opponent = player.predict_agent_gesture()
        else:
            g_opponent = gesture_recognition_server.wait_gesture()
        round = Round(opponent=g_opponent, agent=g_agent)
        print(round)
        gain_agent = round.get_agent_gain()
        if gain_agent > 0:
            score_agent += gain_agent
        elif gain_agent < 0:
            score_opponent -= gain_agent

        game.append(round)
        player.record(round)
        print('Résultat:')
        print('Humain {} - {} Machine'.format(score_opponent, score_agent))

        gesture_recognition_server.wait_end_of_gesture()

    return game, score_agent, score_opponent


def play_one_game_cv(player, n_rounds, gesture_recognition_server,
                     main_window, back_window,
                     score_games, score_rounds):
    scores = {'agent': 0, 'opponent': 0}
    game = []
    for i_round in range(n_rounds):
        print('#' * 40)
        print('Round {} / {}'.format(i_round + 1, n_rounds))
        print('Jouez!')
        main_window.show_wait_gesture(scores=scores,
                                      n_round_left=n_rounds - i_round,
                                      location='left')
        g_agent = player.predict_agent_gesture()
        back_window.show_backstage(agent_gesture=g_agent,
                                   scores=scores,
                                   n_round_left=n_rounds - i_round,
                                   score_games=score_games,
                                   score_rounds=score_rounds)
        if auto_play:
            g_opponent = player.predict_agent_gesture()
        else:
            g_opponent = gesture_recognition_server.wait_gesture()
        round = Round(opponent=g_opponent, agent=g_agent)
        print(round)
        gain_agent = round.get_agent_gain()
        if gain_agent > 0:
            scores['agent'] += 1
        elif gain_agent < 0:
            scores['opponent'] += 1

        game.append(round)
        player.record(round)
        print('Résultat:')
        print('Humain {} - {} Machine'
              .format(scores['opponent'], scores['agent']))

        main_window.show_agent_result(round,
                                      scores=scores,
                                      n_round_left=n_rounds-i_round)
        back_window.show_round_result(round,
                                      scores=scores,
                                      n_round_left=n_rounds-i_round,
                                      score_games=score_games,
                                      score_rounds=score_rounds)
        gesture_recognition_server.wait_end_of_gesture()

    return game, scores


class GestureRecognitionServer:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.connexion = None
        self.lock = threading.Condition()
        # 1) création du socket :
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) liaison du socket à une adresse précise :
        while True:
            try:
                self.mySocket.bind((host, port))
                print(self.mySocket.getsockname())
                break
            except socket.error:
                print("La liaison du socket à l'adresse choisie a échoué.")
                print(socket.error)
                time.sleep(1)
                print('Retrying...')


    def wait_client_connection(self):
        # 3) Attente de la requête de connexion d'un client :
        print("Serveur prêt, en attente de connection du client ...")
        self.mySocket.listen(2)

        # 4) Etablissement de la connexion :
        self.connexion, adresse = self.mySocket.accept()
        print("Client connecté, adresse IP {}, port {}"
              .format(adresse[0], adresse[1]))


    def handle_gesture(self, msgClient=None):
        valid_gestures = ['rock', 'paper', 'scissors']
        if msgClient and msgClient in valid_gestures:
            return rps_from_str(msgClient)
        else:
            print(f"Invalid gesture received: {msgClient}")
            return(ROCK)
    
    def wait_gesture(self, expected_gesture=None):
        # 5) Dialogue avec le client :
        if expected_gesture is None:
            msgServeur = "Wait gesture"
        else:
            msgServeur = "Wait gesture:{}".format(expected_gesture)
        print(msgServeur)
        self.connexion.send(msgServeur.encode("Utf8"))
        msgClient = self.connexion.recv(1024).decode("Utf8")
        print('Received {}'.format(msgClient))
        return rps_from_str(msgClient)


    def wait_end_of_gesture(self):
        """
        Block until EOG signal is received through socket.

        EOG signals means that the player has removed his hand from the camera.
        :return:
        """
        # 5) Dialogue avec le client :
        self.lock.acquire()
        try:
            msgServeur = "Wait end"
            self.connexion.send(msgServeur.encode("Utf8"))
            msgClient = self.connexion.recv(1024).decode("Utf8")
            print('Received {}'.format(msgClient))
            if msgClient == "EOG":
                return
            else:
                raise ValueError('End of gesture not detected ({})'
                                .format(msgClient))
        finally:
            self.lock.release()


    def close_connection(self):
        self.connexion.close()
        print("Connexion fermée.")


def main_loop_terminal():
    # todo regrouper ceci avec main_loop_cv
    # Set up
    game_file = 'recorded_games.pickle'
    recorded_games, score_rounds, score_games = load_games(game_file)
    gesture_recognition_server = GestureRecognitionServer()
    gesture_recognition_server.wait_client_connection()
    
    n_rounds = 20

    i_game = 0
    while True:
        print('*' * 80)
        print('Nouvelle partie')

        # Choose a player
        # TODO replace random player by list of available players
        print('Joueur aléatoire')
        player = RandomPlayer.load()


        # Play
        game, score_agent, score_opponent = play_one_game(
            player=player,
            n_rounds=n_rounds,
            gesture_recognition_server=gesture_recognition_server)

        # Update and display results
        recorded_games.append(game)
        score_rounds['agent'] += score_agent
        score_rounds['opponent'] += score_opponent
        if score_agent > score_opponent:
            print('La machine a gagné!')
            score_games['agent'] += 1
        elif score_agent < score_opponent:
            print("L'humain a gagné!")
            score_games['opponent'] += 1
        else:
            print('Match nul!')
            score_games['draw'] += 1
        print('Score globaux:')
        n_played_rounds = score_rounds['agent']+score_rounds['opponent']
        print('{} rounds: Humain {:.1%} - {:.1%} Machine'
              .format(n_played_rounds,
                      score_rounds['opponent'] / n_played_rounds,
                      score_rounds['agent'] / n_played_rounds))
        n_played_games = score_games['agent'] \
                         + score_games['opponent'] \
                         + score_games['draw']
        print('{} parties: Humain {:.1%} - {:.1%} Machine - {:.1%} Nuls'
              .format(n_played_games,
                      score_games['opponent'] / n_played_games,
                      score_games['agent'] / n_played_games,
                      score_games['draw'] / n_played_games))

        # Record game
        save_games(game_file, recorded_games, score_rounds, score_games)

        i_game += 1
        if auto_play and i_game >= n_games:
            break

from shifumy_demo_cv.cv_show import CvShow


def main_loop_cv(main_win_size=(1080, 1920), back_win_size=(900, 1440)):
    """
    Start the program.

    Load old recorded games file.
    Start gesture recognition server.
    Setup main and back windows.
    Do training.
    Select player options.
    Start game.


    Notes:
    - Window size are formated as (height, width)

    :param main_win_size: size of the main screen, shown to the player
    :param back_win_size:  size of the back screen, shown to the public
    :return:
    """
    # Set up
    game_file = 'recorded_games.pickle'
    recorded_games, score_rounds, score_games = load_games(game_file)
    gesture_recognition_server = GestureRecognitionServer()
    try:
        gesture_recognition_server.wait_client_connection()

        # get map between gesture and artificial player
        rps_players = get_rps_players()

        for p in rps_players.values():
            if p['id'] not in score_rounds.keys():
                score_rounds[p['id']] = {'agent': 0, 'opponent': 0}
            if p['id'] not in score_games.keys():
                score_games[p['id']] = {'agent': 0, 'opponent': 0, 'draw': 0}


        

        # the two screens may not have the same size: change those lines according to your configuration

        # self.screen_size = np.array((1080, 1920))
        main_window = CvShow(win_name='Main window',
                             win_size=main_win_size,
                             move_xy=(0, back_win_size[0]))
        back_window = CvShow(win_name='Back window',
                             win_size=back_win_size,
                             move_xy=(0, 0))

        i_game = 0
        while True:
            print('*' * 80)
            print('Nouvelle partie')

            # Choose a player
            rps_players_names = {k: v['name'] for k, v in rps_players.items()}
            for win in (main_window, back_window):
                win.show_choose_3_options(
                    title="Faites un geste pour choisir votre adversaire",
                    rps_options=rps_players_names)
                
            g = gesture_recognition_server.handle_gesture()
            if g is not None:
                player = rps_players[g]['player']
            else:
                print("Invalid gesture received.")
            
            player = rps_players[g]['player']
            player_id = rps_players[g]['id']
            print('Player:', rps_players[g]['name'])
            main_window.agent_name = rps_players[g]['name']
            back_window.agent_name = rps_players[g]['name']
            for win in (main_window, back_window):
                win.show_center_text('Joueur choisi: ' + rps_players[g]['name'])

            #gesture_recognition_server.wait_end_of_gesture()


            nb_round_choice_str = 20

            # Choose a number of round
            nb_round_choice = {
                ROCK: 20,
                PAPER: 40,
                SCISSORS: 60,
            }


            g = gesture_recognition_server.handle_gesture()
            n_rounds = nb_round_choice[g]
            print('n_round = {}'.format(n_rounds))
            for win in (main_window, back_window):
                win.show_center_text('Partie en {} rounds!'.format(n_rounds))
            #gesture_recognition_server.wait_end_of_gesture()

            # Play
            game, scores = play_one_game_cv(
                player=player,
                n_rounds=n_rounds,
                gesture_recognition_server=gesture_recognition_server,
                main_window=main_window,
                back_window=back_window,
                score_games=score_games,
                score_rounds=score_rounds)

            # Update and display results
            recorded_games.append(game)
            score_rounds[player_id]['agent'] += scores['agent']
            score_rounds[player_id]['opponent'] += scores['opponent']
            if scores['agent'] > scores['opponent']:
                print('La machine a gagné!')
                score_games[player_id]['agent'] += 1
            elif scores['agent'] < scores['opponent']:
                print("L'humain a gagné!")
                score_games[player_id]['opponent'] += 1
            else:
                print('Match nul!')
                score_games[player_id]['draw'] += 1
            print('Score globaux:')
            n_played_rounds = score_rounds[player_id]['agent'] \
                              + score_rounds[player_id]['opponent']
            print('{} rounds: Humain {:.1%} - {:.1%} Machine'
                  .format(n_played_rounds,
                          score_rounds[player_id]['opponent'] / n_played_rounds,
                          score_rounds[player_id]['agent'] / n_played_rounds))
            n_played_games = score_games[player_id]['agent'] \
                             + score_games[player_id]['opponent'] \
                             + score_games[player_id]['draw']
            print('{} parties: Humain {:.1%} - {:.1%} Machine - {:.1%} Nuls'
                  .format(n_played_games,
                          score_games[player_id]['opponent'] / n_played_games,
                          score_games[player_id]['agent'] / n_played_games,
                          score_games[player_id]['draw'] / n_played_games))

            # Record game
            save_games(game_file, recorded_games, score_rounds, score_games)

            # Display end of game
            main_window.show_end_of_game(scores=scores, display_wait_text=False)
            back_window.show_back_end_of_game(scores=scores,
                                              score_games=score_games,
                                              score_rounds=score_rounds,
                                              recorded_games=recorded_games)
            print_all_scores(score_games, score_rounds)

            # Reload players for next game (
            rps_players = get_rps_players()
            main_window.show_end_of_game(scores=scores, display_wait_text=True)

            # Wait gesture to init next game
            gesture_recognition_server.handle_gesture()
            for win in (main_window, back_window):
                win.show_center_text('Shifumi-IA!')
            gesture_recognition_server.wait_end_of_gesture()

            i_game += 1
            if auto_play and i_game >= n_games:
                break
    finally:
        gesture_recognition_server.mySocket.close()


def print_all_scores(score_games, score_rounds):
    glob_score_games = {'agent': 0, 'opponent': 0, 'draw': 0}
    glob_score_rounds = {'agent': 0, 'opponent': 0}
    for k in score_games.keys():
        glob_score_games['agent'] += score_games[k]['agent']
        glob_score_games['opponent'] += score_games[k]['opponent']
        glob_score_games['draw'] += score_games[k]['draw']
    for k in score_rounds.keys():
        glob_score_rounds['agent'] += score_rounds[k]['agent']
        glob_score_rounds['opponent'] += score_rounds[k]['opponent']
    n_played_games = glob_score_games['agent'] \
                     + glob_score_games['opponent'] \
                     + glob_score_games['draw']
    n_played_rounds = glob_score_rounds['agent'] \
                      + glob_score_rounds['opponent']

    print('*' * 80)
    print('Scores globaux:')

    print('{} parties:'.format(n_played_games))
    for k in glob_score_games.keys():
        print('  - {}: {:.1%}'.format(k, glob_score_games[k]/n_played_games))
    print('{} rounds gagnants:'.format(n_played_rounds))
    for k in glob_score_rounds.keys():
        print('  - {}: {:.1%}'.format(k, glob_score_rounds[k]/n_played_rounds))

    print('*' * 80)
    print('Scores par agent:')

    for k_agent in score_games.keys():
        print(k_agent)
        n_played_games = score_games[k_agent]['agent'] \
                         + score_games[k_agent]['opponent']
        n_played_rounds = score_rounds[k_agent]['agent'] \
                          + score_rounds[k_agent]['opponent']
        if n_played_games == 0:
            print('no game recorded')
            continue
        print('  * {} parties gagnantes:'.format(n_played_games))
        print('    - Humain: {:.1%}'.format(
            score_games[k_agent]['opponent'] / n_played_games))
        print('    - Machine: {:.1%}'.format(
            score_games[k_agent]['agent'] / n_played_games))
        print('      ({} matchs nuls)'.format(score_games[k_agent]['draw']))
        print('  * {} rounds gagnants:'.format(n_played_rounds))
        print('    - Humain: {:.1%}'.format(
            score_rounds[k_agent]['opponent'] / n_played_rounds))
        print('    - Machine: {:.1%}'.format(
            score_rounds[k_agent]['agent'] / n_played_rounds))


def get_rps_players():
    """
    Return a mapping between gesture and artificial player infos:

    {gesture: {name:?, player:?, id:?}}

    :return: dict
    """
    rps_players = {
        ROCK: {'name': 'Oliv-IA', 'player': UpdateAllNsMetaAgent.load()},
        PAPER: {'name': 'KilIAs', 'player': KiliasPlayer.load()},
        SCISSORS: {'name': 'AI-Capone', 'player': UpdateAllMetaAgent.load()},
        # SCISSORS: {'name': 'AI-Capone', 'player': SgdLogRegAgent.load()},
    }
    # build id for each player (to be used to store scores)
    for g in rps_players.keys():
        rps_players[g]['id'] = str(type(rps_players[g]['player']))
    return rps_players


if __name__ == '__main__':
    main_loop_cv()
    # main_loop_terminal()
