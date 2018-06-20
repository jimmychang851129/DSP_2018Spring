from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Activation
from keras.optimizers import SGD, Adam, Adadelta,rmsprop
from keras.models import Sequential
import tensorflow as tf
from scipy.sparse import coo_matrix
from sklearn.utils import shuffle
import numpy as np
from keras.utils import np_utils
import scipy.io.wavfile
import numpy as np
import train
import sys
##########
# config #
##########
DATA_NUM = 81
testfile = sys.argv[1]
#############
# load file #
#############
alldata = []
music = ["do/","re/","mi/","fa/","so/"]
inputfile = "MFCC/"
for i in music:
	d = np.load(inputfile+i+"test.npy")
	alldata.append(d)

alldata = np.array(alldata)
alldata = alldata.reshape(alldata.shape[0]*alldata.shape[1],alldata.shape[2]*alldata.shape[3])
label = np.ndarray(shape=(DATA_NUM*5,1))
for i in range(1,6):
	label[DATA_NUM*(i-1):DATA_NUM*i].fill(i-1)

label = np_utils.to_categorical(label)
###########
# shuffle #
###########
ALL = coo_matrix(alldata)
alldata, ALL, label = shuffle(alldata, ALL, label, random_state=0)
model = Sequential()
model.add(Dense(512,input_dim=alldata.shape[1],activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(256,activation='sigmoid'))
model.add(Dense(64,activation='sigmoid'))
model.add(Dense(5,activation='softmax'))
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x=alldata, y=label,epochs=300,validation_split=0.15)

sample_rate, signal = scipy.io.wavfile.read(testfile)

NUM_PER_SEC = 44032*2
len = signal.shape[0]
diff = 198 - 161
prev = 0

mfccdata = []
for i in range(0,len,NUM_PER_SEC//2):
	print("prev = ",prev,"i = ",i)
	t = signal[i:i+NUM_PER_SEC//2]
	t = train.refine(t,t.shape[0])
	d = train.ToMFCC(t)
	mfccdata.append(d)

mfccdata = np.array(mfccdata)	
mfccdata = mfccdata.reshape(mfccdata.shape[0],mfccdata.shape[1]*mfccdata.shape[2])
ans = model.predict(mfccdata)
ans = np.argmax(ans,axis=1)

music = ["do","re","mi","fa","so"]
for x in ans:
	print(music[x],end=" ")

print("")

