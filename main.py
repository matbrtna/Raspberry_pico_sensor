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

app = Flask(__name__)
app.secret_key = "mykey123"


db_file=os.path.join(os.getcwd(), 'nsi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'



app.register_blueprint(api)


db.init_app(app)




def copy_config_data():
    with open("config_data.json","r") as file:
        data= json.load(file)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)



def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password



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
    return render_template("login.html")



@app.route('/login', methods=['POST'])
def login():
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
