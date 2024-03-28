from flask import *
import json
from flask_session import Session

app = Flask(__name__)
app.secret_key = "mykey123"


data = [
    {"timestamp": "1.1.2024 12:00", "temp": 25.1},
    {"timestamp": "1.1.2024 12:05", "temp": 24.2},
    {"timestamp": "1.1.2024 12:10", "temp": 23.6},
    {"timestamp": "1.1.2024 12:15", "temp": 25.0},
    {"timestamp": "1.1.2024 12:20", "temp": 25.2},
    {"timestamp": "1.1.2024 12:25", "temp": 25.5},
    {"timestamp": "1.1.2024 12:30", "temp": 25.8},
    {"timestamp": "1.1.2024 12:35", "temp": 26.1},
    {"timestamp": "1.1.2024 12:40", "temp": 26.2},
    {"timestamp": "1.1.2024 12:45", "temp": 25.5},
    {"timestamp": "1.1.2024 12:50", "temp": 25.3},
    {"timestamp": "1.1.2024 12:55", "temp": 25.2},
    {"timestamp": "1.1.2024 13:00", "temp": 24.9},
]

# users = [{
#     "username": "admin", "password": "admin", "mail": "mail@example.com"
# }]


def add_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

def load_users():
    with open("users.json", "r") as file:
        return json.load(file)


@app.route('/delete', methods=['POST'])
def delete_data():
    rows = int(request.form.get('numRows'))
    if rows<len(data):
        for i in range(rows):
            data.pop()
        # return render_template("home.html",temperatures=data[::-1])
        return redirect("/")
    else:
        return "There will be no data left"


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')



@app.route('/data')
def get_data():
    data_count = int(request.args.get('count', 10))

    return jsonify(data[-data_count::])


@app.route('/')
def index():  # return render_template('home.html')
    # return redirect(url_for("success"))
    return render_template('home.html', username=session.get('username'), temperatures=data[::-1])





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

@app.route('/success')
def success():
    return render_template("home.html", username=session.get('username'), temperatures=data[::-1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
