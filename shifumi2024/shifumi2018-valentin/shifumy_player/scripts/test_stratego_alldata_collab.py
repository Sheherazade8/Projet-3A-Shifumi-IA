# -*- coding: utf-8 -*-

import numpy as np

import sys
import math

import os

ROCK = np.uint8(0)
PAPER = np.uint8(1)
SCISSORS = np.uint8(2)

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
        #print("******* New Round=",self.opponent,self.agent)

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

    def predict(self):
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

# constant
SEPARATOR = ","
beats = { ROCK : PAPER, PAPER : SCISSORS, SCISSORS : ROCK }
correspondance_gesture_dataraw = { "1" : ROCK, "2" : PAPER, "3" : SCISSORS }
list_data_file = ["data.txt", "alldata.txt"]

###############################################################################

def get_index_next_separator(line, current_index = -1):
    id_separator = line.find(SEPARATOR, current_index+1)
    return id_separator

def get_index_second_separator(line):
    id_separator = get_index_next_separator(line)
    id_separator = get_index_next_separator(line, id_separator)
    return id_separator

def get_id_game_from_line(line):
    id_separator = get_index_next_separator(line)
    str_idgame = line[:id_separator]
    id_game = int(str_idgame)
    return id_game

def test_format_line(line):
    id_sep = get_index_next_separator(line)
    if id_sep == -1:
        print("Wrong data format")
        exit()

def Predict_Move(root, history):
    current_node = root.get_child_from_game(history)
    return current_node.Move_MaxExpectation()

def print_round(round):
    print("opponent = %d" % round.opponent)
    print("agent = %d" % round.agent)

def print_game(game):
    for round in game:
        print_round(round)

def print_history(history):
    for game in history.list:
        print_game(game)

class History:

    def __init__(self):
        self.list = []

    def add_round(self, round, game):
        assert(isinstance(round, Round))
        self.list[game].append(round)

    def convert_lines_to_list(self, list_line):
        print("nb line = %d" % len(list_line))
        list_data = []
        game = []
        id_game = get_id_game_from_line(list_line[0])
        for line in list_line:
            if get_id_game_from_line(line) != id_game:
                id_game = get_id_game_from_line(line)
                list_data.append(game)
                game = []
            opponent = first_gesture(line)
            agent = second_gesture(line)
            game.append(Round(opponent, agent))
        list_data.append(game)
        return list_data

    def read_from_file(self, data_fromfile):
        list_line = data_fromfile.readlines()
        test_format_line(list_line[0])
        print("Format: check")
        self.list = self.convert_lines_to_list(list_line)
        print("File: convert")

    @property
    def length(self):
        length = 0
        for game in self.list:
            length += len(game)
        return length

    def get_nb_subsequence_in_game(self, game):
        length = len(self.list[game])
        return length*(length+1)/2

    def get_nb_subsequence_total(self):
        nb_game = len(self.list)
        nb_subsequence = 0
        for id_game in range(nb_game):
            nb_subsequence += self.get_nb_subsequence_in_game(id_game)
        return nb_subsequence

    def get_length_longest_game(self):
        length_max = 0
        for game in self.list:
            if length_max < len(game):
                length_max = len(game)
        return length_max

    def get_nb_game_of_length(self, length):
        nb_game = 0
        for game in self.list:
            if length == len(game):
                nb_game += 1
        return nb_game

    def get_list_nb_game_per_length(self):
        list_nbgame = []
        length_max = self.get_length_longest_game()
        for length in range(length_max+1):
            nb_game = self.get_nb_game_of_length(length)
            list_nbgame.append(nb_game)
        print(list_nbgame)
        return list_nbgame

    def plot_nb_game_per_length(self):
        list_nbgame = self.get_list_nb_game_per_length()
        length_max = len(list_nbgame)
        plt.figure(figsize = (13.66, 6.10))
        plt.bar(range(length_max), list_nbgame)
        plt.xlabel("Length")
        plt.ylabel("Number of Game")
        plt.title("Number of Game / Length")
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
        plt.margins(0, 0.1)
        path_save_file = path_graph + "Game_Length.png"
        plt.savefig(path_save_file)
        plt.show()

    def get_sum_previous_game_length(self, index_game):
        current_index = 0
        sum = 0
        for game in self.list[:index_game]:
            sum += len(game)
        return sum

