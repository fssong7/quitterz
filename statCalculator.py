# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
from datetime import date,timedelta,datetime
import pytz
from mongoDB import database
import pandas as pd
# import df
# find 7 day average, 30 day average, all time average

from inputs import people

class dataAnalyzer():
    def __init__(self):
        self.mongo = database()

        self.db = {
            person["name_first"]: pd.DataFrame(
                list(self.mongo.collection.find({"name": person["name_first"]}))
            )
            for person in people
        }
        # print(self.db)


        self.drop_id()

    def update_db(self):
        self.db = {
            person["name_first"]: pd.DataFrame(
                list(self.mongo.collection.find({"name": person["name_first"]}))
            )
            for person in people
        }
        self.drop_id()

    def drop_id(self):
        column = '_id'
        for key, df in self.db.items():
            if column in df.columns:
                self.db[key] = df.drop(column, axis=1)
        

    def todays_entry(self,db):
        eastern_tz = pytz.timezone("US/Eastern")
        todays_date = datetime.now(eastern_tz).strftime("%Y-%m-%d")
        #todays_date = date.today().strftime("%Y-%m-%d")
        dates = db['date'].astype(str)
        #print(todays_date)
        index_check = -1
        for index,value in dates.items():
            if value == todays_date:
                #print(index)
                index_check = index
            else:
                continue
        if index_check >= 0:
            return index_check
        else:
            return(-1)
        
    def seven_days(self,db):
        seven_days_ago = datetime.now() - timedelta(days=7)
        try:
            db['date'] = pd.to_datetime(db['date'])
        except KeyError:
            db['date'] = pd.Series(dtype='datetime64[ns]')
        db['date'] = pd.to_datetime(db['date'])
        recent_dates_db = db[db['date'] > seven_days_ago]
        recent_dates_db = recent_dates_db.drop_duplicates(subset=['date'],keep='last')
        recent_dates_db = recent_dates_db.sort_values(by='date',ascending=False)
        mean = recent_dates_db['dval'].mean()
        std = recent_dates_db['dval'].std()
        return recent_dates_db,mean,std

    def thirty_days(self,db):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        try:
            db['date'] = pd.to_datetime(db['date'])
        except KeyError:
            db['date'] = pd.Series(dtype='datetime64[ns]')
        recent_dates_db = db[db['date'] > thirty_days_ago]
        recent_dates_db = recent_dates_db.drop_duplicates(subset=['date'],keep='last')
        recent_dates_db = recent_dates_db.sort_values(by='date',ascending=False)
        mean = recent_dates_db['dval'].mean()
        std = recent_dates_db['dval'].std()
        return recent_dates_db,mean,std
    
    def all_time(self,db):
        
        db = db.drop_duplicates(subset=['date'],keep='last')
        db = db.sort_values(by='date',ascending=False)
        mean = db['dval'].mean()
        std = db['dval'].std()
        return db,mean,std