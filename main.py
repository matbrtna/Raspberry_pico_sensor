from flask import *
import json
from flask_session import Session
from api_routes import api

app = Flask(__name__)
app.secret_key = "mykey123"
app.register_blueprint(api)


# users = [{
#     "username": "admin", "password": "admin", "mail": "mail@example.com"
# }]


def add_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

def load_users():
    with open("users.json", "r") as file:
        return json.load(file)
    

def copy_config_data():
    with open("config_data.json","r") as file:
        data= json.load(file)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')



@app.route('/')
def index():  
    return render_template('home.html', username=session.get('username'), last_temperature=last_temp)





@app.route('/register', methods=['GET'])
def get_register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():
    users = load_users()
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')
    if not username or not password or not email or password != password2:
        return "You did not fill all of the fields"
    else:
        for user in users:
            if user['username'] == username:
                return "Username is already in use"
            if len(username)<4:
                return "Username has to be at least 4 characters"
            if user['mail'] == email:
                return "Email is already in use"
            if len(password) < 5:
                return "Password has to be at least 5 characters"
            if password != password2:
                return "Passwords do not match"
    users.append({"username": username, "password": password, "mail": email})
    add_users(users)
    session['username']=username
    return redirect('/')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    with open("users.json", "r") as file:
        users = json.load(file)
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return "You did not fill all of the fields"
    for user in users:
        if user["username"] == username and user["password"] == password:
            session['username']=username
            return redirect('/')
    return "Invalid username or password"

@app.route('/changed_temp/<S>')
def change_temp(S):
    last_temp=S
    return redirect('/')

if __name__ == '__main__':
    copy_config_data()
    with open("data.json", "r") as file:
        data=json.load(file)
        last_temp=data[-1]
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
