import numpy as np
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #關閉提示訊息
from keras.layers.normalization import layer_normalization
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer 
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
import time
from tqdm import tqdm
from cryptography.fernet import Fernet
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import backend as K

from fl_utils import *
from aggregate_utils import *

def FedAVG(client_num,fixKey): 
    print(client_num)
    #超參數
    comms_round = 1
    epochs_ = 1

    path = './train_data/dataset.csv'
    X, Y = load(path)

    x_train,x_test, y_train, y_test = train_test_split(X, Y,test_size=0.15, random_state=42)


    #create clients anda client's data #
    clients = create_clients(x_train, y_train, num_clients=client_num, initial='client')

    #process and batch the training data for each client
    clients_batched = dict()
    for (client_name, data) in clients.items():
        clients_batched[client_name] = batch_data(data)

    test_batched = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(len(y_test))
    #print(test_batched)

    #--------------------------------------開始聯邦-----------------------------------
    smlp_global = SimpleMLP()
    global_model = smlp_global.build(train_dim = x_train.shape[1] ,target_dim = 1)
    # print(global_model.summary())


    #FedAVG
    #commence global training loop
    for comm_round in range(comms_round):
                
        # get the global model's weights - will serve as the initial weights for all local models
        global_weights = global_model.get_weights()
        
        #initial list to collect local model weights after scalling
        scaled_local_weight_list = list()

        #randomize client data - using keys
        client_names= list(clients_batched.keys())
        random.shuffle(client_names)

        #random.shuffle(client_names)
        print(len(client_names))

        #loop through each client and create new local model
        for client in tqdm(client_names , desc = 'Progress Bar'):
            #time.sleep(0.5)
            smlp_local = SimpleMLP()
            local_model = smlp_local.build(train_dim = x_train.shape[1] ,target_dim = 1)
        
            # print(local_model.summary())
            ##set local model weight to the weight of the global model
            local_model.set_weights(global_weights)
            print("@@@")
            #print(client)
            
            print(clients_batched[client])  


            #fit local model with client's data
            local_model.fit(clients_batched[client], epochs = epochs_, verbose=1)

            #scale the model weights and add to list
            scaling_factor = weight_scalling_factor(clients_batched, client)
            print("scaling_factor: " + str(scaling_factor))
            scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
            scaled_local_weight_list.append(scaled_weights)
            
            #clear session to free memory after each communication round
            K.clear_session()
            
        #to get the average over all the local model, we simply take the sum of the scaled weights
        average_weights = sum_scaled_weights(scaled_local_weight_list)
        
        #update global model 
        global_model.set_weights(average_weights)
        
        
        #在這裡就要加密!(加密後存取，靜態時才能保持加密狀態)
        aggregateModelPath = "./server_model/server_agg_" + str(comms_round)+"_"+str(epochs_)+".h5"
        aggEncryptModelPath = "./enc_server_model/Enc_server_agg_" + str(comms_round)+"_"+str(epochs_)+".h5"
        
        global_model.save(aggregateModelPath)
        file_encrypt(fixKey ,aggregateModelPath ,aggEncryptModelPath)

        #刪除未加密的檔案
        delete_UsedFolder("./server_model/") 
        #os.makedirs("./server_model/")

        #test global model and print out metrics after each communications round
        r2_list = list()
        for(X_test, Y_test) in test_batched:
            r2_score_ = test_model(X_test, Y_test, global_model, comm_round)
            r2_list.append(r2_score_)

        print(r2_list)
    
