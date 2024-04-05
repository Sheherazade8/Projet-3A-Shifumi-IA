# coding: utf8

#sys.setrecursionlimit(314000)

from shifumy_player.players.pst_player.module.Node\
    import NodeNS
from shifumy_player.players.pst_player.module.History\
    import History
from shifumy_player.players.pst_player._format_dataraw_to_data\
    import format_dataraw
from shifumy_player.players.pst_player.defs\
    import list_data_file, path_datasets

#############################################################################

print("Enter a data file or press enter:")
print(list_data_file)
data_file_name = 'alldata.txt'
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
list_line = data_file.readlines()
data_file.seek(0)
history = History()
history.read_from_file(data_file)
print("History created")
data_file.close()


root = NodeNS(alpha=0.123)
root.learn_from_history(history)

pruning = ""
# pgm = input("pruning_gain_max ? (y or n)\n")
pgm = "y"
if pgm == "y":
    root.pruning_gain_max()
    pruning = "pgm"
else:
    depth = input("Enter a depth for pruning or just press enter\n")
    max_depth = root.get_max_depth()
    if "0" <= depth <= str(max_depth):
        root.pruning_depth_max(int(depth))
        pruning = "pdm_" + str(depth)

nb_node = root.get_number_node()

total_sequence = history.get_nb_subsequence_total()
print("Number of Node = %d" % nb_node)
print("Number of Move = %d" % root.get_number_gesture_learn())
print("%d Data used" % total_sequence)

root.save_tree()


#############################################################################
