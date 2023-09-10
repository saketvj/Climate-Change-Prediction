import pandas as pd
import numpy as np

class PrecipitationIndices:
    def __init__(self, data_prcp, year_count, month_count,point_ids):
        self.data_prcp = data_prcp
        self.year_count = year_count
        self.month_count = month_count
        self.point_ids = point_ids

    def monthly_rx1day(self) :
        """
        Monthly maximum 1-day precipitation
        """
        data_prcp = self.data_prcp.groupby(by=["year","month"] , dropna = False)[self.point_ids].max()
        #data_prcp.drop(labels = ["day"] , axis=1, inplace = True)
        return data_prcp

    def monthly_rx5day(self) :
        """
        Monthly maximum 5-day precipitation
        """
        def cons_max(df_prcp,n):
          max_loc = np.convolve(df_prcp, np.ones(n, dtype=float), mode='valid').argmax()
          return df_prcp.loc[max_loc:max_loc+4].sum()

        """
        data_prcp['date']=pd.date_range("1951-01-01",periods=23376,freq='1d')
        """

        """
        data_prcp["year"] = data_prcp["year"].astype(np.int64)
        data_prcp["month"] = data_prcp["month"].astype(np.int64)
        data_prcp["day"] = data_prcp["day"].astype(np.int64)

        data_prcp.insert(3,"date",pd.to_datetime(data_prcp["year"].astype(np.str) + "/" + data_prcp["month"].astype(np.str) + "/" + data_prcp["day"].astype(np.str)),True)
        """

        """
        year_count = np.arange(1951,1952,1)
        month_count = np.arange(1,13,1)

        for i in year_count :
          df_prcp_year = data_prcp[data_prcp["year"] == i]
          for j in month_count :
            df_prcp_month = df_prcp_year[df_prcp_year["month"] == j]
            size = df_prcp_month["day"].size
            for k in range(1 , size - 4 , 1) :
              df_prcp_daily5 = df_prcp_month[k:k+5].sum()
        """

        max_prcp5=np.array([])

        for i in self.year_count :
          df_prcp_year = self.data_prcp[self.data_prcp["year"] == i]
          for j in self.month_count :
            df_prcp_month = df_prcp_year[df_prcp_year["month"] == j]
            df_prcp_month.reset_index(inplace = True , drop = True)
            for k in self.point_ids:
              max_prcp5=np.append(max_prcp5,cons_max(df_prcp_month.loc[ : ,k] , 5))

        df_prcp_max_prcp5 = pd.DataFrame(np.reshape(max_prcp5,(len(self.year_count)*len(self.month_count),len(self.point_ids))), columns=self.point_ids)

        index = pd.date_range(start = str(self.year_count[0]),end = str(self.year_count[-1] + 1) ,freq = "M")
        df_prcp_max_prcp5.set_index(index , drop = True, inplace = True)

        return df_prcp_max_prcp5
        
    def annually_rx5day(self) :
        """
        Monthly maximum 5-day precipitation
        """
        def cons_max(df_prcp,n):
          max_loc = np.convolve(df_prcp, np.ones(n, dtype=float), mode='valid').argmax()
          return df_prcp.loc[max_loc:max_loc+4].sum()
        
        max_prcp5=np.array([])

        for i in self.year_count :
          df_prcp_year = self.data_prcp[self.data_prcp["year"] == i]
          df_prcp_year.reset_index(inplace = True , drop = True)
          for k in self.point_ids:
            max_prcp5=np.append(max_prcp5,cons_max(df_prcp_year.loc[ : ,k] , 5))

        df_prcp_max_prcp5 = pd.DataFrame(np.reshape(max_prcp5,(len(self.year_count),len(self.point_ids))), columns=self.point_ids)
        df_prcp_max_prcp5["year"] = self.year_count
        df_prcp_max_prcp5.set_index("year", drop=True , inplace = True)

        return df_prcp_max_prcp5    

    def annual_rnmm(self , n):
        """
        Annual count of days when precipitation exceeds n mm.
        """
        #data_prcp.iloc[0:10 , 0:10]
        #data_prcp = data_prcp.loc[ : , ["year","month","day",1,2,3,4,5,6,7,8,9,10]]
        
        df_prcp_nmm = pd.DataFrame([])
        df_prcp_nmm["year"] = self.year_count
        df_prcp_nmm.set_index("year", drop=True , inplace = True)

        for i in self.point_ids:
            nmm = self.data_prcp[self.data_prcp[i]>n]
            df_prcp_nmm[i] = nmm.groupby(by = ["year"]).size()

        df_prcp_nmm.fillna(0 , inplace = True)    
        return df_prcp_nmm  

    def prcptot(self) :
        """
        Total precipitation over 'period' (default: annual)
        """
        data_prcp = self.data_prcp.groupby("year")[self.point_ids].sum()
        return data_prcp
    
  
    def cdd_monthly(self) :
        """
        Number of consecutive dry days in 'period' (default: monthly)
        """
        maxm_consecutive_dday=np.array([])

        for i in self.year_count :
          df_prcp_year = self.data_prcp[self.data_prcp["year"] == i]
          for j in self.month_count :
            df_prcp_month = df_prcp_year[df_prcp_year["month"] == j]
            for k in self.point_ids:
              df_prcp_point=df_prcp_month[k].to_numpy()
              count=0
              maxm=0
              for l in df_prcp_point:
                if l<=1:
                  count=count+1
                else:
                  maxm=max(maxm,count)
                  count=0
              maxm_consecutive_dday=np.append(maxm_consecutive_dday,maxm)

        maxm_consecutive_dday = pd.DataFrame(np.reshape(maxm_consecutive_dday,(len(self.year_count)*len(self.month_count),len(self.point_ids))) , columns=self.point_ids)

        index = pd.date_range(start = str(self.year_count[0]),end = str(self.year_count[-1] + 1) ,freq = "M")
        maxm_consecutive_dday.set_index(index , drop = True, inplace = True)
        #maxm_consecutive_dday["date"] = maxm_consecutive_dday.index

        return maxm_consecutive_dday

    def cdd_annually(self) :
        """
        Number of consecutive dry days in 'period' (default: annually)
        """
        maxm_consecutive_dday=np.array([])

        for i in self.year_count :
          df_prcp_year = self.data_prcp[self.data_prcp["year"] == i]
          for k in self.point_ids:
            df_prcp_point=df_prcp_year[k].to_numpy()
            count=0
            maxm=0
            for l in df_prcp_point:
              if l<=1:
                count=count+1
              else:
                maxm=max(maxm,count)
                count=0
            maxm_consecutive_dday=np.append(maxm_consecutive_dday,maxm)

        maxm_consecutive_dday = pd.DataFrame(np.reshape(maxm_consecutive_dday,(len(self.year_count),len(self.point_ids))) , columns=self.point_ids)
        maxm_consecutive_dday["year"] = self.year_count
        maxm_consecutive_dday.set_index("year", drop=True , inplace = True)

        return maxm_consecutive_dday
    
    def cwd_monthly(self):
        """
        Number of consecutive wet days in 'period' (default: monthly)
        """
        maxm_consecutive_wday=np.array([])

        for i in self.year_count :
          df_prcp_year = self.data_prcp[self.data_prcp["year"] == i]
          for j in self.month_count :
            df_prcp_month = df_prcp_year[df_prcp_year["month"] == j]
            for k in self.point_ids:
              df_prcp_point=df_prcp_month[k].to_numpy()
              count=0
              maxm=0
              for l in df_prcp_point:
                if l>=1:
                  count=count+1
                else:
                  maxm=max(maxm,count)
                  count=0
              maxm_consecutive_wday=np.append(maxm_consecutive_wday,maxm)

        maxm_consecutive_wday = pd.DataFrame(np.reshape(maxm_consecutive_wday,(len(self.year_count)*len(self.month_count),len(self.point_ids))) , columns = self.point_ids)

        index = pd.date_range(start = str(self.year_count[0]),end = str(self.year_count[-1] + 1) ,freq = "M")
        maxm_consecutive_wday.set_index(index , drop = True, inplace = True)
        #maxm_consecutive_wday["date"] = maxm_consecutive_wday.index

        return maxm_consecutive_wday

    def cwd_annually(self):
        """
        Number of consecutive wet days in 'period' (default: monthly)
        """
        maxm_consecutive_wday=np.array([])

        for i in self.year_count :
          df_prcp_year = self.data_prcp[self.data_prcp["year"] == i] 
          for k in self.point_ids:
              df_prcp_point=df_prcp_year[k].to_numpy()
              count=0
              maxm=0
              for l in df_prcp_point:
                if l>=1:
                  count=count+1
                else:
                  maxm=max(maxm,count)
                  count=0
              maxm_consecutive_wday=np.append(maxm_consecutive_wday,maxm)

        maxm_consecutive_wday = pd.DataFrame(np.reshape(maxm_consecutive_wday,(len(self.year_count),len(self.point_ids))) , columns = self.point_ids)
        maxm_consecutive_wday["year"] = self.year_count
        maxm_consecutive_wday.set_index("year", drop=True , inplace = True)

        return maxm_consecutive_wday

    def wet_days(self) :
        df_prcp_nmm = pd.DataFrame([])
        df_prcp_nmm["year"] = self.year_count
        df_prcp_nmm.set_index("year", drop=True , inplace = True)

        for i in self.point_ids:
            nmm = self.data_prcp[self.data_prcp[i]>1]
            df_prcp_nmm[i] = nmm.groupby(by = ["year"]).size()

        df_prcp_nmm.fillna(0 , inplace = True)    
        return df_prcp_nmm
    
    def sdii(self):
        """
        Simple precipitation intensity index. Ratio of total precipitation of period to the number of wet days.
        """
      
        return self.prcptot().div(self.wet_days())