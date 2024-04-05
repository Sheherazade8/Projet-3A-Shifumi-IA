# coding: utf8

import sys
import math
import numpy

from .module.Node import Node
from .module.History import History
from .agent.Agent import ConfidentPstAgent
from ._cross_validation import validation, write_win_lose_draw_results_in_file\
                                , play_sequence, get_wld_agent_in_history


from .defs import path_datasets, path_misc_crossvalid_maxlb, list_data_file

###############################################################################
def cross_valid_beta(beta, history):

    agent = ConfidentPstAgent(beta)

    nb_game = len(history.list)
    third = math.floor(nb_game/3)
    hist1, hist2, hist3 = History(), History(), History()
    hist1.list = history.list[:third]
    hist2.list = history.list[third:2*third]
    hist3.list = history.list[2*third:]
    wld1 = validation(agent, hist1, hist2, hist3)
    wld2 = validation(agent, hist2, hist3, hist1)
    wld3 = validation(agent, hist3, hist1, hist2)
    validation_path = path_misc_crossvalid_maxlb[:-4] + "_beta.txt"
    validation_file = open(validation_path, "a")
    winrate = 0
    validation_file.write("\nbeta = %lf\n" % beta)
    winrate += write_win_lose_draw_results_in_file(wld1, validation_file)
    winrate += write_win_lose_draw_results_in_file(wld2, validation_file)
    winrate += write_win_lose_draw_results_in_file(wld3, validation_file)
    winrate = winrate/3
    validation_file.write("\nwinrate = %lf\n\n" % winrate)
    validation_file.close()

print("Which data to use ? (name.txt)")
print(list_data_file)
data_file_name = input()
while data_file_name not in list_data_file:
    print("Error: %s not in list_data_file (defs.py)" % data_file_name)
    print(list_data_file)
    data_file_name = input()

path_data_file = path_datasets + data_file_name

data_file = open(path_data_file, "r")
history = History()
history.read_from_file(data_file)
data_file.close()

min = input("Enter min: ")
max = input("Enter max: ")
scale = input("Enter scale: ")

for value in numpy.arange(float(min), float(max), float(scale)):
    beta = math.pow(2, value)
    cross_valid_beta(beta, history)
#beta = math.pow(2, -9)
#cross_valid_beta(beta, history)
