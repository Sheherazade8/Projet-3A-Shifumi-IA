# coding: utf8

import numpy
import math
import matplotlib.pyplot as plt

from .module.Node import Node
from .module.History import History
from .defs\
    import list_data_file, path_datasets, path_misc_crossvalid_maxlb_beta_plot\
           , path_graph
from ._format_dataraw_to_data import format_dataraw

def plot_winrate_per_beta():
    data_file = open(path_misc_crossvalid_maxlb_beta_plot, "r")
    list_lines = data_file.readlines()
    list_y = []
    id = 1
    for line in list_lines:
        if id % 14 == 0:
            winrate = float(line[10:18])
            list_y.append(winrate)
        id += 1
    list_x = []
    for value in numpy.arange(-10,-5,0.1):
                list_x.append(math.pow(2, value))
    plt.plot(list_x, list_y)
    plt.xlabel("Beta")
    plt.ylabel("Winrate")
    plt.title("Winrate evolution with Beta variation")
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    plt.margins(0, 0.1)
    path_save_file = path_graph + "Winrate_Beta.png"
    plt.savefig(path_save_file)
    plt.show()


print("Enter a data file or press enter:")
print(list_data_file)
data_file_name = input()
if data_file_name is "":
    path_data_file = format_dataraw()
    length_path = len(path_datasets)
    data_file_name = path_data_file[length_path:]
elif data_file_name not in list_data_file:
    print("Error: %s not in dict_data_file (defs.py)")
    exit()
else:
    path_data_file = path_datasets + data_file_name

data_file = open(path_data_file, "r")
history = History()
history.read_from_file(data_file)
data_file.close()

root = Node()
root.learn_from_history(history)
#root.pruning_depth_max(3)
root.pruning_gain_max()

print("nb_round = %d" % history.length)
print("nb_game = %d" % len(history.list))
plot = input("Plot NbGame/Length ? (y or n) ")
if plot == "y":
    history.plot_nb_game_per_length()
print("Tree_depth = %d" % root.get_max_depth())
plot = input("Plot NbData/Depth ? (y or n) ")
if plot == "y":
    root.plot_nb_data_learn_per_depth()
plot = input("Plot Child/Depth ? (y or n) ")
if plot == "y":
    root.plot_percentage_child_per_depth()
plot = input("Plot Winrate/Beta ? (y or n) ")
if plot == "y":
    plot_winrate_per_beta()
