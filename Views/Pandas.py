import pandas as pd
import re

class Pandas:
    def __init__(self):
        self.df = pd.read_csv('TLVTrafficCounting15-2022-08-22.csv')
        
    def find_vehicle(self, vehicle):
        all = []
        for column in self.df.columns:
            if re.search(vehicle, column):
                all.append(column)
        return all 
    
    def get_all_vehicles(self):
        sum = 0
        for column in self.df.columns:
            if re.search('(car|truck|bus|motorbike|van)', column):
                sum += self.df[column].sum()
        # print (sum)   
        
        
    def get_vehicals_columns(self):
        vehicle_columns = []
        car=[]
        bus = []
        truck = []
        for column in self.df.columns:
            if re.search('(car|truck|bus|motorbike|van)', column):
                vehicle_columns.append(column)
            if re.search('car', column):
                car.append(column)  
            if re.search('bus', column):
                bus.append(column)
            if re.search('truck', column):
                truck.append(column)          
                
        return {"all":vehicle_columns, "car":car, "bus":bus, "truck":truck}            
        
        
    def build_basic_chart(self, start_date, end_date):
        period = self.get_time_period(start_date, end_date)
        vehicle_columns = self.get_vehicals_columns()['all']
        chart = []
        for i, row in period.iterrows():
            time = row['Start']
            time = pd.to_datetime(time)
            sum = 0
            for column in vehicle_columns:
                sum += row[column]
            chart.append([time, sum])            
        return chart  
    
    def get_time_period(self, start_date, end_date):
        start = '0'
        finish = '95'
        for i, row in self.df.iterrows():
            if row['Start']==start_date:
                start = i
            if row['Start']==end_date:
                finish = i    
        period = self.df.iloc[start:finish]         
        return period
    
    def count_vehicles(self, start_date, end_date):
        period = self.get_time_period(start_date, end_date)
        vehicle_columns = self.get_vehicals_columns()
        car = 0
        truck = 0
        bus = 0
        for i, row in period.iterrows():
            for column in vehicle_columns['car']:
                car += row[column]
        for time in period:
            for column in vehicle_columns['bus']:
                bus += row[column]
        for time in period:
            for column in vehicle_columns['truck']:
                truck += row[column]               
        return {"cars": car, "busses": bus, "trucks": truck}             
            
    def test(self):
        #multiple columns
        # df[['a','b']]
        
        # print content of specific column
        # print (self.df[[' 11  truck ']])
        
        # print (self.df[' 11  truck '].sum())
        
        # print (self.df)
        
        # print(self.df.iloc[1])
        
        
        return self.df