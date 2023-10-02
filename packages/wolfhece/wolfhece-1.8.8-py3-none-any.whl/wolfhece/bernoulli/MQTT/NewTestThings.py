from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from time import sleep
import logging
import os
import sys
import paho.mqtt.client as mqtt
import json
import time
import random
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
#insert the following information
username = "t.pirard@uliege.be"
password = "111122"
port=1883
DeviceToken = "guCnZNPPCPP6oA9NeE2Q"
topic = "v1/devices/me/attributes"
topic2 = "v1/devices/me/attributes/+"
topic3 = "v1/devices/me/attributes/1"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = 'http://iot4h2o.mv.uni-kl.de:8080/api/auth/login'
url = 'http://iot4h2o.mv.uni-kl.de:8080'
THINGSBOARD_HOST = 'iot4h2o.mv.uni-kl.de'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc) :
    if (rc==0) :
        print("connected OK Returned code = ", rc)
    else :
        print("Bad connection Returned code = ", rc)

def on_message(client, userdata, msg) :
    sleep(1)
    print (msg.topic + " " + str(msg.payload))  

def on_attributes_change(result, exception):
    sleep(1)
    if exception is not None:
        print("Exception: " + str(exception))
    else:
        print(result)
#Procédure générale
#Client HTTP qui récupère la valeur des attributs
with RestClientCE(base_url=url) as rest_client:
    try:
        # Auth with credentials
        rest_client.login(username=username, password=password)

#Client qui crée l'information
client = mqtt.Client()
client.on_message = on_message
client.on_subscribe=on_subscribe
client.username_pw_set(DeviceToken)
client.connect(THINGSBOARD_HOST, port, 20)
client.loop_start()
client.subscribe(topic2)
sleep(2)
# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=1
sensor_data = {'Temperature': 0, 'Humidity': 0}
Humidity=0
Temperature=1
next_reading = time() 

#On indique qu'on publie de nouvelles données

cpt=1
try:
    while cpt<21:
        Temperature=random.randint(0, 10)
        Humidity=random.randint(0, 20)
        sensor_data['Temperature'] = Temperature
        sensor_data['Humidity'] = Humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish(topic, json.dumps(sensor_data), 1)
        client.publish(topic3, json.dumps(sensor_data), 1)
        cpt+=1
        next_reading += INTERVAL
        sleep_time = next_reading-time()
        if sleep_time > 0:
            sleep(sleep_time)
except KeyboardInterrupt:
    pass
client.disconnect()
#client3.disconnect()
#client2.disconnect()
client.loop_stop()
#client2.loop_stop()