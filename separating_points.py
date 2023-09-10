import os
os.environ['PROJ_LIB'] = r'C:\Users\XXXXX\Anaconda3\pkgs\proj4-5.2.0- ha925a31_1\Library\share'
import pandas as pd
import numpy as np
import time

    
path = r"E:\India"
path_result = r"E:\India_result"
path_point = r"E:\India_points"
modelNames = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "EC-Earth3", "EC-Earth3-Veg", "INM-CM4-8", "INM-CM5-0", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0", "NorESM2-LM", "NorESM2-MM"]
sceneNames = ["ssp126"]
dataNames = ["PrecipData", "TmaxData", "TminData"]


for i in modelNames :
    for j in sceneNames :
        print(i,j)
        starting_time = time.time()
        for k in dataNames : 
            path1 = os.path.join(path_result, i , j )
            
            if k == "PrecipData" :
                data_prcp = pd.read_csv(os.path.join(path, i , j , k) , sep = " ", header = None)
            if k == "TmaxData" :
                data_tmax = pd.read_csv(os.path.join(path, i , j , k) , sep = " ", header = None)
            if k == "TminData" :
                data_tmin = pd.read_csv(os.path.join(path, i , j , k) , sep = " ", header = None)
        
        start = time.time()
        header = ["year","month","day"]
        header.extend(np.arange(1,data_tmax.shape[1] - 2,1))
        
        data_prcp.columns = header
        data_tmax.columns = header
        data_tmin.columns = header
        
        point_ids=list(range(1,len(header) - 2,1))

        #data_prcp.drop(labels = ["month","day"] , axis=1, inplace = True)
        
        data_prcp["year"][0] = "longitude"
        data_prcp["year"][1] = "latitude"
        
        data_tmax["year"][0] = "longitude"
        data_tmax["year"][1] = "latitude"
        
        data_tmin["year"][0] = "longitude"
        data_tmin["year"][1] = "latitude"
        
        lonlat = (data_prcp.iloc[[0,1]]).set_index("year")
        lonlat.drop(labels=['month','day'],axis=1,inplace=True)
        lonlat = lonlat.T
        
        data_prcp.set_index('year',inplace=True)
        data_tmax.set_index('year',inplace=True)
        data_tmin.set_index('year',inplace=True)
        
        data_prcp.drop(labels=['latitude','longitude'],inplace=True)
        data_tmax.drop(labels=['latitude','longitude'],inplace=True)
        data_tmin.drop(labels=['latitude','longitude'],inplace=True)
        
        for l in point_ids :

            data_new=pd.DataFrame()
            
            data_new['year']=data_tmin.index
            data_new.set_index('year',inplace=True)
            
            data_new['month']=data_tmin['month']
            data_new['day']=data_tmin['day']
            
            data_new['prcp']=data_prcp[l]
            data_new['tmin']=data_tmin[l]
            data_new['tmax']=data_tmax[l]
            
            data_new.to_csv(os.path.join(path_point , i , j , "data"+"_"+str(lonlat['latitude'][l])+"_"+str(lonlat['longitude'][l])+".txt"), sep = " ")
        
        data_prcp = []
        data_tmax = []
        data_tmin = []
        data_new = []
        
        end = time.time()
        print(f"Total runtime of program is {end - start}")

