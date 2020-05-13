#!/usr/bin/env python

import sqlite3
import sys
import random
import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    data = str(message.payload.decode("utf-8")).split(",")
    print(data)
    temperature = data[0]
    humidity = data[1]
    bpm = data[2]
    bPressure = data[3]
    print(data[0],data[1],data[2],data[3])
    log_values("1", temperature, humidity,bpm,bPressure) 
    
    
broker_address="52.91.209.21"

print("creating new instance")
client = mqtt.Client("VM") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address,1883) #connect to broker
client.subscribe("test")

def log_values(sensor_id, temp, hum,bpm,bPressure):
    conn=sqlite3.connect('/home/ubuntu/lab_app.db')  #It is important to provide an
                                 #absolute path to the database
                                 #file, otherwise Cron won't be
                                 #able to find it!
    curs=conn.cursor()
    curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,temp))
    curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,hum))
    curs.execute("""INSERT INTO bpm values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,bpm))
    curs.execute("""INSERT INTO bPressure values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,bPressure))
    conn.commit()
    conn.close()
client.loop_forever()

