# coding: utf8

import sys
import os
from ...base import ROCK, PAPER, SCISSORS, Round, RESOURCES_PATH


# path to graph
path_graph = RESOURCES_PATH + "/graph/"

# path to datasets
path_datasets = RESOURCES_PATH + "/data/datasets/"
path_alldata = path_datasets + "alldata.txt"
path_data = path_datasets + "data.txt"
path_dataraw= path_datasets + "dataraw.txt"

# path to tree folder
path_tree               = os.path.join(RESOURCES_PATH,"data")
path_tree_1              = os.path.join(path_tree,"models")
path_tree_2              = os.path.join(path_tree_1,"tree")

path_tree_data          = path_tree + "from_data.txt"
path_tree_readable_data = path_tree + "from_readable_data.txt"
path_tree_alldata       = path_tree + "from_alldata.txt"

path_pst           = os.path.join(path_tree_1 , "pst_file.txt")

path_pst_ns        = os.path.join(path_tree_1 , "pst_ns_file.txt")

# path to misc folder
path_misc                     = RESOURCES_PATH + "/misc/"
path_misc_crossvalid_lastnode = path_misc\
                                + "crossvalid_lastnode/crossvalid_lastnode.txt"
path_misc_crossvalid_maxlb    = path_misc\
                                + "crossvalid_maxlb/crossvalid_maxlb.txt"
path_misc_crossvalid_maxlb_beta_plot = RESOURCES_PATH\
                + "/misc/crossvalid_maxlb/crossvalid_maxlb_beta_plot.txt"


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
