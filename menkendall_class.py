import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pymannkendall as mk

class mannkendall:
  def __init__(self,data,lonlat,path,title) :
      
      self.path=path
      self.data= data
      self.title=title
      self.lon_arr = np.arange(lonlat['longitude'].min() , lonlat['longitude'].max()+0.25, 0.25)
      self.lat_arr = np.arange(lonlat['latitude'].min() , lonlat['latitude'].max()+0.25 , 0.25)
      self.year_count=list(map( int , data.index.values ))
      self.point_ids=list(map( int , data.columns.values ))
      self.lonlat = lonlat
      self.lon_edges = np.arange((lonlat)['longitude'].min()-0.125 , (lonlat)['longitude'].max()+0.375, 0.25)
      self.lat_edges = np.arange((lonlat)['latitude'].min()-0.125 , (lonlat)['latitude'].max()+0.375 , 0.25)


  def mannkendall_analysis(self):
      x = 0
      header = ["trend" , "h" , "p", "z" , "Tau", "s" , "var_s" , "slope" , "intercept"]
      results = np.array([])
      for i in range(1,len(self.point_ids)+1,1) :
        result = mk.original_test(np.array(self.data["{}".format(i)]))
        if x == 0 :
          results = result
          x=1
        else:
          results = np.append(results , result)
      file_mk =  pd.DataFrame(np.reshape(results,(len(self.point_ids),9)) , columns = header , index= np.arange(1,len(self.point_ids)+1,1))
      return file_mk

  def trend_analysis_map(self):
      file_mk=self.mannkendall_analysis()
      tem = (file_mk["p"].copy()).astype(float)
      p_index = tem[tem <= 0.05].index

      lons_i = np.array([])
      lats_i = np.array([])

      lons_d = np.array([])
      lats_d = np.array([])

      for i in p_index :
        if file_mk["trend"][i] == 'increasing' :
          lon_i = ((self.lonlat))["longitude"][(i)]
          lat_i = ((self.lonlat))["latitude"][(i)]
          
          lons_i = np.append(lons_i , lon_i)
          lats_i = np.append(lats_i , lat_i)

        elif file_mk["trend"][i] == 'decreasing' :
          lon_d = (self.lonlat)["longitude"][(i)]
          lat_d = (self.lonlat)["latitude"][(i)]
          
          lons_d = np.append(lons_d , lon_d)
          lats_d = np.append(lats_d , lat_d)

      d_set = file_mk["slope"].to_numpy(dtype = np.float64())

      slope2d = np.empty((len(self.lat_arr),len(self.lon_arr)))
      slope2d[:] = np.NaN
      
      x = 0
      m = 0
      for i in self.lon_arr:
        n = 0
        for j in self.lat_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["longitude"][(x+1)],(self.lonlat)["latitude"][(x+1)]) :
            slope2d[n][m] = d_set[(x)] 
            x = x + 1
          n = n + 1
        m = m + 1
  
      plt.pcolormesh(self.lon_edges,self.lat_edges,slope2d,vmin = -np.max(d_set), vmax = np.max(d_set), cmap = "jet")
      #plt.clim(-1*np.max(d_set), np.max(d_set))
      cbar = plt.colorbar()
      cbar.set_label('slope values', rotation=270,labelpad=+15)

      plt.title(self.title)
      
      #plt.savefig(os.path.join(self.path,"slope of Annual Precipitation.jpg"), bbox_inches='tight', dpi=400)
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('Longitude')
      axes.set_ylabel('Latitude')
      plt.plot(lons_i , lats_i , linewidth = 0 , color='black', marker="^", markersize=.1 , label = "Increasing Trend")
      plt.plot(lons_d , lats_d , linewidth = 0 , color='white', marker="v", markersize=.1 , label = 'Decreasing Trend')
      plt.legend(loc='upper right')

      plt.savefig(os.path.join(self.path,self.title + ".jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")