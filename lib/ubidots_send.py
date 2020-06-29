import urequests as requests
import machine
import time

TOKEN = "YOUR TOKEN HERE" #Put here your TOKEN
DELAY = 1  # Delay in seconds

# Builds the json to send the request
def build_json(sens_name, value):
    try:
        data = {sens_name: {"value": value}}
        return data
    except:
        return None

# Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
def post_var(device, sens_name, value):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json(sens_name, value)
        if data is not None:
            #print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            print('Data is None')
    except:
        print("Unable to send data to Ubidots")
