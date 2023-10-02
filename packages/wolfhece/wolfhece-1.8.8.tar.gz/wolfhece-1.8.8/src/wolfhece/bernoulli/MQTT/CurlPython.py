import requests
from datetime import datetime

#insert the following information
username = "t.pirard@uliege.be"
password = "111122"
DeviceToken = "nyosxGylFDO8JaTXOz1c"
DeviceToken = "guCnZNPPCPP6oA9NeE2Q"
DeviceToken = "698e65a0-21c0-11ec-a052-af580412d5c6"

#function for getting the token for the curl-command
def getCurlToken():
    url = 'http://iot4h2o.mv.uni-kl.de:8080/api/auth/login'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    loginJSON = {'username': username, 'password': password}
    tokenAuthResp = requests.post(url, headers=headers, json=loginJSON).json()
    token = tokenAuthResp['token']
    return token

#function for getting telemetry data
def GetTelemetryData(CurlToken):
    url = 'http://iot4h2o.mv.uni-kl.de:8080/api/plugins/telemetry/DEVICE/'+DeviceToken+'/values/timeseries'
    headers = {'Content-Type': 'application/json', 'X-Authorization': 'Bearer '+CurlToken}
    telemetryDataResp = requests.get(url, headers=headers).json()
    #telemetryDataResp = requests.get(url).json()
    return telemetryDataResp




#call funktion 
telemetryData=GetTelemetryData(getCurlToken())

#exampels for getting the values out of the json-message
print(telemetryData)

#store every key of the dictionary
keys = list(telemetryData.keys())
print("The first key is: " +  keys[0])

#print first key of the dictionary
data = telemetryData[str(keys[0])][0]

#get value and time stamp
print("The value is : " + data['value'])
time = int(data['ts'])
print("The timestamp is: " + str(datetime.fromtimestamp(time/1000)))



