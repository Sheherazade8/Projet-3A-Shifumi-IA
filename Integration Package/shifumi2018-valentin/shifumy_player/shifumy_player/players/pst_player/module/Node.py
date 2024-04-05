# coding: utf8

import matplotlib.pyplot as plt
import json
import jsonpickle
import jsonpickle.util as util
import sys
import numpy
import math
import random
import os

from ..defs import beats, path_tree_1, path_graph, path_tree_2

#path_base = '/home/kaamelott/Bureau/L1/Stage_Qarma/Git/shifumi2018/shifumy'
#sys.path.append(path_base)
from ....base import ROCK, PAPER, SCISSORS, Round, str_rps

jsonpickle.set_preferred_backend('simplejson')
sys.setrecursionlimit(314000)


class Node:

    def __init__(self):
        self.nb_rps = { str(ROCK) : 0, str(PAPER) : 0, str(SCISSORS) : 0 }
        self.children = {}

    def update_from_dict(self, node_dict):
        self.__dict__.update(node_dict)
        for child in list(self.children.values()):
            dict = child
            node = Node()
            child = node.update_from_dict(dict)

    def learn_gesture(self, gesture):
        assert (gesture == ROCK or
                gesture == PAPER or
                gesture == SCISSORS)
        gesture = str(gesture)
        self.nb_rps[gesture] += 1

    def add_child_from_round(self, round):
        name = round.key
        if name not in self.children.keys():
            self.children[name] = Node()

    def get_child_from_round(self, round):
        name = round.key
        if name in self.children.keys():
            return self.children[name]
        return 0

    def learn_sequence(self, sequence):
        node = self
        gesture_tolearn = sequence[-1].opponent
        id_round = len(sequence) - 2
        while id_round >= 0:
            current_round = sequence[id_round]
            node.learn_gesture(gesture_tolearn)
            node.add_child_from_round(current_round)
            node = node.get_child_from_round(current_round)
            id_round -= 1
        node.learn_gesture(gesture_tolearn)

    def learn_game(self, game):
        length_game = len(game)
        for id_round in range(length_game):
            sequence = game[:id_round+1]
            self.learn_sequence(sequence)

    def learn_from_history(self, history):
        for game in history.list:
            self.learn_game(game)

    def get_sum_rps(self):
        sum = 0
        for gesture in list(self.nb_rps.keys()):
            sum += self.nb_rps[gesture]
        return sum

    def get_number_gesture_learn(self, nb_round = 0):
        stack = [self,]
        size = len(stack)
        nb_round = 0
        while size > 0:
            node = stack.pop()
            nb_round += node.get_sum_rps()
            for child in node.children.values():
                stack.append(child)
            size = len(stack)
        return nb_round

    def get_number_node(self):
        stack = [self,]
        size = len(stack)
        nb_node = 0
        while size > 0:
            node = stack.pop()
            nb_node += 1
            for child in node.children.values():
                stack.append(child)
            size = len(stack)
        return nb_node

    def get_gesture_with_max_value(self):
        list_keys = list(self.nb_rps.keys())
        list_values = list(self.nb_rps.values())
        return list_keys[list_values.index(max(list_values))]

    def get_child_from_game(self, game):
        length = len(game)
        current_node = self
        for id_round in reversed(range(length)):
            round = game[id_round]

            if isinstance(current_node, Node):
                current_node = current_node
            else:
                root = Node()
                root.update_from_dict(current_node)
                current_node = root
                assert (isinstance(root, Node))

            assert (isinstance(current_node, Node))

            child = current_node.get_child_from_round(round)

            if child is 0:
                break
            current_node = child
        return current_node

    def save_with_json(self, save_file, nb_node):
        if nb_node <= 820:
            root_injson = json.dumps(self, default=lambda o: o.__dict__\
                                     , indent = 2)
            save_file.write(root_injson)
        else:
            save_file.write("Too Much Data")

    def save_with_pickle(self, save_file):
        root_inpickle = jsonpickle.encode(self)
        json.dump(root_inpickle, save_file)

    def get_gesture_with_best_gain_expectation(self, limit = 0):
        sum_rps = self.get_sum_rps()
        if sum_rps <= limit:
            return None
        proba_r = self.nb_rps[str(ROCK)]/sum_rps
        proba_p = self.nb_rps[str(PAPER)]/sum_rps
        proba_s = self.nb_rps[str(SCISSORS)]/sum_rps
        third = 1/3
        if proba_r > third and proba_s < third:
            return PAPER
        elif proba_p > third and proba_r < third:
            return SCISSORS
        else:
            return ROCK

    def get_list_node_from_sequence(self, sequence):
        list_node = [self,]
        current_node = self
        for round in sequence:
            current_node = current_node.get_child_from_round(round)
            if current_node != 0:
                list_node.append(current_node)
            else:
                break
        return list_node

    def get_max_depth(self, current_depth = 0, max_depth = 0):
        current_depth += 1
        for child in self.children.values():
            if max_depth < current_depth:
                max_depth = current_depth
            max_depth = child.get_max_depth(current_depth, max_depth)
        return max_depth

    def get_nb_data_learn_in_depth(self, depth, current_depth = -1):
        current_depth += 1
        nb_round = 0
        for child in self.children.values():
            if current_depth < depth:
                nb_round += child.get_nb_data_learn_in_depth(depth\
                                                            , current_depth)
            else:
                return self.get_sum_rps()
        return nb_round

    def get_list_nb_data_learn_per_depth(self):
        list_nbdata = []
        max_depth = self.get_max_depth()
        for depth in range(max_depth+1):
            nbdata_indepth = self.get_nb_data_learn_in_depth(depth)
            list_nbdata.append(nbdata_indepth)
        return list_nbdata

    def get_nb_child_learn_in_depth(self, depth, current_depth = -1):
        current_depth += 1
        nb_child = 0
        for child in self.children.values():
            if current_depth < depth:
                nb_child += child.get_nb_child_learn_in_depth(depth\
                                                            , current_depth)
            else:
                return len(self.children)
        return nb_child

    def get_list_percentage_child_learn_per_depth(self):
        list_percentage = []
        nbchild_indepth_max = 0
        max_depth = self.get_max_depth()
        for depth in range(max_depth+1):
            nbchild_indepth_max += math.pow(9, depth+1)
            nbchild_indepth = self.get_nb_child_learn_in_depth(depth)
            percentage_indepth = (nbchild_indepth / nbchild_indepth_max) * 100
            list_percentage.append(percentage_indepth)
        return list_percentage

    def plot_percentage_child_per_depth(self):
        list_percentage = self.get_list_percentage_child_learn_per_depth()
        size_max = len(list_percentage)
        plt.figure(figsize = (13.66, 6.10))
        plt.bar(range(0,size_max), list_percentage[:size_max])
        plt.xlabel("Depth")
        plt.ylabel("Percentage child")
        plt.title("Percentage of child learned for each depth")
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
        plt.margins(0, 0.1)
        path_save_file = path_graph + "Child_Depth.png"
        plt.savefig(path_save_file)
        plt.show()


    def plot_nb_data_learn_per_depth(self):
        list_nbdata = self.get_list_nb_data_learn_per_depth()
        size_max = min(len(list_nbdata), 25)
        plt.figure(figsize = (13.66, 6.10))
        plt.bar(range(0,size_max), list_nbdata[:size_max])
        plt.xlabel("Depth")
        plt.ylabel("Number of Round")
        plt.title("Number of Round lerned for each depth")
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
        plt.margins(0, 0.1)
        path_save_file = path_graph + "Round_Depth.png"
        plt.savefig(path_save_file)
        plt.show()

    def save_tree(self, nb_node, data_file_name, pruning = ""):
        if data_file_name == "pst":
            path_save_file = os.path.join(path_tree_1, "pst_file.txt")
        else:
            tree_file_name = "from_" + data_file_name
            if pruning != "":
                tree_file_name = "/" + tree_file_name[:-4] + "_" + pruning + ".txt"
            path_save_file = os.path.join(path_tree_2, tree_file_name)
        save_file = open(path_save_file, "w")
        self.save_with_pickle(save_file)
        save_file.close()
        readable_tree_file_name = "from_readable_" + data_file_name
        if pruning != "":
            readable_tree_file_name = readable_tree_file_name[:-4]\
                                        + "_" + pruning + ".txt"
        path_readable_save_file = os.path.join(path_tree_2, readable_tree_file_name)
        save_file = open(path_readable_save_file, "w")
        self.save_with_json(save_file, nb_node)
        save_file.close()

    @staticmethod
    def load_tree(path_load_file):
        load_file = open(path_load_file, "r")
        root_inpickle = json.load(load_file)
        root_dict = jsonpickle.decode(root_inpickle)
        load_file.close()
        if isinstance(root_dict, Node):
            root = root_dict
        else:
            root = Node()
            root.update_from_dict(root_dict)
            assert(isinstance(root, Node))
        assert(isinstance(root, Node))
        return root

    def predict_gesture_variant(self, game, depth):
        node = self.get_child_from_game(game[-depth:])
        return node.get_gesture_with_best_gain_expectation()

    def predict_gesture_undecided(self, game, depth, beta):
        list_node = self.get_list_node_from_sequence(game[-depth:])
        if len(list_node) == 1:
                return get_gesture_from_list_node(list_node, beta)
        return get_gesture_from_list_node(list_node[1:], beta)

    def predict_gesture_deepest(self, game):
        node = self.get_child_from_game(game)
        if isinstance(node, Node):
            root = node
        else:
            root = Node()
            root.update_from_dict(node)
        return root.get_gesture_with_best_gain_expectation()

    def predict_gesture_online(self, game):
        list_node = self.get_list_node_from_sequence(reversed(game))
        gesture = None
        for node in list_node:
            g = node.get_gesture_with_best_gain_expectation(1)
            if g != None:
                gesture = g
        return gesture

    def predict_gesture_confident(self, game, beta):
        list_node = self.get_list_node_from_sequence(game)
        #if len(list_node) == 1:
        #        return get_gesture_from_list_node(list_node, beta)
        return get_gesture_from_list_node(list_node, beta)

    def get_gesture_and_maxlb(self, beta):
        n = self.get_sum_rps()
        gesture = self.get_gesture_with_best_gain_expectation()
        gain = self.get_gain_max()
        epsilon = get_epsilon_from_nbdata(n, beta)
        gain_lb = gain - epsilon
        return (gesture, gain_lb)

    def get_gain_max(self):
        gesture = self.get_gesture_with_best_gain_expectation()
        l_gesture = beats[gesture]
        w_gesture = beats[l_gesture]
        gain = (self.nb_rps[str(w_gesture)] - self.nb_rps[str(l_gesture)])\
                / self.get_sum_rps()
        return gain

    def pruning_gain_max(self):
        gain_node = self.get_gain_max()
        gain_max = gain_node
        for id_child in list(self.children.keys()):
            gain_child = self.children[id_child].pruning_gain_max()
            if gain_child <= gain_node:
                del self.children[id_child]
            else:
                gain_max = max(gain_child, gain_max)
        return gain_max

    def pruning_depth_max(self, depth_max, current_depth = 0):
        for id_child in list(self.children.keys()):
            if current_depth < depth_max:
                self.children[id_child].pruning_depth_max(depth_max\
                                                    , current_depth+1)
            else:
                del self.children[id_child]

    def print(self, tab=0, prefix=''):
        print(' ' * tab + prefix + '[Rock: {} / Paper: {} / Scissors: {}]'
            .format(self.nb_rps[str(ROCK)],
                    self.nb_rps[str(PAPER)],
                    self.nb_rps[str(SCISSORS)]))
        for id_child in list(self.children.keys()):
            prefix = '-{}-> '.format(id_child)
            self.children[id_child].print(tab=tab+1, prefix=prefix)

