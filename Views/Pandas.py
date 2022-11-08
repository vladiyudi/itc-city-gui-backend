from time import strftime, strptime
import pandas as pd
import re
import datetime as dt
import glob


class Pandas:
    def __init__(self):
        # self.df = pd.read_csv('TLVTrafficCounting15-2022-08-22.csv')
        self.df = pd.read_csv(
            'GoldCoast/GoldenCoastTrafficCounting-2022-10-23.csv')
        # self.dataset = glob.glob('TLV CVC/*.csv')
        self.dataset = glob.glob('GoldCoast/*.csv')
        self.days = self.get_days()

    def build_multipledays_chart(self, start_date, end_date, vehicle, directions, weekdays):
        check = list(self.days[0].values())[0]
        vehicle_columns = self.get_cols(check)[vehicle]
        vehicle_columns = self.filter_by_direction(directions, vehicle_columns)
        chart = []
        days = self.get_history_period(start_date, end_date)
        days = self.filter_by_weekdays(weekdays, days)
        for day in days:
            d = list(day.values())[0]
            sum = 0
            for column in vehicle_columns:
               sum += d[column].sum()
            now = list(str(list(day.keys())[0]))
            # now = "20"+now[0]+now[1]+"-"+now[2]+now[3]+"-"+now[4]+now[5]
            now = now[0]+now[1]+now[2]+now[3] + \
                "-"+now[4]+now[5]+"-"+now[6]+now[7]
            chart.append([now, int(sum)])

        return chart

    def filter_by_weekdays(self, weekdays, period):
        days = []
        result = []

        if weekdays['allDays'] == 'true':
            return self.filter_by_weekends(weekdays, period)

        if weekdays['mondays'] == 'true':
            days.append(0)
        if weekdays['tuesdays'] == 'true':
            days.append(1)
        if weekdays['wednesdays'] == 'true':
            days.append(2)
        if weekdays['thursdays'] == 'true':
            days.append(3)
        if weekdays['fridays'] == 'true':
            days.append(4)
        if weekdays['saturdays'] == 'true':
            days.append(5)
        if weekdays['sundays'] == 'true':
            days.append(6)

        for day in period:
            now = list(str(list(day.keys())[0]))
            now = now[0]+now[1]+now[2]+now[3] + \
                "-"+now[4]+now[5]+"-"+now[6]+now[7]
            now = strptime(now, "%Y-%m-%d").tm_wday
            for d in days:
                if now == d:
                  result.append(day)

        return result

    def filter_by_weekends(self, weekdays, period):
      if weekdays['includeWeekends'] == 'true':
        return period
      else:
          result = []
          for day in period:
            now = list(str(list(day.keys())[0]))
            now = now[0]+now[1]+now[2]+now[3] + \
                "-"+now[4]+now[5]+"-"+now[6]+now[7]
            now = strptime(now, "%Y-%m-%d").tm_wday
            if now == 5 or now == 6:
              result.append(day)
          return result

    def get_days(self):
        days = []
        for file in self.dataset:
            df = pd.read_csv(file)
            # key = int(file.split('-')[1].split('.')[0])
            x = file.split('-')
            key = int(x[1]+x[2] + x[3].split('.')[0])
            days.append({key: df})
            days = sorted(days, key=lambda x: list(x.keys())[0])
        return days

    def build_zero_history_chart(self, start_date, end_date):
        chart = []
        days = self.get_history_period(start_date, end_date)
        for day in days:
            now = list(str(list(day.keys())[0]))
            now = now[0]+now[1]+now[2]+now[3] + \
                "-"+now[4]+now[5]+"-"+now[6]+now[7]
            # now = "20"+now[0]+now[1]+"-"+now[2]+now[3]+"-"+now[4]+now[5]
            chart.append([now, 0])
        return chart

    def get_history_period(self, start_date, end_date):
        control = False
        period = []
        for day in self.days:
          now = list(str(list(day.keys())[0]))
          now = now[0]+now[1]+now[2]+now[3]+"-"+now[4]+now[5]+"-"+now[6]+now[7]
        #   now = "20"+now[0]+now[1]+"-"+now[2]+now[3]+"-"+now[4]+now[5]
          if now == start_date:
            control = True
          if control:
            period.append(day)
          if now == end_date:
            return period

    def get_vehicals_columns(self):
        vehicle_columns = []
        car = []
        bus = []
        truck = []
        van = []
        motorbike = []
        person = []
        vehicals = []
        for column in self.df.columns:
            if re.search('(car|truck|bus|motorbike|van|person)', column):
                vehicle_columns.append(column)
            if re.search('(car|truck|bus|motorbike|van)', column):
                vehicals.append(column)
            if re.search('car', column):
                car.append(column)
            if re.search('bus', column):
                bus.append(column)
            if re.search('truck', column):
                truck.append(column)
            if re.search('van', column):
                van.append(column)
            if re.search('motorbike', column):
                motorbike.append(column)
            if re.search('person', column):
                person.append(column)
        return {"all": vehicle_columns, "car": car, "bus": bus, "truck": truck, "van": van, "motorbike": motorbike, 'person': person, 'vehicals': vehicals}

    def get_time_period(self, start_time, end_time, day):
        
        day = self.select_day(day)
        day = list(day.values())[0]
        
        
        start = '0'
        finish = '95'
        for i, row in day.iterrows():
            if row['Start'] == start_time:
                start = i
            if row['Start'] == end_time:
                finish = i
        period = day.iloc[start:finish]
        return period
    
    
    

    def filter_by_direction(self, directions, columns):
       ways = []
       cols = []
       if directions['north_south'] == 'true':
           ways.append('1')
       if directions['east_west'] == 'true':
           ways.append('2')
       if directions['south_north'] == 'true':
           ways.append('3')
       if directions['west_east'] == 'true':
           ways.append('4')

       for way in ways:
           for column in columns:
               if re.search("^"+way, column):
                   cols.append(column)

       return cols

    def count_vehicles(self, start_time, end_time, day):
        period = self.get_time_period(start_time, end_time, day)
        vehicle_columns = self.get_vehicals_columns()
        # vehicle_columns = self.filter_by_direction(directions, vehicle_columns['all'])
        car = 0
        truck = 0
        bus = 0
        ped = 0
        for i, row in period.iterrows():
            for column in vehicle_columns['car']:
                car += row[column]
            for column in vehicle_columns['bus']:
                bus += row[column]
            for column in vehicle_columns['truck']:
                truck += row[column]
            for column in vehicle_columns['person']:
                ped += row[column]
        return {"cars": car, "busses": bus, "trucks": truck, "pedestrians": ped}

    def count_history_vehicals(self, start, end):
        period = self.get_history_period(start, end)
        vehicle_columns = self.get_vehicals_columns()
        car = 0
        truck = 0
        bus = 0
        ped = 0
        for day in period:
            day = list(day.values())[0]
            for i, row in day.iterrows():
                    for column in vehicle_columns['car']:
                        car += row[column]
                    for column in vehicle_columns['bus']:
                         bus += row[column]
                    for column in vehicle_columns['truck']:
                        truck += row[column]  
                    for column in vehicle_columns['person']:
                        ped += row[column]                 
        return {"cars": car, "busses": bus, "trucks": truck, "pedestrians": ped} 
            
    def select_day(self, day):
        for file in self.days:
            now = list(str(list(file.keys())[0]))
            now = now[0]+now[1]+now[2]+now[3]+"-"+now[4]+now[5]+"-"+now[6]+now[7]
            if now == day:
                return file
    
    def build_vehicles_chart(self, start_time, end_time, vehicle, directions, day):
        
       
        
        # print(self.df)
        
        period = self.get_time_period(start_time, end_time, day)
        vehicle_columns = self.get_vehicals_columns()[vehicle]
        vehicle_columns = self.filter_by_direction(directions, vehicle_columns)
        chart = []
        for i, row in period.iterrows():
            time = row['Start']
            time = pd.to_datetime(time)
            sum = 0
            for column in vehicle_columns:
                sum += row[column]
            chart.append([time, sum])  
        return chart  
    
    def build_zero_chart(self, start_time, end_time, day):
        period = self.get_time_period(start_time, end_time, day)
        chart = []
        for i, row in period.iterrows():
            time = row['Start']
            time = pd.to_datetime(time)
            chart.append([time, 0])
        return chart
    
    def get_lanes(self, start_time, end_time, day):
        period = self.get_time_period(start_time, end_time, day)

        lanes = {
            '11': 0,
            '12': 0,
            '13': 0,
            '14': 0,
            '21': 0,
            '22': 0,
            '31': 0,
            '32': 0,
        }
        
        peds = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
        }
        
        peds_cols ={}
        
        col11 = self.get_lanes_columns('11')
        col12 = self.get_lanes_columns('12')
        col13 = self.get_lanes_columns('13')
        col14 = self.get_lanes_columns('14')
        col21 = self.get_lanes_columns('21')
        col22 = self.get_lanes_columns('22')
        col31 = self.get_lanes_columns('31')
        col32 = self.get_lanes_columns('32')
        
        for ped in peds:
            peds_cols[ped] = self.get_lanes_columns(ped, 'person')
                           
        for i, row in period.iterrows():
            for column in col11:
                lanes['11']+= row[column]
            for column in col12:
                lanes['12']+= row[column]
            for column in col13:
                lanes['13']+= row[column]
            for column in col14:
                lanes['14']+= row[column]    
            for column in col21:
                lanes['21']+= row[column]
            for column in col22:
                lanes['22']+= row[column]
            for column in col31:
                lanes['31']+= row[column]
            for column in col32:
                lanes['32']+= row[column]  
            for ped in peds:
                for column in peds_cols[ped]:
                    peds[ped] += row[column]
                                                           
        return {"vehicals":lanes, "peds":peds}    
            
            
    def get_lanes_columns(self, direction, type='vehicals'):
        lane = []
        columns = self.get_vehicals_columns()[type]
        for column in columns:
            if re.search("^"+direction, column):
                lane.append(column)
        return lane      
    
    def get_cols(self, source):
        vehicle_columns = []
        car=[]
        bus = []
        truck = []
        van = []
        motorbike = []
        person=[]
        for column in source.columns:
            if re.search('(car|truck|bus|motorbike|van|person)', column):
                vehicle_columns.append(column)
            if re.search('car', column):
                car.append(column)  
            if re.search('bus', column):
                bus.append(column)
            if re.search('truck', column):
                truck.append(column)   
            if re.search('van', column):
                van.append(column)  
            if re.search('motorbike', column):
                motorbike.append(column) 
            if re.search('person',column):
                person.append(column)                             
        return {"all":vehicle_columns, "car":car, "bus":bus, "truck":truck, "van":van, "motorbike":motorbike, 'person':person}
    
 