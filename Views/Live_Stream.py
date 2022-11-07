import redis 
import json
from threading import Lock
import os
import threading
import random
import time

class Live_Stream():
    def __init__(self):
        self.SERVER_IP = os.getenv('SERVER_IP')
        self.r = redis.Redis(host=self.SERVER_IP, port=6379)
        self.lock = Lock()
        
    def generate_live_stream(self):
        mylist = range(10)
        while True:
            live_stream = self.r.get('vehicles real time')
            live_stream = live_stream.decode('utf-8')
            yield live_stream
            time.sleep(5)
         
    def generate_mock_data(self):
        threading.Timer(5.0, self.generate_mock_data).start()
        cars = random.randint(1,100)
        trucks = random.randint(1,100)
        buses = random.randint(1,100)
        pedestrians = random.randint(1,100)
        self.r.set('vehicles real time', json.dumps({"cars":cars, "trucks":trucks, "buses":buses, "pedestrians":pedestrians}))
        
        
    def generate_mock_barChart(self):
        threading.Timer(5.0, self.generate_mock_barChart).start()
        barChart = {"data":[   
        {"data": random.randint(0, 60), "icon": 'phase1'},
        {"data": random.randint(0, 60), "icon": 'phase2'},
        {"data": random.randint(0, 60), "icon": 'phase3'},
        {"data": random.randint(0, 60), "icon": 'phase4'},
        {"data": random.randint(0, 60), "icon": 'phase5'},
        {"data": random.randint(0, 60), "icon": 'phase6'},
        ]}
        self.r.set('bar chart', json.dumps(barChart))
        
    def generate_barChart_stream(self):
        while True:
            barChart_stream = self.r.get('bar chart')
            barChart_stream = barChart_stream.decode('utf-8')
            yield barChart_stream
            time.sleep(5)    
    
        