def get_epsilon_from_nbdata(nb_data, beta):
    return math.sqrt(beta)/math.sqrt(nb_data)

def get_gesture_from_list_node(list_node, beta):
    dict_gesture_maxlb = { str(ROCK) : 0, str(PAPER) : 0, str(SCISSORS) : 0}
    for node in list_node:
        gesture_gain = node.get_gesture_and_maxlb(beta)
        if gesture_gain[1] > dict_gesture_maxlb[str(gesture_gain[0])]:
            dict_gesture_maxlb[str(gesture_gain[0])] = gesture_gain[1]
    gesture = int(max(dict_gesture_maxlb, key=dict_gesture_maxlb.get))
    return gesture

from ..defs import path_pst_ns


class NodeNS(Node):
    """ Node for non-stationary environments """
    def __init__(self, alpha=0.123):
        Node.__init__(self)
        self.nb_rps = {str(ROCK): 1/3, str(PAPER): 1/3, str(SCISSORS): 1/3}
        self.alpha = alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        for c in self.children.values():
            c.alpha = alpha

    def learn_gesture(self, gesture):
        assert (gesture == ROCK or
                gesture == PAPER or
                gesture == SCISSORS)
        for g in {ROCK, PAPER, SCISSORS}:
            x = int(g == gesture)
            k_g = str(g)
            self.nb_rps[k_g] += self.alpha * (x - self.nb_rps[k_g])

    def predict_gesture_online(self, game):
        list_node = self.get_list_node_from_sequence(reversed(game))
        gesture = None
        for node in list_node:
            g = node.get_gesture_with_best_gain_expectation(0)
            if g != None:
                gesture = g
        return gesture

    def add_child_from_round(self, round):
        name = round.key
        if name not in self.children.keys():
            self.children[name] = NodeNS(alpha=self.alpha)

    def save_tree(self, filename=path_pst_ns):
        save_file = open(filename, "w")
        self.save_with_pickle(save_file)
        save_file.close()
        print('Saved to {}'.format(filename))

    @staticmethod
    def load_tree(filename=path_pst_ns):
        load_file = open(filename, "r")
        root_inpickle = json.load(load_file)
        root_dict = jsonpickle.decode(root_inpickle)
        load_file.close()
        if isinstance(root_dict, NodeNS):
            root = root_dict
        else:
            root = NodeNS()
            root.update_from_dict(root_dict)
            assert(isinstance(root, NodeNS))
        assert(isinstance(root, NodeNS))
        print('NodeNS loaded')
        return root
