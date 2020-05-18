#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import sqlite3
import random
import Adafruit_DHT
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')
import paho.mqtt.client as mqtt
from time import *
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Define Variables
MQTT_HOST = "52.91.209.21"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "patientmonitor96@gmail.com"
password ="finalyear123"
receiver_email = "customer96@gmail.com"
# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
dbname='TempData.db'
sampleFreq = 60 #Sets sample freqency to 60




# Define on_publish event function
def on_publish(client, userdata, mid):
 print ("Message Published...")



# get data from DHT sensor
def getDHTdata():   
    
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 16
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum

# log sensor data on database
def logData (temp, hum):
    
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
    conn.commit()
    conn.close()
    
def sendmail(msg):
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("email sent")
    

def main():
    while True:
        temp, hum = getDHTdata()
        logData (temp, hum)
        bpm=random.randint(40,50)
        bp=random.randint(50,70)
        if temp > 100:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Temperature Alert"
            message["From"] = sender_email
            message["To"] = receiver_email
            text = "Temperature exceeds limit, last temperature value logged was "+str(temp)
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            sendmail(message)
    
        if bp > 100:
            message = MIMEMultipart("alternative")
            message["Subject"] = "BP Alert"
            message["From"] = sender_email
            message["To"] = receiver_email
            text = "BP exceeds limit, last BP value logged was "+str(bp)
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            sendmail(message)
            
        if hum > 100:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Humidity Alert"
            message["From"] = sender_email
            message["To"] = receiver_email
            text = "Humidity exceeds limit, last Humidity value logged was "+str(hum)
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            sendmail(message)
            
        if bpm > 100:
            message = MIMEMultipart("alternative")
            message["Subject"] = "BPM Alert"
            message["From"] = sender_email
            message["To"] = receiver_email
            text = "BP< exceeds limit, last BPM value logged was "+str(bpm)
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            sendmail(message)
    

            

        mqttc.publish("test",str(temp)+","+str(hum)+","+str(bpm)+","+str(bp))
        print(str(temp)+","+str(hum)+","+str(bpm)+","+str(bp))
        
        sleep(5) #Takes sensor sample every 60s

main()



