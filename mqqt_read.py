import paho.mqtt.client as mqtt
from Adafruit_IO import Client,Feed
import time

# # Funkce při připojení k brokeru
# def on_connect(client, userdata, flags, rc):
#     print(f"Connected with result code {rc}")
#     client.subscribe("brtnamat/feeds/nsi")
#
# # Funkce při přijetí zprávy
# def on_message(client, userdata, msg):
#     print(f"{msg.topic} {msg.payload}")
#
# username="brntamat"
# password="aio_dqcz617mIbLCEH0Ekxcy8oxn1bMb"
#
# client = mqtt.Client()
# client.username_pw_set(username=username, password=password)
# client.on_connect = on_connect
# client.on_message = on_message
#
# client.connect("io.adafruit.com")
#
# client.loop_start()
#
#
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Odpojení od brokeru")
#     client.loop_stop()
#     client.disconnect()