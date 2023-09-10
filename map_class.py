import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import os

class map :
  def __init__(self,data_annual_prcp,data_annual_tmax,data_annual_tmin,lonlat,year_count,month_count,point_ids,path) :
   
      self.path=path
      self.data_annual_prcp = data_annual_prcp
      self.data_annual_tmax = data_annual_tmax
      self.data_annual_tmin = data_annual_tmin

      lon_arr = np.arange(lonlat['longitude'].min() , lonlat['longitude'].max()+0.25, 0.25)
      lat_arr = np.arange(lonlat['latitude'].min() , lonlat['latitude'].max()+0.25 , 0.25)

      #lon_arr = np.arange(61.125 , 97.875, 0.25)
      #lat_arr = np.arange(6.125 , 37 , 0.25)

      self.lat_arr = lat_arr
      self.lon_arr = lon_arr
      self.year_count=year_count
      self.month_count=month_count
      self.point_ids=point_ids
      self.lonlat = lonlat
      #latlon = lonlat.sort_values(by=['latitude','longitude'],axis=0,inplace=False)
      #latlon.reset_index(inplace=True,drop=True)
      #self.latlon=latlon


  def ann_prcp(self) :
      df_avg=self.data_annual_prcp.iloc[:].mean()
      prep_avg=df_avg.to_numpy(dtype = np.float64())

      avg_prep2d = np.empty((len(self.lon_arr),len(self.lat_arr)))
      avg_prep2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lon_arr:
        n = 0
        for j in self.lat_arr:
          if x == len(self.point_ids):
            break
          if (j,i) == ((self.lonlat)["latitude"][x+1],(self.lonlat)["longitude"][x+1]) :
            avg_prep2d[n][m] = prep_avg[x]
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

      plt.pcolormesh(self.lon_arr,self.lat_arr,avg_prep2d,vmin = np.min(prep_avg), vmax = np.max(prep_avg))
      #plt.clim(np.min(prep_avg), np.max(prep_avg))
      cbar = plt.colorbar()
      cbar.set_label('Mean Annual Precipitation Values', rotation=270)

      plt.title('Mean Annual Precipitation' + " " + str(self.year_count[0]) + "-" + str(self.year_count[-1]))
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('longitude')
      axes.set_ylabel('latitude')

      plt.savefig(os.path.join(self.path,'Mean Annual Precipitation' + " " + str(self.year_count[0]) + "-" + str(self.year_count[-1]) + ".jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")

  def change_analysis_prcp(self) :
      df=self.data_annual_prcp.iloc[len(self.year_count)//2:].mean() - self.data_annual_prcp.iloc[0:len(self.year_count)//2].mean()
      prep_diff=df.to_numpy(dtype = np.float64())

      diff_prep2d = np.empty((len(self.lat_arr),len(self.lon_arr)))
      diff_prep2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lat_arr:
        n = 0
        for j in self.lon_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["latitude"][x],(self.lonlat)["longitude"][x]) :
            diff_prep2d[m][n] = prep_diff[x]

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

      c_scheme = mp.pcolor(x, y, diff_prep2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("change in prcp value(in mm)")

      plt.title('Annual Precipitation Difference')
      plt.savefig( os.path.join(self.path,"Annual Precipitation Difference.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_arr,self.lat_arr,diff_prep2d)
      plt.clim(-1*np.max(prep_diff), np.max(prep_diff))
      cbar = plt.colorbar()
      cbar.set_label('Annual Precipitation Difference Values', rotation=270)

      plt.title('Annual Precipitation Difference')
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('longitude')
      axes.set_ylabel('latitude')

      plt.savefig(os.path.join(self.path,"Annual Precipitation Difference.jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")

  def ann_tmax(self) :
      df_avg=self.data_annual_tmax.iloc[:].mean()
      tmax_avg=df_avg.to_numpy(dtype = np.float64())

      avg_tmax2d = np.empty((len(self.lat_arr),len(self.lon_arr)))
      avg_tmax2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lat_arr:
        n = 0
        for j in self.lon_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["latitude"][x],(self.lonlat)["longitude"][x]) :
            avg_tmax2d[m][n] = tmax_avg[x]
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
      #print(len(lon_arr),len(lat_arr))
      #print(lons,lats)

      x,y = mp(lons, lats)
      #print(len(x),len(y))

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, avg_tmax2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("mean avg tmax value(in mm)")

      plt.title('Mean Annual Tmax')
      plt.savefig( os.path.join(self.path,"Mean Annual Tmax.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_arr,self.lat_arr,avg_tmax2d)
      plt.clim(np.min(tmax_avg), np.max(tmax_avg))
      cbar = plt.colorbar()
      cbar.set_label('Mean Annual Tmax Values', rotation=270)

      plt.title('Mean Annual Tmax')
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('longitude')
      axes.set_ylabel('latitude')

      plt.savefig(os.path.join(self.path,"Mean Annual Tmax.jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")

  def change_analysis_tmax(self) :
      df=self.data_annual_tmax.iloc[len(self.year_count)//2:].mean()-self.data_annual_tmax[0:len(self.year_count)//2].mean()
      tmax_diff=df.to_numpy(dtype = np.float64())

      diff_tmax2d = np.empty((len(self.lat_arr),len(self.lon_arr)))
      diff_tmax2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lat_arr:
        n = 0
        for j in self.lon_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["latitude"][x],(self.lonlat)["longitude"][x]) :
            diff_tmax2d[m][n] = tmax_diff[x]
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
      #print(len(lon_arr),len(lat_arr))
      #print(lons,lats)

      x,y = mp(lons, lats)
      #print(len(x),len(y))

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, diff_tmax2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("change in tmax value(in C)")

      plt.title('Annual tmax Difference')
      plt.savefig( os.path.join(self.path,"Annual tmax Difference.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''
      plt.pcolormesh(self.lon_arr,self.lat_arr,diff_tmax2d)
      plt.clim(-1*np.max(tmax_diff), np.max(tmax_diff))
      cbar = plt.colorbar()
      cbar.set_label('Annual Tmax Difference Values', rotation=270)

      plt.title('Annual Tmax Difference')
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('longitude')
      axes.set_ylabel('latitude')

      plt.savefig(os.path.join(self.path,"Annual Tmax Difference.jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")

  def ann_tmin(self) :
      df_avg=self.data_annual_tmin.iloc[:].mean()
      tmin_avg=df_avg.to_numpy(dtype = np.float64())

      avg_tmin2d = np.empty((len(self.lat_arr),len(self.lon_arr)))
      avg_tmin2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lat_arr:
        n = 0
        for j in self.lon_arr:
          if x == len(self.point_ids):
            break
          if (i,j) == ((self.lonlat)["latitude"][x],(self.lonlat)["longitude"][x]) :
            avg_tmin2d[m][n] = tmin_avg[x]
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
      #print(len(lon_arr),len(lat_arr))
      #print(lons,lats)

      x,y = mp(lons, lats)
      #print(len(x),len(y))

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, avg_tmin2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("mean avg tmin value(in mm)")

      plt.title('Mean Annual Tmin')
      plt.savefig( os.path.join(self.path,"Mean Annual Tmin.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_arr,self.lat_arr,avg_tmin2d)
      plt.clim(np.min(tmin_avg), np.max(tmin_avg))
      cbar = plt.colorbar()
      cbar.set_label('Mean Annual Tmax Values', rotation=270)

      plt.title('Mean Annual Tmax')
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('longitude')
      axes.set_ylabel('latitude')

      plt.savefig(os.path.join(self.path,"Mean Annual Tmin.jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")

  def change_analysis_tmin(self) :
      df = self.data_annual_tmin.iloc[len(self.year_count)//2:].mean()-self.data_annual_tmin[0:len(self.year_count)//2].mean()
      tmin_diff=df.to_numpy(dtype = np.float64())

      diff_tmin2d = np.empty((len(self.lat_arr),len(self.lon_arr)))
      diff_tmin2d[:] = np.NaN

      x = 0
      m = 0
      for i in self.lat_arr:
        n = 0
        for j in self.lon_arr:
          if x == len(self.point_ids)-1:
            break
          if (i,j) == ((self.lonlat)["latitude"][x],(self.lonlat)["longitude"][x]) :
            diff_tmin2d[m][n] = tmin_diff[x]
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
      #print(len(lon_arr),len(lat_arr))
      #print(lons,lats)

      x,y = mp(lons, lats)
      #print(len(x),len(y))

      mp.drawcoastlines()
      mp.drawcountries()

      c_scheme = mp.pcolor(x, y, diff_tmin2d , cmap = 'jet')

      cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')
      cbar.set_label("change in tmin value(in C)")

      plt.title('Annual tmin Difference')
      plt.savefig( os.path.join(self.path,"Annual tmin Difference.jpg"), bbox_inches='tight', dpi=400)
      plt.show()
      plt.close("all")
      '''

      plt.pcolormesh(self.lon_arr,self.lat_arr,diff_tmin2d)
      plt.clim(-1*np.max(tmin_diff), np.max(tmin_diff))
      cbar = plt.colorbar()
      cbar.set_label('Annual Tmin Difference Values', rotation=270)

      plt.title('Annual Tmin Difference')
      
      axes = plt.gca()
      axes.set_xlim([np.min(self.lon_arr) - 2, np.max(self.lon_arr) + 2])
      axes.set_ylim([np.min(self.lat_arr) - 2, np.max(self.lat_arr) + 2])
      axes.set_xlabel('longitude')
      axes.set_ylabel('latitude')

      plt.savefig(os.path.join(self.path,"Annual Tmin Difference.jpg"), bbox_inches='tight', dpi=400)

      plt.show()
      plt.close("all")