# Raspberry Pi Pico Temperature Sensor

An IoT temperature monitoring system that collects temperature data from a Raspberry Pi Pico and displays it on a web dashboard with real-time charts and tables.

## Architecture

```
Raspberry Pi Pico          Host Computer                  Web Browser
+-----------------+        +------------------------+     +----------------+
| MicroPython     |  UART  | serial_read.py         |     |                |
| Generate temp   |------->| or                     |     | Dashboard      |
| readings        |  MQTT  | subscriber_read.py     |     | - Line chart   |
+-----------------+        +----------+-------------+     | - Data table   |
                                      | HTTP POST         | - Controls     |
                                      v                   +-------+--------+
                           +----------+-------------+             |
                           | Flask Web Server        |  HTTP GET   |
                           | (main.py + api_routes)  |<------------+
                           +----------+-------------+
                                      |
                                      v
                           +----------+-------------+
                           | SQLite Database (nsi.db)|
                           | - Temperature records   |
                           | - User accounts         |
                           +------------------------+
```

## Project Structure

```
.
├── main.py                  # Flask web server entry point
├── api_routes.py            # REST API endpoints (Blueprint)
├── models.py                # SQLAlchemy database models (Data, User)
├── mqqt_read.py             # Legacy MQTT reader (Adafruit IO, unused)
├── publisher_test.py        # Test script to publish MQTT messages
├── pico/                    # Raspberry Pi Pico firmware (MicroPython)
│   ├── main.py              # Pico main program (UART or MQTT mode)
│   ├── connection.py        # WiFi connection helper
│   └── simple.py            # MQTT client library (umqtt.simple)
├── data_reading/            # Host-side data collection scripts
│   ├── serial_read.py       # Reads temperature from USB serial port
│   └── subscriber_read.py   # Reads temperature from MQTT broker
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Base layout (Bootstrap 5 + Chart.js)
│   ├── home.html            # Homepage with dashboard
│   ├── dashboard.html       # Chart, table, and controls
│   ├── navbar.html          # Navigation bar
│   ├── login.html           # Login form
│   └── register.html        # Registration form
└── static/
    ├── graf.js              # Dashboard JavaScript (chart + table logic)
    └── style.css            # Custom styles
```

## Requirements

### Host Computer (Server)

- Python 3
- Flask
- Flask-Session
- Flask-SQLAlchemy
- pyserial (for serial/UART mode)
- paho-mqtt (for MQTT mode)

### Raspberry Pi Pico

- MicroPython firmware
- Raspberry Pi Pico or Pico W (Pico W required for MQTT/WiFi mode)

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Flash the Pico

Copy the files from the `pico/` directory onto the Raspberry Pi Pico running MicroPython:
- `main.py`
- `connection.py`
- `simple.py`

By default, the Pico runs in **serial (UART) mode**, sending temperature data over USB at 115200 baud.

### 3. Start the Flask Server

```bash
python main.py
```

The server starts on `http://0.0.0.0:5000`.

### 4. Start a Data Reader

Choose one depending on your communication method:

**Serial (UART) mode** - connect the Pico via USB, then:
```bash
python data_reading/serial_read.py
```

**MQTT mode** - requires an MQTT broker (e.g., Mosquitto) running on localhost:
```bash
python data_reading/subscriber_read.py
```

## Usage

1. Open `http://localhost:5000` in a browser.
2. Register an account or log in.
3. The dashboard displays:
   - The most recent temperature reading and timestamp
   - A line chart of temperature over time
   - A table of recent temperature records
4. Use the slider to adjust how many data points are shown (2-30).
5. Use the "Add random value" button to insert test data.
6. Use the delete form to remove the oldest records.

## API Endpoints

| Method | Endpoint                     | Description                                  |
|--------|------------------------------|----------------------------------------------|
| GET    | `/api/last_data_value`       | Returns the most recent temperature record   |
| GET    | `/api/data?count=N`          | Returns the last N temperature records       |
| POST   | `/api/data`                  | Adds a random temperature record             |
| POST   | `/api/send_data_from_mqtt`   | Receives temperature data from MQTT reader   |
| POST   | `/api/send_data_from_serial` | Receives temperature data from serial reader |
| POST   | `/api/delete_data`           | Deletes the oldest N records                 |

## Data Flow

1. The **Raspberry Pi Pico** generates temperature readings (simulated, 22-26 C) every 10 seconds.
2. Data is transmitted via **UART** (USB serial) or **MQTT** to the host computer.
3. The **data reader script** (`serial_read.py` or `subscriber_read.py`) forwards the data to the Flask API via HTTP POST.
4. The **Flask server** stores the data in a **SQLite database**.
5. The **web dashboard** fetches data from the API and renders it using **Chart.js**.

## Testing Without Hardware

You can test the MQTT pipeline without a physical Pico:

1. Install and start an MQTT broker (e.g., Mosquitto) on localhost.
2. Start the Flask server: `python main.py`
3. Start the MQTT subscriber: `python data_reading/subscriber_read.py`
4. Publish a test message: `python publisher_test.py`