###############################################################################


def first_gesture(line):
    id_separator = get_index_second_separator(line)
    return int(line[id_separator+1])

def second_gesture(line):
    id_separator = get_index_second_separator(line)
    return int(line[id_separator+3])

class StrategoPlayer(RpsAgent):

    def __init__(self, c = 50, f = 5, scale = 5):
        RpsAgent.__init__(self)
        self.repeatWin  = 0
        self.repeatLose = 0
        self.repeatDraw = 0
        self.upWin   = 0
        self.upLose  = 0
        self.upDraw  = 0
        self.downWin   = 0
        self.downLose  = 0
        self.downDraw  = 0
        self.old_go = None
        self.confidence  = c/100
        self.forget = f
        self.scale = scale/100

    def reset_game(self):
        super().reset_game()
        self.repeatWin  = 0
        self.repeatLose = 0
        self.repeatDraw = 0
        self.upWin   = 0
        self.upLose  = 0
        self.upDraw  = 0
        self.downWin   = 0
        self.downLose  = 0
        self.downDraw  = 0
        self.old_go = None

    def record(self, last_round):
        if len(self.game) > 1:
            go = self.game[-1].opponent
            result = self.game[-1].get_opponent_gain()
            if result == 1:
                if last_round.opponent == go:
                    if self.repeatWin < max(self.upWin,self.downWin) + self.forget:
                        self.repeatWin += 1
                elif last_round.opponent == beats[go]:
                    if self.upWin < max(self.repeatWin,self.downWin) + self.forget:
                        self.upWin += 1
                else:
                    if self.downWin < max(self.repeatWin,self.upWin) + self.forget:
                        self.downWin += 1
            elif result == 0:
                if last_round.opponent == go:
                    if self.repeatDraw < max(self.upDraw,self.downDraw) + self.forget:
                        self.repeatDraw += 1
                elif last_round.opponent == beats[go]:
                    if self.upDraw < max(self.repeatDraw,self.downDraw) + self.forget:
                        self.upDraw += 1
                else:
                    if self.downDraw < max(self.repeatDraw,self.upDraw) + self.forget:
                        self.downDraw += 1
            else:
                if last_round.opponent == go:
                    if self.repeatLose < max(self.upLose,self.downLose) + self.forget:
                        self.repeatLose += 1
                elif last_round.opponent == beats[go]:
                    if self.upLose < max(self.repeatLose,self.downLose) + self.forget:
                        self.upLose += 1
                else:
                    if self.downLose < max(self.repeatLose,self.upLose) + self.forget:
                        self.downLose += 1
            if self.old_go == last_round.opponent:
                if self.confidence < (100-self.scale)/100:
                    self.confidence += self.scale
                elif self.confidence < (100-self.scale/10)/100:
                    self.confidence += self.scale
            elif self.old_go != None:
                if self.confidence > self.scale:
                    self.confidence -= self.scale
                elif self.confidence > self.scale/10:
                    self.confidence -= self.scale/10
        self.confidence = round(self.confidence,6)
        super().record(last_round)

    def predict(self):
        proba = {ROCK : 1/3, PAPER : 1/3, SCISSORS : 1/3}
        value = np.random.random()
        if len(self.game) > 0:
            result = self.game[-1].get_opponent_gain()
            go = self.game[-1].opponent
            if result == 1:
                if self.repeatWin > max(self.upWin,self.downWin):
                    proba[beats[go]] +=  1/3 * self.confidence
                    proba[beats[beats[go]]] -= 1/3 * self.confidence
                elif self.upWin > max(self.repeatWin,self.downWin):
                    proba[beats[beats[go]]] += 1/3 * self.confidence
                    proba[go] -= 1/3 * self.confidence
                elif self.downWin > max(self.upWin,self.repeatWin):
                    proba[go] +=  1/3 * self.confidence
                    proba[beats[go]] -= 1/3 * self.confidence
            elif result == 0:
                if self.repeatDraw > max(self.upDraw,self.downDraw):
                    proba[beats[go]] +=  1/3 * self.confidence
                    proba[beats[beats[go]]] -= 1/3 * self.confidence
                elif self.upDraw > max(self.repeatDraw,self.downDraw):
                    proba[beats[beats[go]]] += 1/3 * self.confidence
                    proba[go] -= 1/3 * self.confidence
                elif self.downDraw > max(self.upDraw,self.repeatDraw):
                    proba[go] +=  1/3 * self.confidence
                    proba[beats[go]] -= 1/3 * self.confidence
            else:
                if self.repeatLose > max(self.upLose,self.downLose):
                    proba[beats[go]] +=  1/3 * self.confidence
                    proba[beats[beats[go]]] -= 1/3 * self.confidence
                elif self.upLose > max(self.repeatLose,self.downLose):
                    proba[beats[beats[go]]] += 1/3 * self.confidence
                    proba[go] -= 1/3 * self.confidence
                elif self.downLose > max(self.upLose,self.repeatLose):
                    proba[go] +=  1/3 * self.confidence
                    proba[beats[go]] -= 1/3 * self.confidence
        if proba[ROCK] == proba[PAPER] == proba[SCISSORS]:
            self.old_go = None
        elif proba[ROCK] > max(proba[PAPER],proba[SCISSORS]):
            self.old_go = SCISSORS
        elif proba[PAPER] > proba[SCISSORS]:
            self.old_go = ROCK
        else:
            self.old_go = PAPER
        if value < proba[ROCK]:
            return ROCK
        if value < proba[ROCK] + proba[PAPER]:
            return PAPER
        return SCISSORS

    def load(filename=None):
        assert filename is None
        return StrategoPlayer()

