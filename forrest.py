import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
from scipy.sparse import coo_matrix
from sklearn.utils import shuffle
from sklearn.externals import joblib
import sys
##########
# config #
##########
DATA_NUM = 81
TREE_NUM = int(sys.argv[1])

alldata = []
music = ["do/","re/","mi/","fa/","so/"]
inputfile = "MFCC/"
for i in music:
	d = np.load(inputfile+i+"test.npy")
	alldata.append(d)

alldata = np.array(alldata)
alldata = alldata.reshape(alldata.shape[0]*alldata.shape[1],alldata.shape[2]*alldata.shape[3])
label = np.ndarray(shape=(DATA_NUM*5))
for i in range(1,6):
	label[DATA_NUM*(i-1):DATA_NUM*i].fill(i-1)

###########
# shuffle #
###########
ALL = coo_matrix(alldata)
for i in range(TREE_NUM):
	alldata, ALL, label = shuffle(alldata, ALL, label, random_state=0)

	#########
	# train #
	#########
	clf = tree.DecisionTreeRegressor()
	clf.fit(alldata,label)

	##############
	# save model #
	##############
	joblib.dump(clf,"tree"+"%02d"%(i)+".pkl")
