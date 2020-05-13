#!/usr/bin/env python

import sqlite3
import sys

import random

def log_values(sensor_id, temp, hum):
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

humidity = random.randint(20,40)
temperature = random.randint(20,40)
bpm = random.randint(30,150)
bPressure = random.randint(80,110)
# If you don't have a sensor but still wish to run this program, comment out all the 
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
if humidity is not None and temperature is not None:
    log_values("1", temperature, humidity)  
else:
    log_values("1", -999, -999)
if bpm is not None and bPressure is not None:
    log_values("1", bpm, bPressure)  
else:
    log_values("1", -999, -999)

