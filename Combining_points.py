import os
os.environ['PROJ_LIB'] = r'C:\Users\XXXXX\Anaconda3\pkgs\proj4-5.2.0- ha925a31_1\Library\share'
import glob
import pandas as pd
import numpy as np

os.chdir(r"E:\ObservedData")

file_type = ["*.125","*.375","*.625","*.875"]

header1 = ["year","month","day","prcp","Tmax","Tmin"]
header2 = ["prcp","Tmax","Tmin"]
header3 = ["latitude","longitude","a_prcp","Tmax","Tmin"]

"""You know that Lat Lon of all points. You also have values of average Prcp, Tmax and Tmin. Prepare three maps showing these average values."""

filenames = []
lonlat=pd.read_csv(r"E:\India_result\ACCESS-CM2\historical\textfile\lonlat transpose.txt",sep=" ")
lonlat.columns=['point_ids','longitude','latitude']
lonlat=lonlat.set_index('point_ids')
latlon=lonlat.sort_values(by=['latitude','longitude'])
latlon.reset_index(drop =True, inplace=True)

arr = []

for x in range(4641) :
    a = "_".join(["data",str(latlon.latitude[x]),str(latlon.longitude[x])])
    arr.append(a)

list1 = np.linspace(1,4641,num = 4641).astype(int)


zip_iterator = zip(arr, list1)

a_dictionary = dict(zip_iterator)

x = 0
i=0
df_prcp=pd.DataFrame(columns = list1)
df_tmax=pd.DataFrame(columns = list1)
df_tmin=pd.DataFrame(columns = list1)
path="E:\ObservedData_result"
y=0
file_data=[df_prcp,df_tmin,df_tmax]
save_data=['prcp','Tmin','Tmax']


for type in file_type:
    for file_name in glob.glob(type):
        df = pd.read_csv(file_name, sep=" ",names=header1)
        if y==0:
            df_prcp['year']=df.year
            df_prcp['month']=df.month
            df_prcp['day']=df.day
            df_tmax['year']=df.year
            df_tmax['month']=df.month
            df_tmax['day']=df.day
            df_tmin['year']=df.year
            df_tmin['month']=df.month
            df_tmin['day']=df.day
            y=1
        temp=file_name
        dic = a_dictionary.get(temp)
        
        if dic != None :
            
            df_prcp[int(dic)] = df.prcp
            df_tmax[int(dic)] = df.Tmax
            df_tmin[int(dic)] = df.Tmin
   

df_prcp.to_csv(os.path.join(path+"prcp"+".txt"),sep=" ", index=False)
df_tmax.to_csv(os.path.join(path+"tmax"+".txt"),sep=" ", index=False)
df_tmin.to_csv(os.path.join(path+"tmin"+".txt"),sep=" ", index=False)
    