import paho.mqtt.client as mqtt
import json
import requests

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("nsi/brtnamat")

def on_message(client, userdata, msg):
    print(f"Received {msg.payload}")
    try:
        data = json.loads(msg.payload.decode())
        url = 'http://localhost:5000/api/send_data_from_mqtt'
        headers = {'Content-Type': 'application/json'}
        requests.get(url, data=json.dumps(data),headers=headers)
    except Exception as e:
        print(e)



client = mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

client.connect("localhost",1883,60)
print("listening")
try:
    client.loop_forever()
except:
    print("loop forever ended")