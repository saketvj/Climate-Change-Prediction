import pandas as pd
import numpy as np

class TemperatureIndices:
    def __init__(self,data_tmax, data_tmin, year_count , month_count, point_ids):
        self.data_tmax=data_tmax
        self.data_tmin=data_tmin
        self.year_count=year_count
        self.month_count=month_count
        self.point_ids=point_ids

    def annual_frost_days(self):
        df = pd.DataFrame([])
        df["year"] = self.year_count
        df.set_index("year", drop=True , inplace = True)

        for i in self.point_ids:
            n = self.data_tmin[self.data_tmin[i]<0]
            df[i] = n.groupby(by = ["year"]).size()

        df.fillna(0 , inplace = True)    
        return df

    def annual_tropical_nights(self):
        df = pd.DataFrame([])
        df["year"] = self.year_count
        df.set_index("year", drop=True , inplace = True)

        for i in self.point_ids:
            n = self.data_tmin[self.data_tmin[i]>20]
            df[i] = n.groupby(by = ["year"]).size()

        df.fillna(0 , inplace = True)    
        return df

    def annual_icing_days(self):
        df = pd.DataFrame([])
        df["year"] = self.year_count
        df.set_index("year", drop=True , inplace = True)

        for i in self.point_ids:
            n = self.data_tmax[self.data_tmax[i]<0]
            df[i] = n.groupby(by = ["year"]).size()

        df.fillna(0 , inplace = True)    
        return df

    def annual_summer_days(self):
        df = pd.DataFrame([])
        df["year"] = self.year_count
        df.set_index("year", drop=True , inplace = True)

        for i in self.point_ids:
            n = self.data_tmax[self.data_tmax[i]>25]
            df[i] = n.groupby(by = ["year"]).size()

        df.fillna(0 , inplace = True)    
        return df
    
    def monthly_txx(self):
        data_tmax = self.data_tmax.groupby(by=["year","month"] , dropna = False)[self.point_ids].max()
        return data_tmax
    
    def monthly_txn(self):
        data_tmax = self.data_tmax.groupby(by=["year","month"] , dropna = False)[self.point_ids].min()
        return data_tmax
    
    def monthly_tnx(self):
        data_tmin = self.data_tmin.groupby(by=["year","month"] , dropna = False)[self.point_ids].max()
        return data_tmin
    
    def monthly_tnn(self):
        data_tmin = self.data_tmin.groupby(by=["year","month"] , dropna = False)[self.point_ids].min()
        return data_tmin
    
    def daily_temperature_range(self):
        data_tmax=self.data_tmax.groupby(by=["year","month"] , dropna = False)[self.point_ids].mean()
        data_tmin=self.data_tmin.groupby(by=["year","month"] , dropna = False)[self.point_ids].mean()
        data_res = data_tmax.subtract(data_tmin)
        return data_res

    """
    def annual_growing_season_length(self, X: Union[xr.data_prcpArray, xr.data_prcpset], varname='MEANT'):
        raise NotImplementedError()
    """
