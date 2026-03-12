"""
MQTT Publisher Test Script

A simple test utility that publishes a single random temperature value to the
local MQTT broker. Used for testing the MQTT data pipeline without a physical
Raspberry Pi Pico device.

The script generates a random temperature between 23 and 26 degrees Celsius
and publishes it as JSON to the "nsi/brtnamat" topic on localhost:1883.
"""

import paho.mqtt.publish as publish
import json
import time
import random

# MQTT broker connection settings
mqqt_broker_address = 'localhost'
mqqt_channel="nsi/brtnamat"

# Generate a random temperature value and format it as JSON
timern=time.time()
number = round(random.uniform(23, 26), 1)
# message=json.dumps({"timestamp":timern,"temp":number})
message=json.dumps({"temp":number})

# Publish the temperature reading to the MQTT broker
publish.single(mqqt_channel,message,hostname=mqqt_broker_address)


