# coding: utf8

import sys
import math

from .module.Node import Node
from .module.History import History
from .agent.Agent import VariantPstAgent
from ._cross_validation import validation, write_win_lose_draw_results_in_file\
                                , play_sequence, get_wld_agent_in_history


from .defs import list_data_file, path_datasets, path_misc

###############################################################################

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

agent = VariantPstAgent()

for depth in range(2, 10, 1):

    agent.depth = depth
    nb_game = len(history.list)
    third = math.floor(nb_game/3)
    hist1, hist2, hist3 = History(), History(), History()
    hist1.list = history.list[:third]
    hist2.list = history.list[third:2*third]
    hist3.list = history.list[2*third:]
    wld1 = validation(agent, hist1, hist2, hist3)
    wld2 = validation(agent, hist2, hist3, hist1)
    wld3 = validation(agent, hist3, hist1, hist2)
    validation_path = path_misc + "crossvalid_variant/crossvalid_variant_"\
                      + str(depth) + ".txt"
    validation_file = open(validation_path, "w")
    winrate = 0
    winrate += write_win_lose_draw_results_in_file(wld1, validation_file)
    winrate += write_win_lose_draw_results_in_file(wld2, validation_file)
    winrate += write_win_lose_draw_results_in_file(wld3, validation_file)
    winrate = winrate/3
    validation_file.write("\nwinrate = %lf" % winrate)
    validation_file.close()
