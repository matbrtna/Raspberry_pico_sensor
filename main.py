"""
Main Flask Application Module

This is the entry point for the Raspberry Pi Pico temperature sensor web application.
It initializes the Flask server, configures the database, sets up user authentication
(login, register, logout), and defines the core HTTP routes.

The application serves as a central hub that receives temperature data from either
a serial (UART) connection or an MQTT broker, stores it in a SQLite database,
and displays it on a web dashboard with charts and tables.
"""

from flask import *
import json
from flask_session import Session
from api_routes import api
import os
from flask_sqlalchemy import *
import hashlib
from models import db, User, Data
from datetime import datetime
from time import sleep
import requests
import serial


# Initialize Flask application and configure server-side sessions
app = Flask(__name__)
app.secret_key = "trynewone123"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure SQLite database path using the current working directory
db_file=os.path.join(os.getcwd(), 'nsi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'


# Register the API blueprint that contains all REST API endpoints
app.register_blueprint(api)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Global state variables to track errors and the last data source used (MQTT or Serial)
error=None
last_read=None


def copy_config_data():
    """
    Resets the data.json file by copying contents from the config_data.json template.
    This is called at startup to initialize the data file with default values.
    """
    with open("config_data.json","r") as file:
        data= json.load(file)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)



def hash_password(password):
    """
    Hashes a plaintext password using SHA-256.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hexadecimal SHA-256 hash of the password.
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password



@app.route('/logout')
def logout():
    """Logs out the current user by removing their username from the session."""
    session.pop('username', None)
    return redirect('/')



@app.route('/')
def index():
    """
    Renders the homepage with the current user's info, last temperature reading,
    the last data source used (MQTT/Serial), and any error notifications.
    """
    return render_template('home.html', username=session.get('username'), last_temperature=last_temp,last_read=last_read,error=session.get('error'))

@app.route('/error')
def generate_error():
    """Sets the global error flag and redirects to the homepage to display an error notification."""
    global error
    error=True
    return redirect('/')

@app.route('/mqtt')
def mqtt_session():
    """
    Sets the last data source to MQTT, clears any errors,
    and redirects to the homepage.
    """
    global last_read,error
    error=None
    last_read="MQTT"
    return redirect('/')

@app.route('/serial')
def serial_session():
    """
    Sets the last data source to Serial, clears any errors,
    and redirects to the homepage.
    """
    global last_read, error
    error=None
    last_read="Serial"
    return redirect('/')


@app.route('/register', methods=['GET'])
def get_register():
    """Renders the user registration form."""
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():
    """
    Handles user registration. Validates form input (username length >= 4,
    password length >= 5, passwords match, unique email and username),
    creates a new User record in the database, and logs the user in.
    Returns an error message string if validation fails.
    """
    formUsername = request.form.get('username')
    formPassword = request.form.get('password')
    formPassword2 = request.form.get('password2')
    formEmail = request.form.get('email')
    if not formUsername or not formPassword or not formEmail:
        return "You did not fill all of the fields"
    if len(formUsername)<4:
        return "Username has to be at least 4 characters"
    if len(formPassword) < 5:
        return "Password has to be at least 5 characters"
    if  formPassword!=formPassword2:
        return "Password do not match" 

    if User.query.filter_by(email=formEmail).first() is not None:
        return "Email is taken"
    if User.query.filter_by(username=formUsername).first() is not None:
        return "Username is taken"

    user=User(formUsername,hash_password(formPassword),formEmail)
    db.session.add(user)
    db.session.commit()
    db.session.close()
    session['username']=formUsername
    return redirect('/')





@app.route('/login', methods=['GET'])
def get_login():
    """Renders the login form."""
    return render_template("login.html")



@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login. Verifies the username and hashed password against
    the database. On success, stores the username in the session and redirects
    to the homepage. Returns an error message if credentials are invalid.
    """
    formUsername = request.form.get('username')
    formPassword = request.form.get('password')
    if not formPassword or not formUsername:
        return "You did not fill all of the fields"
    user = User.query.filter_by(username=formUsername, password=hash_password(formPassword)).first()
    if user:
        session['username']=formUsername
        return redirect('/')
    else:
        return "Invalid username or password"
    

def read_values():
    """
    Continuously reads temperature values from the serial port (/dev/ttyACM0)
    connected to the Raspberry Pi Pico. Each reading is stored in the database.
    Stops if the serial connection fails.
    """
    print("Reading values")
    while True:
        try:
            ser = serial.Serial(
                port='/dev/ttyACM0',  # Přizpůsob sériový port
                baudrate=115200,
                # Rychlost komunikace (musí odpovídat nastavení na Raspberry Pi Pico)           # Timeout v sekundách pro čtení
            )

            data = ser.readline().decode()
            print(data)
            add_to_db(data)
            sleep(5)
        except:
            print("Unable to read")
            break


def add_to_db(temp):
    """
    Creates a new Data record with the given temperature value and current
    timestamp, then saves it to the database.

    Args:
        temp: The temperature value to store.
    """
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    data = Data(timestamp, temp)
    db.session.add(data)
    db.session.commit()
    db.session.close()
    last_temp = data['value']

# @app.route('/changed_temp/<S>')
# def change_temp(S):
#     last_temp=S
#     return redirect('/')



if __name__ == '__main__':
    copy_config_data()
    # with open("data.json", "r") as file:
    #     data=json.load(file)
    #     last_temp=data[-1]
   
    with app.app_context():
        db.create_all()
    #     for i in range(4):
    #         sleep
    #         # timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    #         timestamp=datetime.now()
    #         data=Data(timestamp,25.5)
    #         db.session.add(data)
    #         db.session.commit()
    #         db.session.close()

    last_temp=0
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    response=requests.get('http://localhost:5000/api/last_data_value')
    data = response.json()
    last_temp = data['value']
