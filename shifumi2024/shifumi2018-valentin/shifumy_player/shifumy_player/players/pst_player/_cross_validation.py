# coding: utf8

import sys
import math

from .module.Node import Node
from .module.History import History
from .defs import beats
from .agent.Agent import DoubleFacePstAgent, ConfidentPstAgent


from .defs import path_misc, path_misc_crossvalid_lastnode, list_data_file

###############################################################################

def validation(agent, hist1_tolearn, hist2_tolearn, hist3_totest):
    agent.root.learn_from_history(hist1_tolearn)
    agent.root.learn_from_history(hist2_tolearn)
    if isinstance(agent, DoubleFacePstAgent):
        agent.root.pruning_depth_max(3)
    if isinstance(agent, ConfidentPstAgent):
        agent.root.pruning_gain_max()
    wld = get_wld_agent_in_history(agent, hist3_totest)
    agent.root = Node()
    return wld

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

###############################################################################
