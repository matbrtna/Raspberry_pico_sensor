"""
Serial Port Reader Module

Reads temperature data from the Raspberry Pi Pico via a USB serial (UART) connection
on /dev/ttyACM0 at 115200 baud. Each temperature value read from the serial port
is forwarded to the Flask web server's API endpoint for storage in the database.

If no data is received for 3 consecutive read attempts, an error notification
is sent to the server. This script should be run as a separate process alongside
the Flask web server.
"""

import serial
import sys
import time
import datetime
# from models import db, Data
import sqlite3
import json
import requests

# Direct database connection (used by the commented-out add_to_db function)
conn = sqlite3.connect('nsi.db')
cursor = conn.cursor()


def read_values():
    """
    Continuously reads temperature values from the serial port every 5 seconds.
    Each successful reading is sent as JSON to the Flask API endpoint
    /api/send_data_from_serial. Tracks consecutive empty reads and triggers
    an error notification after 3 failed attempts.
    """
    no_input = 0
    requests.get('http://localhost:5000/error')
    while True:
        # try:
        time.sleep(5)
        ser = serial.Serial(
            port='/dev/ttyACM0',  # Serial port for the Raspberry Pi Pico
            baudrate=115200,
        )

        data = ser.readline().decode()
        if data:
            print("Read from serial: " + data)

            # add_to_db(data)
            try:
                data = {"temp": data}
                url = 'http://localhost:5000/api/send_data_from_serial'
                headers = {'Content-Type': 'application/json'}
                requests.get(url, data=json.dumps(data), headers=headers)
                print("Sent requset")
                no_input = 0


            except Exception as e:
                print(e)
        else:
            no_input += 1
            if no_input > 3:
                requests.post('http://localhost:5000/api/data_recieved')



    # except:
    #     print("Unable to read")
    #     break


# def add_to_db(data):
#     try:
#         timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
#         cursor.execute("SELECT id,temp FROM data ORDER BY id DESC LIMIT 1")
#         row = cursor.fetchone()
#         id, temp = row
#         new_id = id + 1
#
#         cursor.execute("INSERT INTO data  VALUES (?,?,?)", (new_id, timestamp, data))
#         conn.commit()
#         print("Added to database")
#
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
#         conn.close()


read_values()
