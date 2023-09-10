import os
os.environ['PROJ_LIB'] = r'C:\Users\XXXXX\Anaconda3\pkgs\proj4-5.2.0- ha925a31_1\Library\share'
import pandas as pd
import numpy as np
import time

    
path = r"E:\India_result"
path_result = r"E:\temp"
path_point = r"E:\India_result"
modelNames = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "EC-Earth3", "EC-Earth3-Veg", "INM-CM4-8", "INM-CM5-0", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0", "NorESM2-LM", "NorESM2-MM"]
sceneNames = ["historical"]
dataNames = ["PrecipData", "TmaxData", "TminData"]
lonlat = pd.read_csv(r"E:\India_result\ACCESS-CM2\historical\textfile\lonlat transpose.txt")


for i in modelNames :
    for j in sceneNames :
        print(i,j)
        starting_time = time.time()
         
        path1 = os.path.join(path_result, i , j )
        data_prcp = pd.read_csv(os.path.join(path, i , j , "textfile" ,"annually_rx1day.txt") , sep = " ", header = None)

        start = time.time()
        header = ["year","month","day"]
        header.extend(np.arange(1,data_prcp.shape[1] - 2,1))
        
        data_prcp.columns = header
        
        
        point_ids=list(range(1,len(header) - 2,1))

        #data_prcp.drop(labels = ["month","day"] , axis=1, inplace = True)
        
        data_prcp["year"][0] = "longitude"
        data_prcp["year"][1] = "latitude"

        
        for l in point_ids :

            data_new=pd.DataFrame()
            
            data_new['year']=data_prcp.index
            data_new.set_index('year',inplace=True)
            
            data_new['month']=data_prcp['month']
            data_new['day']=data_prcp['day']
            
            data_new['prcp']=data_prcp[l]
            
            
            data_new.to_csv(os.path.join(path_result , i , j , "data"+"_"+str(lonlat['latitude'][l])+"_"+str(lonlat['longitude'][l])+".txt"), sep = " ")
        
        data_prcp = []
        data_new = []
        
        end = time.time()
        print(f"Total runtime of program is {end - start}")

