import datetime
import random
import time
import os
import csv
from csv import reader
import argparse
from influxdb import client as influxdb


db = influxdb.InfluxDBClient(host='influxdb', port=8086, database='mydb')
def read_data():
    with open('file.csv') as f:
        return [x.split(',') for x in f.readlines()[1:]]

a = read_data()

for metric in a:
    influx_metric = [{
        'measurement': 'your_measurement',
        'time': metric[0],
        'fields': {
             'value': metric[1]
        }
    }]
    db.write_points(influx_metric)