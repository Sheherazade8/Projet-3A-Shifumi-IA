
### Import From Other
import tensorflow as tf
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import _pickle as cPickle
import marshal
from numpy import *
# import pydot
# import graphviz


### Import From Keras

from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Dropout, Activation, Flatten, TimeDistributed, Conv2D, MaxPooling2D, Input
from tensorflow.python.keras.optimizers import SGD
# from tensorflow.python.keras.layers.recurrent import LSTM
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.utils import to_categorical
# from tensorflow.python.keras.utils.vis_utils import plot_model
from tensorflow.python import keras

### Import From Sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


import datetime



### path

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shifumy_player.shifumy_player.base import  RpsAgent,RESOURCES_PATH

class Tdnn():

    def __init__(self):

        path = RESOURCES_PATH
        path1 = os.path.join(path,"data")
        path2 = os.path.join(path1,"datasets")

        pathdata = os.path.join(path2,"data.txt")

        self.datashifumi = pd.read_csv(pathdata, delimiter=":")
        self.model = None

    def plot_round(self):
        self.datashifumi["Round"].hist(bins=50, figsize=(10, 15))
        plt.xlim(1, 18)
        plt.ylabel("Nombre d'occurence")
        plt.xlabel("Nombre de Round")
        plt.show()

    def plot_model(self):
        plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=False)

    def transform_rps_vecteur(self,coup):
        encoded = to_categorical(coup, num_classes=4)
        #    print("Before=",encoded)
        #    print(shape(encoded))
        oneHotVector = delete(encoded, 0)

        return oneHotVector

    def transform_data_prepation(self,data):

        list_data_game_playerOne = [[]]
        list_data_game_playerTwo = [[]]
        list_data_all = [[[], []]]

        dict_data_transform = {}

        Game = 1

        for index, row in data.iterrows():
            game = row["Game"]
            rd = row["Round"]
            player_op = row["Player_oppement"]
            player_ag = row["Player_agent"]

            if (Game == game):

                list_data_game_playerOne[-1].append(transform_rps_vecteur(player_op))
                list_data_game_playerTwo[-1].append(transform_rps_vecteur(player_ag))

                list_data_all[-1][0].append(transform_rps_vecteur(player_op))
                list_data_all[-1][1].append(transform_rps_vecteur(player_ag))

            else:
                Game = game
                list_data_game_playerOne.append([])
                list_data_game_playerTwo.append([])

                list_data_game_playerOne[-1].append(transform_rps_vecteur(player_op))
                list_data_game_playerTwo[-1].append(transform_rps_vecteur(player_ag))

                list_data_all.append([[], []])
                list_data_all[-1][0].append(transform_rps_vecteur(player_op))
                list_data_all[-1][1].append(transform_rps_vecteur(player_ag))

        return list_data_game_playerOne, list_data_game_playerTwo, list_data_all


    def transform_rps_vecteur(self,coup):
        encoded = to_categorical(coup, num_classes=4)
        #    print("Before=",encoded)
        #    print(shape(encoded))
        oneHotVector = delete(encoded, 0)

        return oneHotVector

    def get_data_step(self,data, step):
        """
        Param : data , ste
        Fonction return x(data),y(target)
        """
        list_x_playerOne = []
        list_x_playerTwo = []

        list_y = []
        dict_x = {}
        dict_y = {}

        list_player_one = data["1"]
        list_player_two = data["2"]

        for index, row in enumerate(list_player_one):
            game_playerOne = list_player_one[index]
            game_playerTwo = list_player_two[index]

            if ((len(game_playerOne) > step) & (len(game_playerTwo) > step)):
                list_x_playerOne.append(game_playerOne[0:step])
                list_x_playerTwo.append(game_playerTwo[0:step])

                list_y.append(game_playerOne[step])

        dict_x["1"] = list_x_playerOne
        dict_x["2"] = list_x_playerTwo

        dict_y["3"] = list_y

        return list_x_playerOne, list_y

    def get_data_step_array(self,data, step):
        """
        Param : data , ste
        Fonction return x(data),y(target)
        """

        list_x = []
        list_y = []

        #   list_player_two = data["2"]

        data_RPS = data

        for index, row in enumerate(data_RPS):

            party_all = row
            party_op = row[0]
            party_ag = row[1]

            if ((len(party_ag) > step)):
                list_x.append([party_op[0:step], party_ag[0:step]])
                list_y.append(party_op[step])

        return list_x, list_y



    def createSequentialModel(self,X,y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train, X_test, y_train, y_test = array(X_train), array(X_test), array(y_train), array(y_test)
        self.X_train = X_train
        self.y_train = y_train


        from keras.models import Model

        print("X=", X[0])
        print("X_shape=", shape(X_train))
        print("X_type=", type(X_train))

        print("y=", y_train[0])
        print("y_shape=", shape(y_train))
        print("y_type=", type(y_train))

        print("Build model ..")

        model = Sequential()

        model.add(Dense(25, activation='sigmoid', input_shape=(2, 2, 3)))

        model.add(Dense(15, activation='relu'))

        model.add(Flatten())

        model.add(Dense(3, activation='softmax'))

        print("Plot model draw..")

        # plot_model(model)

        print("Compile model ..")
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
        print("Fit model ..")

        model.fit(X_train, y_train, batch_size=32, epochs=1)
        score = model.evaluate(X_test, y_test, batch_size=32)

        self.model = model

        print("Score=", score)


    def predict(self):
        X_pred = to_categorical([random.randint(3, size=(1, 1))], num_classes=3)
        #
        # print("*** X_pred",X_pred[0:1])
        # print("*** X_Trin",self.X_train[0:1])
        # print("*** X_pred shape=", shape(X_pred))
        # print("*** X_pred shape=", shape(self.X_train))
        # print("Prediction ...")
        y_pred = self.model.predict_classes(X_pred)
        print(" Fin Prediction ")
        # print("X=", self.X_train[0:1], "y=", self.y_train[0:1])

        return y_pred
        # print(self.model.summary())

    def saved_model_Tdnn(self):
        self.model.save("tdnn.h5")

    def load_model_saved(self):
        self.model = load_model("tdnn2.h5")





















#
# print("TensorFlow=",tf.__version__)
#
# print("Keras=",keras.__version__)
#
#
# f = load_model("tdnn4.h5")
#
#
# tdnn = Tdnn()
#
# tdnn.plot_round()
#
#
#
# X_humans,X_robot= tdnn.transform_data_prepation()
#
# X_ar_humans = array(X_humans)
# ts = datetime.datetime.now()
# print("create Array data ...")
# X, y =tdnn.get_data_step_array(X_ar_humans,1)
# tf = datetime.datetime.now()
# print("finish data ...")
# print("Time to ",tf-ts)
#
#
# print("Create Model ...")
# ts = datetime.datetime.now()
#
# tdnn.createSequentialModel(X,y)
# tf = datetime.datetime.now()
# print("Time to create Model",tf-ts)
#

print("load ..")
# tdnn.load_model_saved()

# print("predict_agent_gesture Model ...")
#
# ts = datetime.datetime.now()
#
# y_pred = tdnn.predict_agent_gesture()
# tf = datetime.datetime.now()
#
# print("Time to predict_agent_gesture Model",tf-ts)
# print("Y_pred:",y_pred)
#
# #
# # print("saved ..")
# # tdnn.saved_model_Tdnn()



# datashifumi = pd.read_csv("data.txt",delimiter=":" )

# X_humans,X_robot,data_all= transform_data_prepation(datashifumi)
# X_ar_humans = array(X_humans)
# X,y=get_data_step_array(data_all,1)
# X, y =get_data_step_array(data_all,2)
