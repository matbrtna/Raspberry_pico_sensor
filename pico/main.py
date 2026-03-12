"""
Raspberry Pi Pico Main Firmware (MicroPython)

This is the main program that runs on the Raspberry Pi Pico microcontroller.
It generates simulated temperature readings (22-26 C) and transmits them to the
host computer using one of two communication methods:

1. Serial (UART) mode: Sends temperature values over UART (GPIO 0/1) at 115200 baud.
   The host computer reads these via the serial_read.py script.
2. MQTT mode: Connects to WiFi and publishes temperature data to an MQTT broker.
   The host computer receives these via the subscriber_read.py script.

Currently configured to run in serial (UART) mode.
"""

import time
import random
from connection import connect
from umqtt.simple import MQTTClient
import ujson
from machine import UART, Pin
import sys

# WiFi and MQTT broker configuration
ssid = "13373-IoT-Lab"
pwd = "asgasgasg"
server = "mqtt.eclipseprojects.io"
topic = "/nsi/brtnamat/temp"
# client = MQTTClient(client_id="Ras_pico_brntamat", server=server, port=1883)

# HiveMQ Cloud broker settings (alternative MQTT broker)
mqtt_host = b"asgasg.s1.eu.hivemq.cloud"
host = b"asgasgasg.s1.eu.hivemq.cloud"

# Adafruit IO broker settings (another alternative)
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
    """
    Sends a temperature value over UART (serial) to the host computer.
    Uses UART0 on GPIO pins 0 (TX) and 1 (RX) at 115200 baud.

    Args:
        value: The temperature value to send.
    """
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
    value = str(value)
    print(value)


def send_mqtt(num):
    """
    Publishes a temperature value to the MQTT broker as a JSON message.

    Args:
        num: The temperature value to publish.
    """
    current_timestamp = time.time()
    MESSAGE = ujson.dumps({"temp": num})
    client.publish(topic, MESSAGE)


def connect_mqtt():
    """Attempts to connect to the configured MQTT broker. Prints an error on failure."""
    try:
        client.connect()
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")


def serial_loop():
    """
    Main loop for serial (UART) mode. Generates a random temperature value
    between 22 and 26 degrees Celsius every 10 seconds and sends it over UART.
    """
    while True:
        number = round(random.uniform(22, 26), 1)
        send_value(number)
        time.sleep(10)


def mqtt_loop():
    """
    Main loop for MQTT mode. Connects to WiFi and the MQTT broker, then
    generates and publishes a random temperature value every 10 seconds.
    """
    connect("Ema2021", "mnbvcmnbvc")
    connect_mqtt()
    while True:
        number = round(random.uniform(22, 26), 1)
        send_mqtt(number)
        time.sleep(10)


if __name__ == "__main__":
    serial_loop()
    # mqtt_loop()

