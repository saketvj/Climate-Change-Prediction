import os
os.environ['PROJ_LIB'] = r'C:\Users\XXXXX\Anaconda3\pkgs\proj4-5.2.0- ha925a31_1\Library\share'

import glob

import pandas as pd
import numpy as np
import time

import precipitation_indices as pi
import temperature_indices as ti
    
path = r"E:\India"
path_result = r"E:\India_result"

modelNames = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "EC-Earth3", "EC-Earth3-Veg", "INM-CM4-8", "INM-CM5-0", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0", "NorESM2-LM", "NorESM2-MM"]
sceneNames = ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]
dataNames = ["PrecipData", "TmaxData", "TminData"]

'''
for i in range(len(glob.glob(path + '\\*'))) :
    for j in range(len(glob.glob(glob.glob(path + '\\*')[i] + "\\*"))) :
        starting_time = time.time()
        for k in range(len(glob.glob(glob.glob(glob.glob(path + '\\*')[i] + "\\*")[j] + "\\*"))) :
            path1=glob.glob(glob.glob(path_result + '\\*')[i] + "\\*")[j] 

            if k == 0 :
                data_prcp = pd.read_csv(glob.glob(glob.glob(glob.glob(path + '\\*')[i] + "\\*")[j] + "\\*")[k] , sep = " ", header = None)
            if k == 1 :
                data_tmax = pd.read_csv(glob.glob(glob.glob(glob.glob(path + '\\*')[i] + "\\*")[j] + "\\*")[k] , sep = " ", header = None)
            if k == 2 :
                data_tmin = pd.read_csv(glob.glob(glob.glob(glob.glob(path + '\\*')[i] + "\\*")[j] + "\\*")[k] , sep = " ", header = None)
'''

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

        header = ["year","month","day"]
        header.extend(np.arange(1,data_tmax.shape[1] - 2,1))

        data_prcp.columns = header
        data_tmax.columns = header
        data_tmin.columns = header

        #data_prcp.drop(labels = ["month","day"] , axis=1, inplace = True)

        starting_year=int(data_tmin['year'].min())
        ending_year=int(data_tmin['year'].max())

        year_count=list(range(starting_year,ending_year+1,1))
        point_ids=list(range(1,len(header) - 2,1))
        month_count=list(range(1,13,1))

        data_prcp["year"][0] = "longitude"
        data_prcp["year"][1] = "latitude"

        data_tmax["year"][0] = "longitude"
        data_tmax["year"][1] = "latitude"

        data_tmin["year"][0] = "longitude"
        data_tmin["year"][1] = "latitude"

        lonlat = (data_prcp.iloc[[0,1]]).set_index("year")
        lonlat.drop(labels=['month','day'],axis=1,inplace=True)
        lonlat.to_csv(os.path.join(path1,"textfile","lonlat.txt") , sep = " ")
        lonlat = lonlat.T
        lonlat.to_csv(os.path.join(path1,"textfile","lonlat transpose.txt") , sep = " ")

        """
        latlon = (lonlat).sort_values(by=['latitude','longitude'],axis=0,inplace=False)
        #latlon = latlon.T
        latlon.reset_index(inplace=True,drop=True)
        latlon.to_csv(os.path.join(path1,"latlon transpose.txt") , sep = " ")

        lon_arr = np.arange((lonlat)['longitude'].min() , (lonlat)['longitude'].max()+0.25, 0.25)
        lat_arr = np.arange((lonlat)['latitude'].min() , (lonlat)['latitude'].max()+0.25 , 0.25)

        #lon_arr = np.arange(61.125 , 97.875, 0.25)
        #lat_arr = np.arange(6.125 , 37 , 0.25)
        """

        data_prcp = data_prcp[2:]
        data_prcp.reset_index(inplace = True , drop = True)

        data_tmax = data_tmax[2:]
        data_tmax.reset_index(inplace = True , drop = True)

        data_tmin = data_tmin[2:]
        data_tmin.reset_index(inplace = True , drop = True)

        
        data_prcp_annual = data_prcp.groupby("year")[np.arange(1,len(header) - 2,1)].sum()
        data_prcp_annual.to_csv(os.path.join(path1,"textfile", "data_prcp_annual.txt") , sep = " ")
        data_prcp_annual = []

        """
        data_prcp_map = pd.concat([lonlat.T,data_prcp_annual])
        data_prcp_map.sort_values(by=["latitude","longitude"] , axis=1, inplace=True)
        data_prcp_map.to_csv(os.path.join(path1 ,"textfile","data_prcp_map.txt") , sep = " ")
        """
        
        data_tmax_annual = data_tmax.groupby("year")[np.arange(1,len(header) - 2,1)].mean()
        data_tmax_annual.to_csv(os.path.join(path1,"textfile", "data_tmax_annual.txt") , sep = " ")
        data_tmax_annual = []

        data_tmin_annual = data_tmin.groupby("year")[np.arange(1,len(header) - 2,1)].mean()
        data_tmin_annual.to_csv(os.path.join(path1,"textfile", "data_tmin_annual.txt") , sep = " ")
        data_tmin_annual = []
        
        begin = time.time() 

        x = ti.TemperatureIndices(data_tmax, data_tmin, year_count, month_count, point_ids)

        x.annual_frost_days().to_csv(os.path.join(path1,"textfile","annual_frost_days.txt") , sep = " " )
        x.annual_tropical_nights().to_csv(os.path.join(path1,"textfile","annual_tropical_nights.txt") , sep = " " )
        x.annual_icing_days().to_csv(os.path.join(path1,"textfile","annual_icing_days.txt") , sep = " " )
        x.annual_summer_days().to_csv(os.path.join(path1,"textfile","annual_summer_days.txt") , sep = " " )
        x.monthly_txx().to_csv(os.path.join(path1,"textfile","monthly_txx.txt") , sep = " " )
        x.monthly_txn().to_csv(os.path.join(path1,"textfile","monthly_txn.txt") , sep = " " )
        x.monthly_tnx().to_csv(os.path.join(path1,"textfile","monthly_tnx.txt") , sep = " " )
        x.monthly_tnn().to_csv(os.path.join(path1,"textfile","monthly_tnn.txt") , sep = " " )
        x.daily_temperature_range().to_csv(os.path.join(path1,"textfile","daily_temperature_range.txt") , sep = " " )
        
        x = []
        
        end = time.time()
        print(f"Total runtime of temperature indices is {end - begin}")


        begin = time.time()

        y = pi.PrecipitationIndices(data_prcp, year_count, month_count, point_ids)
        y.monthly_rx1day().to_csv(os.path.join(path1,"textfile","monthly_rx1day.txt") , sep = " " )
        #y.monthly_rx5day().to_csv(os.path.join(path1,"textfile","monthly_rx5day.txt") , sep = " " )
        y.annually_rx5day().to_csv(os.path.join(path1,"textfile","annually_rx5day.txt") , sep = " " )
        y.annual_rnmm(10).to_csv(os.path.join(path1,"textfile","annual_r10mm.txt") , sep = " " )
        y.annual_rnmm(20).to_csv(os.path.join(path1,"textfile","annual_r20mm.txt") , sep = " " )
        #y.cdd_monthly().to_csv(os.path.join(path1,"textfile","cdd.txt") , sep = " " )
        y.cdd_annually().to_csv(os.path.join(path1,"textfile","cdd_annually.txt") , sep = " " )
        #y.cwd_monthly().to_csv(os.path.join(path1,"textfile","cwd.txt") , sep = " " )
        y.cwd_annually().to_csv(os.path.join(path1,"textfile","cwd_annually.txt") , sep = " " )
        y.sdii().to_csv(os.path.join(path1,"textfile","sdii.txt") , sep = " " )
        y.prcptot().to_csv(os.path.join(path1,"textfile","prcptot.txt") , sep = " " )
        
        y = []
        
        end = time.time()
        print(f"Total runtime of precipitation indices is {end - begin}")
        
        data_prcp = []
        data_tmax = []
        data_tmin = []

        ending_time = time.time()
        print(f"Total runtime of program is {ending_time - starting_time}")
