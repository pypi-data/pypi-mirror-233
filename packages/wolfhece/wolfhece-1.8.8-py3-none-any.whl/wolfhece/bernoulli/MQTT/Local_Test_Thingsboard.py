from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from time import sleep
import logging
import os
import sys
import paho.mqtt.client as mqtt
import json
import time
#import wolfpy
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
#insert the following information
username = "t.pirard@uliege.be"
password = "111122"
port=1883
DeviceToken = "guCnZNPPCPP6oA9NeE2Q"
topic = "v1/devices/me/telemetry"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = 'http://iot4h2o.mv.uni-kl.de:8080/api/auth/login'
url = 'http://iot4h2o.mv.uni-kl.de:8080'
url = 'iot4h2o.mv.uni-kl.de'

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'DHT22_DEMO_TOKEN'
THINGSBOARD_HOST=url
ACCESS_TOKEN=DeviceToken  
def on_publish(client,userdata,result):             #create function for callback
    print("data published to thingsboard \n")
    pass
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc) :
    if (rc==0) :
        print("connected OK Returned code = ", rc)
    else :
        print("Bad connection Returned code = ", rc)

def on_message(client, userdata, msg) :
    sleep(1)
    print (msg.topic + " " + str(msg.payload))  

#Procédure générale
client2 = mqtt.Client()
client2.on_connect = on_connect
client2.on_message = on_message

client2.username_pw_set(DeviceToken)
client2.connect(url , port, 40)
client2.subscribe(topic)
sleep(2)
# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=1

sensor_data = {'temperature': 0, 'humidity': 0}
humidity=0
temperature=1
next_reading = time() 

#Client qui crée l'information
client = mqtt.Client()
#On indique qu'on publie de nouvelles données
client.on_publish = on_publish
# Set access token
client.username_pw_set(ACCESS_TOKEN)
#client2.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, port, 20)
#client2.connect(THINGSBOARD_HOST, 1883, 10)

#client2.loop_start()

try:
    while temperature<21:
        #humidity,temperature = dht.read_retry(dht.DHT22, 4)
        humidity = humidity + 3
        temperature = temperature + 1
        #print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temperature, humidity))
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish(topic, json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time()
        if sleep_time > 0:
            sleep(sleep_time)
except KeyboardInterrupt:
    pass
client.disconnect()
client2.disconnect()
client.loop_stop()
client2.loop_stop()

