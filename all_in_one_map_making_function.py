import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os

class maps :
  def __init__(self,data,lonlat,path,title) :
      
      self.path=path
      self.data= data
      self.title=title

      #lon_arr = np.arange(61.125 , 97.875, 0.25)
      #lat_arr = np.arange(6.125 , 37 , 0.25)

      self.lon_arr = np.arange(lonlat['longitude'].min() , lonlat['longitude'].max()+0.25, 0.25)
      self.lat_arr = np.arange(lonlat['latitude'].min() , lonlat['latitude'].max()+0.25 , 0.25)
      self.year_count=list(map( int , data.index.values ))
      self.point_ids=list(map( int , data.columns.values ))
      self.lonlat = lonlat
      self.lon_edges = np.arange((self.lonlat)['longitude'].min()-0.125 , (self.lonlat)['longitude'].max()+0.375, 0.25)
      self.lat_edges = np.arange((self.lonlat)['latitude'].min()-0.125 , (self.lonlat)['latitude'].max()+0.375 , 0.25)

  def map(self) :
      
      df_avg=self.data.iloc[:].mean()
      data_avg=df_avg.to_numpy(dtype = np.float64())

      avg_data2d = np.empty((len(self.lon_arr),len(self.lat_arr)))
      avg_data2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lon_arr:
        n = 0
        for j in self.lat_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["longitude"][x+1],(self.lonlat)["latitude"][x+1]) :
            avg_data2d[n][m] = data_avg[x]
            x = x + 1
          n = n + 1   
        m = m + 1

      '''
      mp = Basemap(projection = 'merc',
                  llcrnrlat = self.lat_arr.min() - 2,
                  urcrnrlat = self.lat_arr.max() + 2,
                  llcrnrlon = self.lon_arr.min() - 2,
                  urcrnrlon = self.lon_arr.max() + 2,
                  resolution = 'i')

      lons, lats = np.meshgrid(self.lon_arr, self.lat_arr)

      x,y = mp(lons, lats)

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, avg_prep2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("mean avg prcp value(in mm)")

      plt.title('Mean Annual Precipitation')
      plt.savefig( os.path.join(self.path,"Mean Annual Precipitation.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_edges,self.lat_edges,avg_data2d, vmin = np.min(data_avg), vmax = np.max(data_avg), cmap = "jet")
      #plt.clim(np.min(data_avg), np.max(data_avg))
      cbar = plt.colorbar()
      cbar.set_label(self.title+' Values', rotation=270 , labelpad=+15)

      plt.title(self.title + " " + str(self.year_count[0]) + "-" + str(self.year_count[-1]))
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('Longitude')
      axes.set_ylabel('Latitude')

      plt.savefig(os.path.join(self.path,self.title + " " + str(self.year_count[0]) + "-" + str(self.year_count[-1]) + ".jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")


  def year_separating(self,starting_year,separating_year,ending_year) :
      
      df_avg=self.data.iloc[ending_year - separating_year :].mean() - self.data.iloc[0:separating_year - starting_year + 1].mean()
      data_avg=df_avg.to_numpy(dtype = np.float64())

      avg_data2d = np.empty((len(self.lon_arr),len(self.lat_arr)))
      avg_data2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lon_arr:
        n = 0
        for j in self.lat_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["longitude"][x+1],(self.lonlat)["latitude"][x+1]) :
            avg_data2d[n][m] = data_avg[x]
            x = x + 1
          n = n + 1   
        m = m + 1

      '''
      mp = Basemap(projection = 'merc',
                  llcrnrlat = self.lat_arr.min() - 2,
                  urcrnrlat = self.lat_arr.max() + 2,
                  llcrnrlon = self.lon_arr.min() - 2,
                  urcrnrlon = self.lon_arr.max() + 2,
                  resolution = 'i')

      lons, lats = np.meshgrid(self.lon_arr, self.lat_arr)

      x,y = mp(lons, lats)

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, avg_prep2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("mean avg prcp value(in mm)")

      plt.title('Mean Annual Precipitation')
      plt.savefig( os.path.join(self.path,"Mean Annual Precipitation.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_edges,self.lat_edges,avg_data2d, vmin = -np.max(data_avg), vmax = np.max(data_avg), cmap = "jet")
      #plt.clim(np.min(data_avg), np.max(data_avg))
      cbar = plt.colorbar()
      cbar.set_label(self.title+' Values', rotation=270 , labelpad=+15)

      plt.title('Diff in '+self.title + " " + str(starting_year) + "-"  + str(separating_year)+" & "+str(separating_year+1) + "-"  + str(ending_year))
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('Longitude')
      axes.set_ylabel('Latitude')

      plt.savefig(os.path.join(self.path,'Diff in '+self.title + " " + str(starting_year) + "-"  + str(separating_year)+" & "+str(separating_year+1) + "-"  + str(ending_year)+".jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")


  def diff_map(self) :
      
      starting_year = self.year_count[0]
      separating_year = self.year_count[len(self.year_count)//2 - 1]
      ending_year = self.year_count[-1]

      df_avg=self.data.iloc[ending_year - separating_year :].mean() - self.data.iloc[0:separating_year - starting_year + 1].mean()
      data_avg=df_avg.to_numpy(dtype = np.float64())

      avg_data2d = np.empty((len(self.lon_arr),len(self.lat_arr)))
      avg_data2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lon_arr:
        n = 0
        for j in self.lat_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["longitude"][x+1],(self.lonlat)["latitude"][x+1]) :
            avg_data2d[n][m] = data_avg[x]
            x = x + 1
          n = n + 1   
        m = m + 1

      '''
      mp = Basemap(projection = 'merc',
                  llcrnrlat = self.lat_arr.min() - 2,
                  urcrnrlat = self.lat_arr.max() + 2,
                  llcrnrlon = self.lon_arr.min() - 2,
                  urcrnrlon = self.lon_arr.max() + 2,
                  resolution = 'i')

      lons, lats = np.meshgrid(self.lon_arr, self.lat_arr)

      x,y = mp(lons, lats)

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, avg_prep2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("mean avg prcp value(in mm)")

      plt.title('Mean Annual Precipitation')
      plt.savefig( os.path.join(self.path,"Mean Annual Precipitation.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_edges,self.lat_edges,avg_data2d, vmin = -np.max(data_avg), vmax = np.max(data_avg), cmap = "jet")
      #plt.clim(np.min(data_avg), np.max(data_avg))
      cbar = plt.colorbar()
      cbar.set_label(self.title+' Values', rotation=270 , labelpad=+15)

      plt.title('Diff in '+self.title + " " + str(starting_year) + "-"  + str(separating_year)+" & "+str(separating_year+1) + "-"  + str(ending_year))
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('Longitude')
      axes.set_ylabel('Latitude')

      plt.savefig(os.path.join(self.path,'Diff in '+self.title + " " + str(starting_year) + "-"  + str(separating_year)+" & "+str(separating_year+1) + "-"  + str(ending_year)+".jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")   