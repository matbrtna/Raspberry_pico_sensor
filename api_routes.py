from flask import  *
from datetime import datetime
import random



api = Blueprint('hello_api', __name__)






def read_file(name):
    with open(name+".json", "r") as file:
        return json.load(file)
    

def write_file(name,data):
    with open(name+".json", "w") as file:
        json.dump(data, file, indent=4)

        
    

@api.route('/api/last_data_value',methods=['GET'])
def get_last_data():
    data=list(read_file("data"))
    return jsonify(data[-1])





@api.route('/api/data', methods=['GET'])
def get_data():
    data=read_file("data")
    data_count = int(request.args.get('count', 10))
    return jsonify(data[-data_count::])


@api.route('/api/data', methods=['POST'])
def add_data():
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    temp=random.uniform(25.3, 26.3)
    formatted_temp = f"{temp:.1f}"
    data=list(read_file("data"))
    data.append({"timestamp": timestamp, "temp": formatted_temp})
    write_file("data",data)
    return redirect('/')
    # return redirect('/changed_temp',S=data[-1])
    # return redirect(url_for('changed_temp', S=data[-1]))





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
    data=list(read_file("data"))

    if rows<len(data):
        # for i in range(rows):
        #     data.pop()
      
        del data[:rows]
        write_file("data",data)
        # return render_template("home.html",temperatures=data[::-1])
        return redirect("/")
    else:
        return "There will be no data left"
