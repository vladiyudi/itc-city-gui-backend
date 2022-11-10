import redis 
import json
from threading import Lock
import os
import threading
import random
import time

lock = Lock()

class Live_Stream():
    def __init__(self):
        self.REDIS_IP = os.getenv('MOCK_UP_REDIS')
        self.REDIS_PORT = os.getenv('MOCK_UP_REDIS_PORT')
        self.REDIS_PASSWORD = os.getenv('MOCK_UP_REDIS_PASSWORD')
        # self.r = redis.Redis(host ='localhost', port = 6379)
        self.r = redis.Redis(host=self.REDIS_IP, port=self.REDIS_PORT, password=self.REDIS_PASSWORD)
        
    def generate_live_stream(self):
        mylist = range(10)
        while True:
            global lock 
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
            global lock 
            barChart_stream = self.r.get('bar chart')
            barChart_stream = barChart_stream.decode('utf-8')
            yield barChart_stream
            time.sleep(5)  
            
            
    def generate_mock_waiting(self):
        threading.Timer(5.0, self.generate_mock_waiting).start()
        data = {"vehicles":{
            "lane11":bool(random.getrandbits(1)),
            'lane12':bool(random.getrandbits(1)),
            'lane13':bool(random.getrandbits(1)),
            'lane14':bool(random.getrandbits(1)),
            'lane21':bool(random.getrandbits(1)),
            'lane22':bool(random.getrandbits(1)),
            'lane31':bool(random.getrandbits(1)),
            'lane32':bool(random.getrandbits(1)),
        },
            'peds':{
                "place1":random.randint(0, 10),
                'place2':random.randint(0, 10),
                'place3':random.randint(0, 10),
                'place4':random.randint(0, 10),
                'place5':random.randint(0, 10),
            }  
        }
        self.r.set('waiting', json.dumps(data))        
    
    def generate_waiting_stream(self):
        while True:
            global lock 
            waiting_stream = self.r.get('waiting')
            waiting_stream = waiting_stream.decode('utf-8')
            yield waiting_stream
            time.sleep(5)