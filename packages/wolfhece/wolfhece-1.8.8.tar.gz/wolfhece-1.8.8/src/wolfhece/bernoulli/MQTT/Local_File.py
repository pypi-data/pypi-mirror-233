from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from time import sleep
import logging
import os
import sys
import paho.mqtt.client as mqtt
import json
import time
import random
import requests
import time
from datetime import datetime
from datetime import date
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
broker = 'iot4h2o.mv.uni-kl.de'
#logging.basicConfig(level=logging.DEBUG)

def callback(client, result):
    print(client, result)
    Test=1
def on_publish(client, userdata, result):
    # log.debug("Data published to ThingsBoard!")
    client.request_attributes(["sensorModel", "attribute_2"], callback=on_attributes_change)
    v=1
    pass
def on_attributes_change(client, result, exception):
    client.stop()
    sleep(3)
    if exception is not None:
        print("Exception: " + str(exception))
    else:
        print(result)

#insert the following information
username = "t.pirard@uliege.be"
username = "t.pirard@zwgs.de"
password = "111122"
#Example network
#DeviceID = "698e65a0-21c0-11ec-a052-af580412d5c6" 
DeviceToken = "guCnZNPPCPP6oA9NeE2Q"
EntryExample = ["temperature","humidity"]

#Definition of different usefull device token and usefull entries
#Production unit

DeviceKuhardt = "5124b960-7da1-11eb-81e7-7bf4b1b85926" #Wasserwerk Kuhardt : MengeL1 + MengeL2 +MengeLeimersheim
TokenKuhardt = "uRdOU74bNrwob2wJt6aR"
EntryKuhardt =['MengeL1','MengeL2','MengeLeimersheim']
DeviceJockgrim = "47a69c00-7da1-11eb-81e7-7bf4b1b85926" #Wasserwerk Jockgrim : Menge + Druck
TokenJockgrim = "VaHJOZvERK3iebpkilwT"
EntryJockgrim = ['Menge','Druck']

#Water towers : Wasserturm
NameTowers=['Hatz',"Rulz","Wor"]
DevicesWT=["39805350-7da1-11eb-81e7-7bf4b1b85926","308325c0-7da1-11eb-81e7-7bf4b1b85926","260db010-7da1-11eb-81e7-7bf4b1b85926"]
TokensWT=["n9IqRbv633DvwV8j6Zqb","8s7KqLd4jzIeGbblEauO","aKhhW6x92cFFEXybMFfa"]
EntryWT = ['Ablauf','Menge','Niveau']

#Booster system
DeviceKnittel = "5d4e7e30-f423-11eb-88d0-df9159a9b3d4" #Druckerhoehungsanlage - DEA Knittelsheim
TokenKnittel = "XoQ3yRVkWCmsDRqIyhuE"
#Vector for devices
DevicesID=[DeviceKuhardt,DeviceJockgrim,DevicesWT[0],DevicesWT[1],DevicesWT[2],DeviceKnittel]
#Vector for token
TokensID=[TokenKuhardt,TokenJockgrim,TokensWT[0],TokensWT[1],TokensWT[2],TokenKnittel]

#function for getting the token for the curl-command
def getCurlToken():
    url = 'http://iot4h2o.mv.uni-kl.de:8080/api/auth/login'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    loginJSON = {'username': username, 'password': password}
    tokenAuthResp = requests.post(url, headers=headers, json=loginJSON).json()
    token = tokenAuthResp['token']
    return token

#function for getting telemetry data
def GetTelemetryData(CurlToken,DeviceToken):
    url = 'http://iot4h2o.mv.uni-kl.de:8080/api/plugins/telemetry/DEVICE/'+DeviceToken+'/values/timeseries'
    headers = {'Content-Type': 'application/json', 'X-Authorization': 'Bearer '+CurlToken}
    telemetryDataResp = requests.get(url, headers=headers).json()
    #telemetryDataResp = requests.get(url).json()
    return telemetryDataResp

#Function to read the data in the file corresponding to the new_day

Basic_Directory='E:\\Network_Thomas\\Jockgrim_Data\\Data_'

#client = TBDeviceMqttClient(broker, TokensID[0])
#client.connect()  

INTERVAL=2
cpt=1
next_reading = time() 
PreviousDate = date.fromtimestamp(next_reading)
PreviousTimeStamp = time()
Filename=Basic_Directory+str(PreviousDate.year)+'_'+str(PreviousDate.month)+'_'+str(PreviousDate.day)+'.bin'
f = open(Filename, 'w')
LocalDevice=DeviceID
while cpt<5:
    Temperature=str(random.randint(0, 10))
    humidity=str(random.randint(0, 10))
    attributes = {"sensorModel": Temperature}
    telemetry = {"temperature": Temperature, "humidity": humidity}
    # Sending humidity and temperature data to ThingsBoard
    #client.send_telemetry(telemetry,1)
    cpt+=1
    next_reading += INTERVAL
    sleep_time = next_reading-time()
    telemetryData=GetTelemetryData(getCurlToken(),LocalDevice)
    keys = list(telemetryData.keys())
    TimeUsed=float(telemetryData[str(keys[0])][0]['ts']/1000)
    Temp_Data=telemetryData[EntryExample[1]][0]['value']
    if(PreviousTimeStamp!=TimeUsed):
        CurrentDate=date.fromtimestamp(TimeUsed)
        if(PreviousDate.day!=CurrentDate.day):
            #The previous file with the previous day is closed and the new file with the current day is opened
            Filename=Basic_Directory+str(CurrentDate.year)+'_'+str(CurrentDate.month)+'_'+str(CurrentDate.day)+'.bin'
            f.close()
            f = open(Filename, 'w')
        f.write(Temp_Data)
        f.write('\n')
        PreviousTimeStamp=TimeUsed
    #print(value)
    if sleep_time > 0:
        sleep(sleep_time)
client.disconnect()
f.close()
Test=1