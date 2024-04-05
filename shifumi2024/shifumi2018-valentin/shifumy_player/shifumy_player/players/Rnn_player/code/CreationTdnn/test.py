from tensorflow.python.keras.utils import plot_model
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Dropout, Activation, Flatten, TimeDistributed, Conv2D, MaxPooling2D, Input
from tensorflow.python.keras.utils import to_categorical

from numpy import *

from pydot import *

from graphviz import *

model = Sequential()

model.add(Dense(3, activation='sigmoid', input_shape=(1, 3)))

model.add(Flatten())

model.add(Dense(3, activation='sigmoid'))

plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=False)
# X_pred = to_categorical([random.randint(3, size=(1, 1))], num_classes=3)
# print(X_pred)




import sys
import tensorflow as tf

print(sys.version)

print(tf.__version__)