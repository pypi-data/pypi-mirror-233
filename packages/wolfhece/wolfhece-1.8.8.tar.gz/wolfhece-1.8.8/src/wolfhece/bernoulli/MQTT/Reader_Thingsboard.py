from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from time import sleep
import random
import paho.mqtt.client as paho
import json
import logging
telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
broker="iot4h2o.mv.uni-kl.de"
topic = "v1/devices/me/telemetry"
token = "guCnZNPPCPP6oA9NeE2Q"
port=1883
client = TBDeviceMqttClient(broker, token)
# Connect to ThingsBoard
def callback(client, result):
    print(client, result)

logging.basicConfig(level=logging.DEBUG)
client.connect()
# Sending telemetry without checking the delivery status
#client.send_telemetry(telemetry) 
# Sending telemetry and checking the delivery status (QoS = 1 by default)
Value1=str(random.randint(0, 10))
Value2=str(random.randint(0, 10))
attributes = {"Temperature": Value1, "Humidity": Value2}
#sub_id_2 = client.subscribe_to_all_attributes(callback)
client.send_attributes(attributes)
sleep(2)
Value1=str(random.randint(0, 10))
Value2=str(random.randint(0, 10))
attributes = {"Temperature": Value1, "Humidity": Value2}
client.send_attributes(attributes)
Value1=str(random.randint(0, 10))
Value2=str(random.randint(0, 10))
sleep(2)
attributes = {"Temperature": Value1, "Humidity": Value2}
client.send_attributes(attributes)

# Disconnect from ThingsBoard
client.disconnect()
test=1