from influxdb import client as influxdb
import ast

db = influxdb.InfluxDBClient(host='influxdb', port=8086, database='mydb2')
def read_data():
    with open('metric.json') as f:
        return f.readlines()
        
a = read_data()

for metric in a:
    point = ast.literal_eval(metric)
    point['measurement'] = point['metricName']
    del point['metricName']
    influx_metric = [point]
    db.write_points(influx_metric)
