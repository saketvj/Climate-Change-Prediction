import os
os.environ['PROJ_LIB'] = r'C:\Users\XXXXX\Anaconda3\pkgs\proj4-5.2.0- ha925a31_1\Library\share'

import glob

import pandas as pd
import numpy as np
import time

import all_in_one_map_making_function as maps
import menkendall_class as mkn
path = r"E:\India"
path_result = r"E:\India_result"

modelNames = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "EC-Earth3", "EC-Earth3-Veg", "INM-CM4-8", "INM-CM5-0", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0", "NorESM2-LM", "NorESM2-MM"]
sceneNames = ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]
dataNames = ["monthly_rx1day.txt","daily_temperature_range.txt","monthly_tnn.txt","monthly_tnx.txt","monthly_txn.txt","monthly_txx.txt"]
data_annual_Names = ["annually_rx1day.txt","annually_temperature_range.txt","annually_tnn.txt","annually_tnx.txt","annually_txn.txt","annually_txx.txt"]


for i in modelNames:
    for j in sceneNames:
        y=0
        for k in dataNames:
            path1=os.path.join(path_result,i,j,'textfile',k)
            path2=os.path.join(path_result,i,j,'textfile')
            data=pd.read_csv(path1,sep=" ",index_col='year')
            data=data.groupby('year').mean()
            data.pop('month')
            data.to_csv(os.path.join(path_result,i,j,'textfile',data_annual_Names[y]),sep=" ")
            y+=1
        
