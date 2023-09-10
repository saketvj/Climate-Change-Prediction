import os
os.environ['PROJ_LIB'] = r'C:\Users\XXXXX\Anaconda3\pkgs\proj4-5.2.0- ha925a31_1\Library\share'

import glob

import pandas as pd
import numpy as np
import time

import pymannkendall as pym
import map_class 
import menkendall_class as mk
import all_in_one_map_making_function as maps


path = r"E:\India"
path_result = r"E:\India_result"

lonlat = pd.read_csv(r"E:\India_result\ACCESS-CM2\historical\textfile\lonlat transpose.txt" , sep = " " )
lonlat.columns.values[0] = 'ids'
lonlat.set_index("ids", inplace = True)
modelNames = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "EC-Earth3"]
sceneNames = ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]
dataFolder = ["textfile"]
dataNames = ["prcptot.txt"]





for i in sceneNames :
    for j in dataFolder:
        for k in dataNames:
            x=0
            path1 = os.path.join(path_result, "ENSEMBLE DATA" , i, j)
            path2 = os.path.join(path_result, "ENSEMBLE DATA" , i, "maps")
            print(path1,path2)
            
            for l in modelNames:
                if x==0:
                    data_avg=pd.read_csv(os.path.join(path_result, l , i , j, k) , sep = " ",index_col="year")
                    x=1
                else:
                    data_tm= pd.read_csv(os.path.join(path_result, l , i , j, k) , sep = " ",index_col="year")
                    data_avg=data_avg.add(data_tm)
                    data_avg=data_avg.div(2)
            data_avg.to_csv(os.path.join(path1,k) , sep = " " )
            hopeless=maps.maps(data_avg,lonlat,path2,"xyz")
            hopeless.map()
            hopeless.diff_map()
