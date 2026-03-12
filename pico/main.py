import time
import random
from connection import connect
from umqtt.simple import MQTTClient
import ujson
from machine import UART, Pin
import sys

ssid = "13373-IoT-Lab"
pwd = "asgasgasg"
server = "mqtt.eclipseprojects.io"
topic = "/nsi/brtnamat/temp"
# client = MQTTClient(client_id="Ras_pico_brntamat", server=server, port=1883)


mqtt_host = b"asgasg.s1.eu.hivemq.cloud"
host = b"asgasgasg.s1.eu.hivemq.cloud"

mqt2t_host = "io.adafruit.com"
mqtt_pwd = b"asfaf"
mqtt2_pwd = "asfasgasgas"
mqtt_topic = "brtnamat/feeds/nsi"
mqtt_username = "brtnamat"


# client = MQTTClient(b"raspi_brtnamat", host, 0,mqtt_username,mqtt_pwd,keepalive=7200,ssl=True)

# topic = "/nsi/brtnamat/"
# ser = serial.Serial('/dev/ttyACM0', 9600)


# client=MQTTClient("raspi_brtnamat", server=mqtt_host,port=0, user=mqtt_username,password=mqtt_pwd,keepalive=7200,ssl=True,ssl_params={'server_hostname':"1df2d5701f3a44a4ae268315f751c165.s1.eu.hivemq.cloud"})

def send_value(value):
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
    value = str(value)
    print(value)


def send_mqtt(num):
    current_timestamp = time.time()
    MESSAGE = ujson.dumps({"temp": num})
    client.publish(topic, MESSAGE)


def connect_mqtt():
    try:
        client.connect()
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")


def serial_loop():
    while True:
        number = round(random.uniform(22, 26), 1)
        send_value(number)
        time.sleep(10)


def mqtt_loop():
    connect("Ema2021", "mnbvcmnbvc")
    connect_mqtt()
    while True:
        number = round(random.uniform(22, 26), 1)
        send_mqtt(number)
        time.sleep(10)


if __name__ == "__main__":
    serial_loop()
    # mqtt_loop()

