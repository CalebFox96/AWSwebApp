
from flask import Flask, request, render_template
import time
import datetime
import sys
#import Adafruit_DHT
import sqlite3
import random

app = Flask(__name__)
app.debug = True # Set this to true to allow debugging

@app.route("/sensor")
def lab_temp():
    BeatsPerMin = random.randint(65,70)
    Bpressure = random.randint(70,75)
    humidity = random.randint(40,45)
    temperature = random.randint(25,29)
    #humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 16)
    if humidity is not None and temperature is not None and BeatsPerMin is not None and Bpressure is not None:
        return render_template("sensor.html",temp=temperature,hum=humidity,
        bpm=BeatsPerMin,bp=Bpressure)


@app.route("/", methods=['GET']) 
def lab_env_db():
    temperature,  bpm, bPressure,humidity, fromDateValue,toDateValue = fetch_records()
    return render_template( "lab_env_db.html",
                            temp = temperature,
                            hum  = humidity,
                            beats = bpm,
                            bp = bPressure,
                            from_date = fromDateValue, 
                            to_date = toDateValue,
                            temp_items = len(temperature),
                            hum_items = len(humidity),
                            bpm_items = len(bpm),
                            bp_items = len(bPressure))

 
def fetch_records():
    fromDateValue   = request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
    toDateValue     = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
    
    DateTimeRange    = request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
    rangeInitializer     = "nan"  #initialise this variable with not a number

    try: 
        rangeInitializer = int(DateTimeRange)
    except:
        print ("DateTimeRange not a number")

    if not validate_date(fromDateValue):            # Validate date before sending it to the DB
        fromDateValue    = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(toDateValue):
        toDateValue     = time.strftime("%Y-%m-%d %H:%M")       # Validate date before sending it to the DB

        # If range_h is defined, we don't need the from and to times
    if isinstance(rangeInitializer,int): 
        timeNow = datetime.datetime.now()
        timeFrom = timeNow - datetime.timedelta(hours = rangeInitializer)
        timeTo = timeNow
        fromDateValue = timeFrom.strftime("%Y-%m-%d %H:%M")
        toDateValue = timeTo.strftime("%Y-%m-%d %H:%M")
    
    conn=sqlite3.connect('/home/ubuntu/lab_app.db') #Connects to the database
    curs=conn.cursor()
    curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (fromDateValue, toDateValue))
    temperature    = curs.fetchall()
    curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (fromDateValue, toDateValue))
    humidity      = curs.fetchall()
    curs.execute("SELECT * FROM bpm WHERE rDateTime BETWEEN ? AND ?", (fromDateValue, toDateValue))
    bpm             = curs.fetchall()
    curs.execute("SELECT * FROM bPressure WHERE rDateTime BETWEEN ? AND ?", (fromDateValue, toDateValue))
    bPressure       = curs.fetchall()
    conn.close()
    return [temperature,bpm,bPressure, humidity,fromDateValue, toDateValue]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
