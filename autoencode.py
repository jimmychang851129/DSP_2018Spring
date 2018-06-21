import numpy as np
from keras.models import Model
from keras.layers import Dense,Input
from sklearn import cluster
from keras import callbacks
from keras.callbacks import Callback
from keras.models import load_model
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.neighbors import DistanceMetric
import sys

alldata = []
music = ["do/","re/","mi/","fa/","so/"]
inputfile = "MFCC/"
for i in music:
	d = np.load(inputfile+i+"test.npy")
	alldata.append(d)

alldata = np.array(alldata)
alldata = alldata.reshape(alldata.shape[0]*alldata.shape[1],alldata.shape[2]*alldata.shape[3])
input_word = Input(shape=(alldata.shape[1],))
encoded = Dense(512,activation="relu")(input_word)
encoded = Dense(256,activation="relu")(encoded)
encoded = Dense(128,activation="relu")(encoded)
encoder_output = Dense(32)(encoded)

decoded = Dense(128,activation="relu")(encoder_output)
decoded = Dense(256,activation="relu")(decoded)
decoded = Dense(512,activation="relu")(decoded)
decoded = Dense(alldata.shape[1],activation="relu")(decoded) # activation

autoencoder = Model(input=input_word,output=decoded)
encoder = Model(input=input_word,output=encoder_output)

autoencoder.compile(optimizer="adam",loss="mse")
autoencoder.fit(alldata,alldata,epochs=500,shuffle=True)
autoencoder.save("./best_encoder")