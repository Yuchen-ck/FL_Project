import pandas as pd
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from os import listdir
from os.path import isfile, isdir, join

import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import backend as K
from sklearn.metrics import r2_score

def load(path):
    #匯入資料集
    # path = '../train_data/dataset.csv'
    df_train = pd.read_csv(path)
    print(df_train.shape)

    x = df_train.iloc[:,1:4]
    y = df_train.iloc[:,-1:]

    return x.values ,y.values #回傳.values

def create_clients(data_list, label_list,num_clients, initial='clients'):
    # create a list of client names
    client_names = ['{}_{}'.format(initial, i+1) for i in range(num_clients)]

    #randomize the data
    data = list(zip(data_list, label_list))
    #random.shuffle(data)
    # print(data)

    #shard data and place at each client
    size = len(data)//num_clients
    shards = [data[i:i + size -1] for i in range(1, size*num_clients, size)]

    #number of clients must equal number of shards
    assert(len(shards) == len(client_names))

    #print({client_names[i] : shards[i] for i in range(len(client_names))})
    return {client_names[i] : shards[i] for i in range(len(client_names))}


def batch_data(data_shard, bs = 100):
    '''Takes in a clients data shard and create a tfds object off it
    args:
        shard: a data, label constituting a client's data shard
        bs:batch size
    return:
        tfds object'''
    #seperate shard into data and labels lists
    data, label = zip(*data_shard)
    dataset = tf.data.Dataset.from_tensor_slices((list(data), list(label)))
    return dataset.shuffle(len(label)).batch(bs)

#模型架構_main.py
class SimpleMLP:
    @staticmethod
    def build(train_dim, target_dim):
        model = Sequential()
        model.add(Dense(16,kernel_initializer = 'random_normal',activation = 'relu',input_shape = (train_dim,)))
        model.add(Dense(8, activation = 'relu'))
        model.add(Dense(4, activation = 'relu'))
        model.add(Dense(target_dim, activation = 'linear'))
    
        #adam = optimizers.Adam(lr=0.0001) #lr學習率
        #model.compile(optimizer = adam, loss = 'mae')
    
        sgd = optimizers.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        adam = optimizers.Adam(learning_rate=0.1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
        model.compile(optimizer = adam, loss = 'mae')
        return model


def folder_cleint_name(mypath):
    # 取得所有檔案與子目錄名稱
    files = listdir(mypath)
    client_names_ = list()
    # 以迴圈處理
    for f in files:
        # 產生檔案的絕對路徑
        fullpath = join(mypath, f)
        # 判斷 fullpath 是檔案還是目錄
        if isfile(fullpath):
            print("檔案：", f)
            client_names_.append(f[:-3])
        elif isdir(fullpath):
            print("目錄：", f)
    
    return client_names_

def weight_scalling_factor(clients_trn_data, client_name):
    client_names = list(clients_trn_data.keys())
    #get the bs
    bs = list(clients_trn_data[client_name])[0][0].shape[0]
    #first calculate the total training data points across clinets
    global_count = sum([tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy() for client_name in client_names])*bs
    # get the total number of data points held by a client
    local_count = tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy()*bs
    return local_count/global_count


def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final



def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)
        
    return avg_grad

def test_model(X_test, Y_test,  model, comm_round):
    y_true = Y_test
    y_pred =  model.predict(X_test)
    r2_score_ = r2_score(y_true,y_pred)
    print(r2_score_)
    return r2_score_