def write_win_lose_draw_results_in_file(wld, result_file):
    total = wld[0] + wld[1] + wld[2]
    winrate_total = wld[0]/total
    winrate_without_draw = wld[0]/(total - wld[2])
    result_file.write("(win, lose, draw) = %s\n" % wld)
    result_file.write("win/total = %lf\n" % winrate_total)
    result_file.write("winrate = %lf\n" % winrate_without_draw)
    return float(winrate_without_draw)

def play_sequence(agent, sequence):
    player_gesture = sequence[-1].opponent
    for round in sequence[:-1]:
        agent.predict_agent_gesture()
        agent.record(round)
    agent_gesture = agent.predict_agent_gesture()
    agent.reset_game()
    if agent_gesture == beats[player_gesture]:
        return 1
    if player_gesture == beats[agent_gesture]:
        return -1
    return 0

def get_wld_agent_in_history(agent, history):
    win_lose_draw = [0, 0, 0]
    for game in history.list:
        for id_round in range(1,len(game)):
            current_result = play_sequence(agent, game[:id_round])
            if current_result == 1:
                win_lose_draw[0] += 1
            elif current_result == -1:
                win_lose_draw[1] += 1
            else:
                win_lose_draw[2] += 1
    return win_lose_draw

def valid_stratego(history, file, confidence, forget, scale):
    agent = StrategoPlayer(confidence, forget, scale)
    wld = get_wld_agent_in_history(agent, history)
    file.write("\nconfidence = %lf, forget = %lf, scale = %lf" % (confidence, forget, scale))
    write_win_lose_draw_results_in_file(wld, file)

data_file = open("alldata.txt", "r")
history = History()
history.read_from_file(data_file)
data_file.close()

save_path = path_misc + "stratego_test.txt"
save_file = open("stratego_test.txt", "a")
save_file.write("\n\n\n")

for confidence in range(10, 90, 5):
    for forget in range(1, 10, 1):
        for scale in range(1, 10, 1):
            valid_stratego(history, save_file, confidence, forget, scale)
            print("confidence = %lf, forget = %lf, scale = %lf" % (confidence, forget, scale))
save_file.close()
