# coding: utf8

import matplotlib.pyplot as plt

from ....base import Round

from ..defs import get_index_next_separator\
                  , get_index_second_separator\
                  , get_id_game_from_line\
                  , test_format_line\
                  , path_graph

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
