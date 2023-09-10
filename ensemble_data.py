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
dataNames = ["prcptot.txt","sdii.txt","cwd_annually.txt","cdd_annually.txt","annual_r20mm.txt","annual_r10mm.txt","annually_rx5day.txt","annual_summer_days.txt","annual_icing_days.txt","annual_tropical_nights.txt","annual_frost_days.txt","data_tmin_annual.txt","data_tmax_annual.txt","data_prcp_annual.txt"]
titleNames = ["Mean Annual Precipitation","sdii","cwd_annually","cdd_annually","annual_r20mm","annual_r10mm","annually_rx5day","annual_summer_days","annual_icing_days","annual_tropical_nights","annual_frost_days","data_tmin_annual","data_tmax_annual","data_prcp_annual"]
titleNamesMK = ["Slope & Trend of Mean Annual Precipitation","Slope & Trend of sdii","Slope & Trend of cwd_annually","Slope & Trend of cdd_annually","Slope & Trend of annual_r20mm","Slope & Trend of annual_r10mm","Slope & Trend of annually_rx5day","Slope & Trend of annual_summer_days","Slope & Trend of annual_icing_days","Slope & Trend of annual_tropical_nights","Slope & Trend of annual_frost_days","Slope & Trend of data_tmin_annual","Slope & Trend of data_tmax_annual","Slope & Trend of data_prcp_annual"]

for i in sceneNames :
    y = 0
    for k in dataNames:
        x=0
        path1 = os.path.join(path_result, "ENSEMBLE DATA" , i, "textfile")
        path2 = os.path.join(path_result, "ENSEMBLE DATA" , i, "maps")
        start=time.time()
        for l in modelNames:

            lonlat = pd.read_csv(r"E:\\India_result\\ACCESS-CM2\\historical\textfile\\lonlat transpose.txt" , sep = " " )
            lonlat.columns.values[0] = 'ids'
            lonlat.set_index("ids", inplace = True)

            if x==0:
                data_avg=pd.read_csv(os.path.join(path_result, l , i , "textfile", k) , sep = " ",index_col="year")
                data_avg = data_avg.round(2)

                mp=maps.maps(data_avg,lonlat,os.path.join(path_result, l , i ,"maps"),titleNames[y])
                mp.map()
                mp.diff_map()
                
                mkd = mkn.mannkendall(data_avg,lonlat,os.path.join(path_result, l , i ,"maps"),titleNamesMK[y])
                mkd.trend_analysis_map()

            else:
                data_tm= pd.read_csv(os.path.join(path_result, l , i , "textfile", k) , sep = " ",index_col="year")
                data_tm = data_tm.round(2)

                mp=maps.maps(data_tm,lonlat,os.path.join(path_result, l , i ,"maps"),titleNames[y])
                mp.map()
                mp.diff_map()
                
                mkd = mkn.mannkendall(data_avg,lonlat,os.path.join(path_result, l , i ,"maps"),titleNamesMK[y])
                mkd.trend_analysis_map()

                data_avg=data_avg.add(data_tm)
                
        data_avg=data_avg.div(13)
        data_avg = data_avg.round(2)
        data_avg.to_csv(os.path.join(path1,k) , sep = " " )
        mp=maps.maps(data_avg,lonlat,path2,titleNames[y])
        mp.map()
        mp.diff_map()
        end=time.time()
        print(f"Total runtime of program is {end - start}")
        y += 1