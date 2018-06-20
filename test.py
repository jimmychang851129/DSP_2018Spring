import train
import scipy.io.wavfile
import numpy as np
import sys
testfile = sys.argv[1]
method = sys.argv[2]
tree_num = 0
if method == "tree":
	clf = train.loadTree()
elif method == "forrest":
	tree_num = int(sys.argv[3])
	clf = train.loadForrest(tree_num)
sample_rate, signal = scipy.io.wavfile.read(testfile)

NUM_PER_SEC = 44032*2
len = signal.shape[0]
# diff = 198 - 161
prev = 0

mfccdata = []
for i in range(0,len,NUM_PER_SEC//2):
	t = signal[i:i+NUM_PER_SEC//2]
	t = train.refine(t,t.shape[0])
	print("write to ","test%d"%(i)+".wav",sample_rate)
	# scipy.io.wavfile.write("test%d"%(i)+".wav",sample_rate,t)
	# t = np.repeat(t,2,axis=0).reshape(t.shape[0]*2,2)
	d = train.ToMFCC(t)
	mfccdata.append(d)

# mfccdata = np.array(mfccdata)	
data = np.array(mfccdata)
print("data.shape = ",data.shape)
data = data.reshape(data.shape[0],data.shape[1]*data.shape[2])

music = ["do","re","mi","fa","so"]

######################
# decide which model #
######################
if method == "tree":
	ans = train.TreeTest(clf,data)
elif method == "forrest":
	ans = train.testForrest(clf,data)
for i in ans:
	print(music[int(i)],end=' ')
print("")



# scipy.io.wavfile.write("test.wav",sample_rate,t)
################
# double array #
################
# np.repeat(a,2,axis=0).reshape(4,2)