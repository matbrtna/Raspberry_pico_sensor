"""
MQTT Subscriber Reader Module

Subscribes to the local MQTT broker (localhost:1883) and listens for temperature
data on the "nsi/brtnamat" topic. When a message is received, the JSON payload
is parsed and forwarded to the Flask web server's API endpoint for database storage.

This script should be run as a separate process alongside the Flask web server
and an MQTT broker (e.g., Mosquitto). The Raspberry Pi Pico (or the publisher_test.py
script) publishes temperature data to the same MQTT topic.
"""

import paho.mqtt.client as mqtt
import json
import requests

def on_connect(client, userdata, flags, rc):
    """
    Callback triggered when the client connects to the MQTT broker.
    Subscribes to the "nsi/brtnamat" topic upon successful connection.
    """
    print(f"Connected with result code {rc}")
    client.subscribe("nsi/brtnamat")

def on_message(client, userdata, msg):
    """
    Callback triggered when a message is received on a subscribed topic.
    Parses the JSON payload and forwards the temperature data to the
    Flask API endpoint /api/send_data_from_mqtt.
    """
    print(f"Received {msg.payload}")
    try:
        data = json.loads(msg.payload.decode())
        url = 'http://localhost:5000/api/send_data_from_mqtt'
        headers = {'Content-Type': 'application/json'}
        requests.get(url, data=json.dumps(data),headers=headers)
    except Exception as e:
        print(e)


# Initialize the MQTT client and set callback functions
client = mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

# Connect to the local MQTT broker and start listening indefinitely
client.connect("localhost",1883,60)
print("listening")
try:
    client.loop_forever()
except:
    print("loop forever ended")