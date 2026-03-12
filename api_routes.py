from flask import  *
from datetime import datetime
import random
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Data



api = Blueprint('api', __name__)



        

@api.route('/api/last_data_value',methods=['GET'])
def get_last_data():
    last_data=db.session.query(Data).order_by(Data.id.desc()).limit(1).all()
    last_data=last_data[0]
    return_data=[{'timestamp': last_data.timestamp, 'temp': last_data.temp}]
    return jsonify(return_data[0])




@api.route('/api/data', methods=['GET'])
def get_data():
    engine = create_engine('sqlite:///nsi.db') 
    Session = sessionmaker(bind=engine)
    session = Session()
    data_count = int(request.args.get('count', 10))
    last_records = session.query(Data).order_by(Data.id.desc()).limit(data_count).all()
    session.close()
    last_records=last_records[::-1]
    data_list = [{'temp': record.temp, 'timestamp': record.timestamp} for record in last_records]
    return jsonify(data_list)

 

@api.route('/api/data', methods=['POST'])
def add_data():
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    # timestamp = datetime.now()
    temp=random.uniform(21.3, 26.5)
    formatted_temp = f"{temp:.1f}"
    data=Data(timestamp,formatted_temp)
    db.session.add(data)
    db.session.commit()
    db.session.close()
    return redirect('/')

@api.route('/api/no_data_recieved', methods=['POST',"GET"])
def get_error():
    return redirect('/error')





@api.route('/api/send_data_from_mqtt',methods=['GET','POST'])
def write_mqtt_data():
    request_data = request.json
    temp = request_data.get('temp')
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    data = Data(timestamp, temp)
    db.session.add(data)
    db.session.commit()
    db.session.close()
    session['last_read']="MQTT"
    return redirect('/mqtt')


@api.route('/api/send_data_from_serial',methods=['GET','POST'])
def write_serial_data():
    request_data = request.json
    temp = request_data.get('temp')
    # session.pop("error",None)
    #session['error']=False
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    data = Data(timestamp, temp)
    db.session.add(data)
    db.session.commit()
    db.session.close()
    session['last_read'] = "UART"
    return redirect('/serial')

# @api.route('/api/users', methods=['GET'])
# def get_users():
#     users=read_file("users")
#     return jsonify(users)
    

# @api.route('/api/users', methods=['POST'])
# def add_users(username,password,email):
#     users=list(read_file("users"))
#     users.append({"username": username, "password": password, "mail": email})
#     write_file("users",users)
#     return redirect('/')







# @api.route('/api/users', methods=['DELETE'])
# def delete_users():
#     pass


@api.route('/api/delete_data', methods=['POST'])
def delete_data():
    rows = int(request.form.get('numRows'))
    data=db.session.query(Data).all()
    if rows<len(data):
        oldest_records = Data.query.order_by(Data.id).limit(rows).all()
        for record in oldest_records:
            db.session.delete(record)
        db.session.commit()
        return redirect("/")
    else:
        return "There will be no data left"
