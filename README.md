# DSP final project
## 簡介
寫程式自動將口琴聲音轉成簡譜
## 作法
先自己吹口琴創造training data，存成wav檔
用MFCC的code將wav檔轉成MFCC存成numpy array
用ML或DL的方式train model
supervised learning : 要先把data label(在蒐集時就label好了)
目前只蒐集do~so和noise的wav檔。
使用focus用法，針對signal，取發生那段(詳述在problem.txt內)
## 安裝套件
- python3.6
- sklearn
- scipy
- numpy
- pyaudio == 0.2.11
- **DNN**:
    - 這裡比較特別與tree model不同的點是用python3.5
    - keras == 2.0.8
    - tensorflow == 1.3.0
    - 其餘上述套件版本3.6 3.5都一樣
## 使用方法
### Train
1. train decision tree
    > python3 tree.py
2. train random forrest
    ```
    python3 forrest.py 5
    5代表tree數量，也可以自己改
    ```
3. dnn
    ```
    python3.5 dnn.py [testfile] =>  一路從train到test(使用doremi.wav)
    testfile放要測試的wav檔
    EX : python3.5 dnn.py Testdata/test.wav
    ```
### Test
python3 test.py [testfile] [model] [tree_num]
```
testfile 測試的wav檔 ==> 可以用 Testdata/doremi.wav
model為要用的模型 ==> 可以為 tree或 forrest，分別代表使用decision tree、random forrest
tree_num為random forrest樹的數量，只有用random forrest時才要用
EX : python3 test.py Testdata/doremi.wav tree
EX2 : python3 test.py Testdata/doremi.wav forrest 5
```
### dnn
python3.5 dnn.py

## code
- **record.py**:蒐集wav檔的主要程式碼
- **complement.py**:record.py是做大量蒐集，中間如果有漏錄，或者吹錯音，用這個程式修改，這個程式只做單一wav檔錄製
- **mfcc.py**：將上述wav檔轉成numpy array(MFCC,40維)
- **tree.py** : regression decision tree
- **svm.py** : svm model
- **train.py** : library for training and turn data to mfcc
- **test.py** :把file.wav拿來test
- **demo.py** : demo時錄音用
- **dnn.py** : Deep Nueral Network
- **autoencoder** : 降維(未經測試)

## model
- **tree.pkl**:用tree.py train出來的model
- **tree00~06.pkl**: random forrest的model
- model都存在Dropbox內
## 資料夾架構
- **Traindata/**
    - do/
        - wav檔，從00~80.wav
    - re/
        - wav檔，從00~80.wav
    - mi/
        - wav檔，從00~80.wav
    - fa/
        - wav檔，從00~80.wav
    - so/
        - wav檔，從00~80.wav
- **MFCC/**
    - do/
        - test.npy(do的所有wav檔轉成的大array)，shape=(81,43,36)
    - re/
        - test.npy(do的所有wav檔轉成的大array)，shape=(81,43,36)
    - mi/
        - test.npy(do的所有wav檔轉成的大array)，shape=(81,43,36)
    - fa/
        - test.npy(do的所有wav檔轉成的大array)，shape(81,43,36)
    - so/
        - test.npy(do的所有wav檔轉成的大array)，shape=(81,43,36)

## Traindata位置
### [Dropbox](https://www.dropbox.com/sh/slb81q2s6z9uafc/AACHbLHjwuQ5zprz5LqLP9yEa?dl=1)

## 效果比較
### Training data數量
do,re,mi,fa,so五個音個50個wav檔，每個wav檔就是一個那個特定的音
### Testing data
<歡樂頌> 前12個音、C大調音階
### 嘗試model
### Decision tree
使用sklearn DecisionTreeRegressor，目前發現效果最好。
### Random forrest
### Deep Neural Network
使用keras實作
1. activation : sigmoid(最後一層用softmax)
2. optimizer : adam
3. loss : categorical_crossentropy
效果蠻差的，
