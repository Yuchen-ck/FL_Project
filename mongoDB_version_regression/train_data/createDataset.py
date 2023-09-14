import random
import math
import numpy as np
import pandas as pd

row_number = 10000
energy_list = []
speed_list = []
rate_list = []
line_width_square_list = []

def decimal():
    A=0.03
    B=0.1678
    a = random.uniform(A,B)
    C=4 #随机数的精度round(数值，精度)
    return round(a,C) 

import random
import math
import numpy as np
import pandas as pd

row_number = 10000
power_list = []
energy_list = []
speed_list = []
rate_list = []
line_width_square_list = []

def decimal():
    A=0.03
    B=0.1678
    a = random.uniform(A,B)
    C=4 #随机数的精度round(数值，精度)
    return round(a,C) 

if __name__ == '__main__':
    for i in range(1,row_number):
        ee = decimal()
        #0.
        power_list.append(ee*50)
        
        #1. 
        #print(decimal())
        energy_list.append(ee)
        
        #2.
        speed_list.append(100)
        
        #3.
        rate_list.append(50)
        
        #4.
        ax = 7048.30557 * math.log(ee)   
        line_width_square = ax + 25992.84377
        line_width_square = round(line_width_square,3)
        #print(line_width_square)
        line_width_square_list.append(line_width_square)
    
    power_list_numpy  = np.array(power_list)
    power_list_numpy  = power_list_numpy.reshape(row_number - 1,1)
    
    energy_list_numpy  = np.array(energy_list)
    energy_list_numpy  = energy_list_numpy.reshape(row_number - 1,1)
    
    speed_list_numpy  = np.array(speed_list)
    speed_list_numpy  = speed_list_numpy.reshape(row_number - 1,1)
    
    rate_list_numpy  = np.array(rate_list)
    rate_list_numpy  = rate_list_numpy.reshape(row_number - 1,1)
    
    line_width_square_list_numpy  = np.array(line_width_square_list)
    line_width_square_list_numpy  = line_width_square_list_numpy.reshape(row_number - 1,1)
    
    df0 = pd.DataFrame(power_list_numpy, columns = ['power'])
    #df1 = pd.DataFrame(energy_list_numpy, columns = ['energy'])
    df2= pd.DataFrame(speed_list_numpy, columns = ['speed'])
    df3 = pd.DataFrame(rate_list_numpy, columns = ['rate'])
    df4= pd.DataFrame(line_width_square_list_numpy, columns = ['line_width_square'])
    
    df = pd.concat( [df0, df2 , df3 , df4], axis=1 )
    df= df.reset_index(drop = True)
    df.to_csv("dataset.csv")