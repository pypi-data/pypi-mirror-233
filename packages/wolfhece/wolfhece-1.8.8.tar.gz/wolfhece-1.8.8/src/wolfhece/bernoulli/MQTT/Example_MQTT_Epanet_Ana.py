#For this code we interact with 2 devices in thingsboard. The first device has the name "TestDevice_StartEpanet". In the Dashboard, it is connected to the RPC-button "Start_Epanet". We must subscribe to RPC of this device for getting informaiton about it, e.g. if the button was pushed.
#The second device has the name "TestDevice_MQTT_Epanet", it is the virtual preassure measuring device that is shown in the maps. This device should receive the calculated preassure from Epanet, i.e. we have to publish massages containing the preassure value for this device.

import paho.mqtt.client as mqtt
import json

#information needed to subscribe to a device in thingsboard
token = "dNlU6Jt0Kjbe1n3B8EnD"                       # token of the device that sould be subscribed (in our case "TestDevice_StartEpanet")
token = "z003FlJLj68wJUHie5LA"
broker="iot4h2o.mv.uni-kl.de"                        # host name
port=1883                                            # port
topic = "v1/devices/me/response"                     # topic
value=1


# crate mqtt client
client = mqtt.Client()
client2 = mqtt.Client()

# create function for subscribing
def on_connect(client, userdata, flags, rc) :
    if (rc==0) :
        print("connected OK Returned code = ", rc)                  # mesaage if successfully connected to device
        client.subscribe('v1/devices/me/telemetry/+')
        client.subscribe('v1/devices/me/rpc/request/+')             # subscribe to RPC commands
       
    else :
        print("Bad connection Returned code = ", rc)                # message if device could not be connected

# create function for message reception
def on_message(client, userdata, msg) :
    global value
    global client2
    data = json.loads(msg.payload)                                                                          # messages from Thingsboard are in json format and need to be unpacked
    parameter = json.loads(data["params"])
    if str(parameter) == "True":                                                                            # if RPC-button "Start Epanet" is pushed, the parameter of the received json file is true
        #os.system("runepanet Rede_LENHS_original.inp Rede_LENHS_original.rpt")                              # starts Epanet from the command line, an initial and report file of Epanet are needed
        
        #value = [float(str(s))for s in linecache.getline("Rede_LENHS_original.rpt", 3599).split()][3]       # get the preassure value of a device form the updated report file
        value = value+1

        clientDevice = mqtt.Client()                                                                              # create a new mqqt client
        clientDevice.username_pw_set('z003FlJLj68wJUHie5LA')                                                      # select token (in our case from "TestDevice_MQTT_Epanet")
        clientDevice.loop_start()                                                                                 # start client loop
        clientDevice.connect(broker)                                                                              # connect to broker, its the same host as for the subscribed device
        Ret=clientDevice.publish('v1/devices/me/telemetry', json.dumps({"preassure_Epanet": value}),2)                # send telemetry to device (in our case to "Test_Device_MQTT_Epanet")
        client2.loop(1)
        value=value+1

client.username_pw_set(token)         # set token of device ("TestDevice_StartEpanet")
client.connect(broker , port, 60)     # connect to device ("TestDevice_StartEpanet")
client.on_connect = on_connect        # subscribe to device ("TestDevice_StartEpanet")
client.on_message = on_message        # recive massage ("TestDevice_StartEpanet")

client2.username_pw_set('z003FlJLj68wJUHie5LA')         # set token of device ("TestDevice_StartEpanet")
client2.loop_start()
client2.connect(broker)     # connect to device ("TestDevice_StartEpanet")
#client2.on_connect = on_connect        # subscribe to device ("TestDevice_StartEpanet")
client2.on_message = on_message        # recive massage ("TestDevice_StartEpanet")
client2.subscribe('v1/devices/me/telemetry/request/+')

client.loop_forever()                 # start client loop

client.loop_stop()                    # stop client loop
client.disconnect()                   # diconnect client

        