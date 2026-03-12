"""
WiFi Connection Helper (MicroPython)

Provides a utility function to connect the Raspberry Pi Pico W to a WiFi network.
Used by the Pico's main program when operating in MQTT mode, which requires
network connectivity to publish temperature data to a remote broker.
"""

import network
from time import sleep

def connect(ssid, password):
    """
    Connects the Pico to a WiFi network in station (client) mode.
    Blocks until the connection is established, printing status updates
    each second while waiting. Once connected, prints the network
    configuration (IP address, subnet mask, gateway, DNS).

    Args:
        ssid (str): The WiFi network name to connect to.
        password (str): The WiFi network password.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())
