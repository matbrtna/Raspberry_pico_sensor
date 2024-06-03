import paho.mqtt.publish as publish
import json
import time
import random

mqqt_broker_address = 'localhost'
mqqt_channel="nsi/brtnamat"


timern=time.time()
number = round(random.uniform(23, 26), 1)
# message=json.dumps({"timestamp":timern,"temp":number})
message=json.dumps({"temp":number})


publish.single(mqqt_channel,message,hostname=mqqt_broker_address)


