# -*- coding: utf-8 -*-
"""
@autor : ibrahim Souleiman
Description classe : this classe implemented base.py is agent to use neural network to predict_agent_gesture the next move
"""



import _pickle as cPickle
import marshal
from numpy import *
import h5py

from shifumy_player.base import RpsAgent, Round, ROCK, PAPER, SCISSORS, RESOURCES_PATH

from tensorflow.python.keras.models import Sequential,load_model
from tensorflow.python import  keras
from tensorflow.python.keras.utils import to_categorical


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

X_pred= keras.utils.to_categorical(random.randint(3, size=(1, 1)), num_classes=3)

opMov = {ROCK:PAPER,PAPER:SCISSORS,SCISSORS:ROCK}
opMov123 = {1:PAPER,2:SCISSORS,3:ROCK}

class TdnnPstAgent(RpsAgent):

    def __init__(self):
        super().__init__()
        self.model = None
        self.model1 = None


    def get_two_last_round(self):
        return self.game[-1],self.game[-2]



    def get_array_transformed(self,x_last,x_before):
        list_data_all = [[[], []]]
        list_data_all[-1][0].append(keras.utils.to_categorical(x_before.opponent, num_classes=3))
        list_data_all[-1][0].append(keras.utils.to_categorical(x_last.opponent, num_classes=3))

        list_data_all[-1][1].append(keras.utils.to_categorical(x_before.agent, num_classes=3))
        list_data_all[-1][1].append(keras.utils.to_categorical(x_last.agent, num_classes=3))

        array_data = array(list_data_all)
        return  array_data




    def predict_agent_gesture(self):

        gain = self.get_agent_gain_h2(self.game)

        if(gain == -2):
            game_list = self.transform_hist_data_onehot012(self.game)
            y_pred = random.randint(3, size=(1, 1))[0][0]
            # y_pred = self.model1.predict_classes([game_list])[0]


        else:
            game_list = self.transform_hist_data_onehot123(self.game)
            y_pred = self.model.predict_classes(game_list)[0]


        return opMov[y_pred]

    def transform_hist(self, op, ag):
        x_op = keras.utils.to_categorical(op, num_classes=3)
        x_ag = keras.utils.to_categorical(ag, num_classes=3)

        transform_data = [[[], []]]
        transform_data[-1][0].append(x_op)
        transform_data[-1][0].append(x_ag)

        array_data = array(transform_data)

        return array_data

    def transform_hist_data(self,game):

        length = len(game)
        if(length == 0):
            predict = [[to_categorical(0, num_classes=3), to_categorical(0, num_classes=3)]]
            predict = array(predict)
            return predict
        if(length == 1):
            op_last_move = game[-1].opponent
            predict = [[to_categorical(0, num_classes=3), to_categorical(op_last_move, num_classes=3)]]
            predict = array(predict)
            return predict
        if(length > 1):
            op_last_move = game[-1].opponent
            op_before_last_move = game[-2].opponent
            predict = [[to_categorical(op_before_last_move, num_classes=3), to_categorical(op_last_move, num_classes=3)]]
            predict = array(predict)
            return predict

    def transform_hist_data_onehot012(self,game):

        length = len(game)
        if (length == 0):
            predict = [[self.transform_mov_vector_123(0, 0), self.transform_mov_vector_123(0, 0)]]

            predict = array(predict)
            return predict
        if (length == 1):
            op_last_move = (game[-1].opponent)
            ag_last_move = (game[-1].agent)
            predict = [[self.transform_mov_vector_123(0, 0), self.transform_mov_vector_123(op_last_move, ag_last_move)]]

            predict = array(predict)
            return predict
        if (length > 1):
            op_last_move = (game[-1].opponent)
            op_before_last_move = (game[-2].opponent)
            ag_last_move = (game[-1].agent)
            ag_before_last_move = (game[-2].agent)
            predict = [[self.transform_mov_vector_123(op_before_last_move, ag_before_last_move),
                        self.transform_mov_vector_123(op_last_move, ag_last_move)]]

            predict = array(predict)
            return predict

    def transform_hist_data_onehot123(self,game):

        length = len(game)
        if(length == 0):
            predict = [[self.transform_mov_vector_123(1,1), self.transform_mov_vector_123(1,1)]]

            predict = array(predict)
            return predict
        if(length == 1):
            op_last_move = (game[-1].opponent)+1
            ag_last_move = (game[-1].agent)+1
            predict = [[self.transform_mov_vector_123(1,1), self.transform_mov_vector_123(op_last_move,ag_last_move)]]

            predict = array(predict)
            return predict
        if(length > 1):
            op_last_move = (game[-1].opponent)+1
            op_before_last_move = (game[-2].opponent)+1
            ag_last_move = (game[-1].agent)+1
            ag_before_last_move = (game[-2].agent)+1
            predict = [[self.transform_mov_vector_123(op_before_last_move,ag_before_last_move), self.transform_mov_vector_123(op_last_move,ag_last_move)]]

            predict = array(predict)
            return predict

    def get_agent_gain_h2(self,game):
        gain = 0
        taille = len(game)
        if(taille >=4):
            for round in game[-5:-1]:
               gain += round.get_agent_gain()
        return gain





    def transform_mov_vector_123(self,op, ag):

        """
        R = 1
        P = 2
        S = 3
        RR : [1 0 0 0 0 0 0 0 0]
        RP : [0 1 0 0 0 0 0 0 0]
        RS : [0 0 1 0 0 0 0 0 0]
        PP : [0 0 0 1 0 0 0 0 0]
        PS : [0 0 0 0 1 0 0 0 0]
        PR : [0 0 0 0 0 1 0 0 0]
        SS : [0 0 0 0 0 0 1 0 0]
        SP : [0 0 0 0 0 0 0 1 0]
        SR : [0 0 0 0 0 0 0 0 1]
        """

        if (op == 1 and ag == 1):
            return to_categorical(0, num_classes=9)
        elif (op == 1 and ag == 2):
            return to_categorical(1, num_classes=9)
        elif (op == 1 and ag == 3):
            return to_categorical(2, num_classes=9)
        elif (op == 2 and ag == 1):
            return to_categorical(3, num_classes=9)
        elif (op == 2 and ag == 2):
            return to_categorical(4, num_classes=9)
        elif (op == 2 and ag == 3):
            return to_categorical(5, num_classes=9)
        elif (op == 3 and ag == 1):
            return to_categorical(6, num_classes=9)
        elif (op == 3 and ag == 2):
            return to_categorical(7, num_classes=9)
        elif (op == 3 and ag == 3):
            return to_categorical(8, num_classes=9)
        print("FIN")

    def transform_mov_vector_012(self,op, ag):

        """
        R = 0
        P = 1
        S = 2
        RR : [1 0 0 0 0 0 0 0 0]
        RP : [0 1 0 0 0 0 0 0 0]
        RS : [0 0 1 0 0 0 0 0 0]
        PP : [0 0 0 1 0 0 0 0 0]
        PS : [0 0 0 0 1 0 0 0 0]
        PR : [0 0 0 0 0 1 0 0 0]
        SS : [0 0 0 0 0 0 1 0 0]
        SP : [0 0 0 0 0 0 0 1 0]
        SR : [0 0 0 0 0 0 0 0 1]
        """

        if (op == 0 and ag == 0):
            return to_categorical(0, num_classes=9)
        elif (op == 0 and ag == 1):
            return to_categorical(1, num_classes=9)
        elif (op == 0 and ag == 2):
            return to_categorical(2, num_classes=9)
        elif (op == 1 and ag == 0):
            return to_categorical(3, num_classes=9)
        elif (op == 1 and ag == 1):
            return to_categorical(4, num_classes=9)
        elif (op == 1 and ag == 2):
            return to_categorical(5, num_classes=9)
        elif (op == 2 and ag == 0):
            return to_categorical(6, num_classes=9)
        elif (op == 2 and ag == 1):
            return to_categorical(7, num_classes=9)
        elif (op == 2 and ag == 2):
            return to_categorical(8, num_classes=9)
        print("FIN")

    def load(filepath=None):
        path = os.path.join(RESOURCES_PATH,"data")
        path1 = os.path.join(path,"models")
        path2 = os.path.join(path1,"NN9.h5")
        nn = TdnnPstAgent()
        keras.backend.clear_session()
        nn.model = load_model(path2)
        
        return nn





