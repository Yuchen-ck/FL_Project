import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense
from keras import layers
from keras import optimizers

from sklearn import preprocessing
from sklearn.metrics import r2_score

from encrypt_utils import *


enc_folder_name = "./enc_client_model"

if not os.path.exists(enc_folder_name):
    os.makedirs(enc_folder_name)
    


def trainANN(client_name,fixKey):
    
    batch_size_, epochs_ = train_parameters()
    dataPath = "./train_data/dataset.csv" 
    
    x_train_dataset ,y_train ,x_test_dataset ,y_test = preprocession_dataset(dataPath)
    
    ## 設定模型
    model = model_Adam(dim = x_train_dataset.shape[1],target_dim = 1)

    ##開始訓練啦
    model.fit(x_train_dataset, y_train ,batch_size = batch_size_  ,epochs = epochs_, verbose = 1)

    ##測試
    y_true = y_test
    y_pred =  model.predict(x_test_dataset)
    acc = r2_score(y_true,y_pred)
    print(acc)

    ##加密後另存到./Enc_client_model Folder
    ClientModelPath = "./client_model/"  + client_name + ".h5"
    ClientEncModelPath = enc_folder_name  + client_name + ".h5"
    model.save(ClientModelPath)
    file_encrypt(fixKey ,ClientModelPath ,ClientEncModelPath)
    
    #刪除未加密的檔案
    delete_UsedFolder("./client_model/")

    print("model加密後另存成功")

    
def train_parameters():
    batch_size_times = 800
    epochs_times = 400

    return batch_size_times, epochs_times

def preprocession_dataset(path):
    df_train  = pd.read_csv(path)
    x = df_train.iloc[:,1:4]
    y = df_train.iloc[:,-1:]
    print(y.shape)
    x_train,x_test, y_train, y_test = train_test_split(x,y,test_size=0.15)
    x_train_dataset = x_train.values 
    x_test_dataset = x_test.values

    return  x_train_dataset ,y_train ,x_test_dataset ,y_test

def model_Adam(dim,target_dim):
    model = Sequential()
    model.add(layers.Dense(16,kernel_initializer = 'random_normal',activation = 'relu',input_shape = (dim,)))
    model.add(layers.Dense(8, activation = 'relu'))
    model.add(layers.Dense(4, activation = 'relu'))
    model.add(layers.Dense(target_dim, activation = 'linear'))
    
    adam = optimizers.Adam(learning_rate=0.1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer = adam, loss = 'mae')
    return model
