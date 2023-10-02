# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *

#insert the following information
username = "t.pirard@uliege.be"
password = "111122"
DeviceToken = "jnWbsYRMF5sEaMwLUqXM"
url = 'http://iot4h2o.mv.uni-kl.de:8080/api/auth/login'
url = 'http://iot4h2o.mv.uni-kl.de:8080'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

#Partie télémétrie en vue d'ajouter et de recevoir des informations de télémétrie
"""
logging.basicConfig(level=logging.DEBUG)
telemetry_with_ts = {"ts": int(round(time() * 1000)), "values": {"temperature": 42.1, "humidity": 70}}
attributes = {"sensorModel": "DHT-22", "attribute_2": "value"}
client = TBDeviceMqttClient(url, DeviceToken)
client.connect()
Test=1
client.stop()
"""

# Python 3 implementation of the approach
 
# Array to store the numbers used
# to form the required sum
dp = [0 for i in range(200)]
count = 0
 
# Function to print the array which contains
# the unique partitions which are used
# to form the required sum
def print1(idx):
    for i in range(1,idx,1):
        print(dp[i],end = " ")
    print("\n",end = "")
 
# Function to find all the unique partitions
# remSum = remaining sum to form
# maxVal is the maximum number that
# can be used to make the partition
def solve(remSum,maxVal,idx,count):
    # If remSum == 0 that means the sum
    # is achieved so print the array
    if (remSum == 0):
        print1(idx)
        count += 1
        return
    # i will begin from maxVal which is the
    # maximum value which can be used to form the sum
    i = maxVal
    while(i >= 1):
        if (i > remSum):
            i -= 1
            continue
        elif (i <= remSum):
            # Store the number used in forming
            # sum gradually in the array
            dp[idx] = i
 
            # Since i used the rest of partition
            # cant have any number greater than i
            # hence second parameter is i
            solve(remSum - i, i, idx + 1, count)
            i -= 1
 
# Driver code

n = 7
count = 0
 
solve(n, n, 1, count)
Test=1     
# This code is contributed by
# Surendra_Gangwar

