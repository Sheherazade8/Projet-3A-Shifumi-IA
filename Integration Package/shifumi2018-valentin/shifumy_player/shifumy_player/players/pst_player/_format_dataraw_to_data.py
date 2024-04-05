# coding: utf8
import sys
from .defs import SEPARATOR, correspondance_gesture_dataraw, path_dataraw\
                  , path_data, path_alldata

from .defs import get_index_next_separator\
                  , get_index_second_separator\
                  , get_id_game_from_line

from ...base import ROCK, PAPER, SCISSORS, Round, RpsAgent


def format_dataraw(nb_data = 0):
    dataraw = open(path_dataraw, "r")
    data    = open(path_data   , "w")
    lines = dataraw.readlines()
    for line in lines:
        line = line.replace("\t",SEPARATOR)
        if (SEPARATOR + "0") not in line:
            data.write(line)
    dataraw.close()
    data.close()

    data = open(path_data, "r")
    lines = data.readlines()
    data.close()

    if nb_data <= 0:
        print("How many data do you want in data.txt ? (int)")
        nb_data = input()
        nb_data = int(nb_data)
    while nb_data <= 0:
        print("Enter a positive integer please")
        nb_data = input()
        nb_data = int(nb_data)

    if nb_data >= len(lines):
        path_file = path_alldata
    else:
        path_file = path_data

    data = open(path_file, "w")
    id_round = 0
    id_first_sep = get_index_next_separator(lines[0])
    first_part = lines[0][:id_first_sep]
    id_game = int(first_part)
    current_game = 0
    for line in lines[:min(len(lines), nb_data)]:
        id_first_sep = get_index_next_separator(line)
        id_second_sep = get_index_next_separator(line, id_first_sep)
        first_part = line[:id_first_sep+1]
        second_part = line[id_second_sep:]
        temp = second_part[0]\
              + str(correspondance_gesture_dataraw[second_part[1]]) \
              + second_part[2]\
              + str(correspondance_gesture_dataraw[second_part[3]])
        id_round += 1
        if id_game != int(first_part[:id_first_sep]):
            id_game = int(first_part[:id_first_sep])
            current_game += 1
            id_round = 1
        current_line = str(current_game) + SEPARATOR + str(id_round) + temp + '\n'
        data.write(current_line)
    data.close()
    print("Data saved in %s:" % path_file)
    return path_file

if __name__ is "__main__":
    format_dataraw()
