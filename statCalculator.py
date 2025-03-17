# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
from datetime import date,timedelta,datetime
from mongoDB import database
import pandas as pd
# import df
# find 7 day average, 30 day average, all time average
class dataAnalyzer():
    def __init__(self):
        self.db = database()
        self.saradb = pd.DataFrame(list(self.db.collection.find({"name":"sara"})))
        #print(self.saradb.keys())
        self.gracedb = pd.DataFrame(list(self.db.collection.find({"name":"grace"})))
        self.forestdb = pd.DataFrame(list(self.db.collection.find({"name":"forest"})))
        self.seven_days(self.saradb)

    def todays_entry(self,db):
        todays_date = date.today().strftime("%Y-%m-%d")
        #print(self.saradb['date'])
        dates = db['date'].astype(str)

        index_check = 0
        for index,value in dates.items():
            if value == todays_date:
                #print(index)
                index_check = index
            else:
                continue
        if index_check > 0:
            return index_check
        else:
            return(-1)
        
    def seven_days(self,db):
        seven_days_ago = datetime.now() - timedelta(days=7)
        db['date'] = pd.to_datetime(db['date'])
        recent_dates_db = db[db['date'] > seven_days_ago]
        recent_dates_db = recent_dates_db.drop_duplicates(subset=['date'],keep='last')
        mean = recent_dates_db['dval'].mean()
        std = recent_dates_db['dval'].std()
        return recent_dates_db,mean,std

    def thirty_days(self,db):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        db['date'] = pd.to_datetime(db['date'])
        recent_dates_db = db[db['date'] > thirty_days_ago]
        recent_dates_db = recent_dates_db.drop_duplicates(subset=['date'],keep='last')
        mean = recent_dates_db['dval'].mean()
        std = recent_dates_db['dval'].std()
        return recent_dates_db,mean,std
    
    def all_time(self,db):
        db = db.drop_duplicates(subset=['date'],keep='last')
        mean = db['dval'].mean()
        std = db['dval'].std()
        return db,mean,std