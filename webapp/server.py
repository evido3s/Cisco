#!/usr/bin/env python3
from subprocess import PIPE, Popen
from flask import Flask
from flask import request, render_template, redirect, url_for
#import re
import paramiko
#from flask_sqlalchemy import SQLAlchemy
from models import db, User, Command, Device

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
#db = SQLAlchemy(app)


@app.route('/')
def index():
	return render_template("index.html")

@app.route('/new')
def new():
	return render_template('new.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
       return redirect('/')
    if request.method == 'POST':
        adminuser = User.query.filter_by(username='admin').first()
        username = request.form['username']
        password = request.form['password']
        #if username == 'admin' and password == 'admin123':
        if username == adminuser.username and password == adminuser.password:
             return redirect(url_for('main'))
        else:
            return render_template('authfail.html')

@app.route('/main')
def main():
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]
    desc=[]
    name=[]
    command = []
    commands = []
    commands_query = Command.query.all()
    for i in commands_query: command.append(i.command)
    for i in commands_query: name.append(i.name)
    for i in commands_query: desc.append(i.desc)
    w =[j for i in zip(command,name,desc) for j in i]
    for i in list(chunks(w, 3)): commands.append(i)

    name,desc,ip,devices = [],[],[],[]
    dev_query = Device.query.all()
    for i in dev_query: ip.append(i.ip)
    for i in dev_query: name.append(i.name)
    for i in dev_query: desc.append(i.desc)
    x =[j for i in zip(ip,name,desc) for j in i]
    for i in list(chunks(x, 3)): devices.append(i)
    
    return render_template('main.html', commands = commands, devices=devices)

@app.route('/addnewdevice')
def addnewdevice():
    return render_template('addnewdevice.html')

@app.route('/addnewcommand')
def addnewcommand():
    return render_template('addnewcommand.html')

@app.route('/ciscoconnect', methods=['GET', 'POST'])
def ciscoconnect1():
    data = request.get_data()
    print(data)
    data = str(data)
    index = data.index("customcommand")
    if len(data[index:]) < 16:
         data = data[0:-len(data[index:])-1]
    print(data, type(data))
    #ip_addresses = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', data)
    data = data.strip('b').split('&')
    devices_and_commands = []
    for i in data:
         devices_and_commands.append(i.split('=')[1])
    result = devices_and_commands
    print(result)
    devices= devices_and_commands[:len(devices_and_commands)-1]
    print(devices)
    devices = str(devices)
    devices = devices.strip(']').lstrip('[').strip("'")
    print(devices)
    print('###################################################################')
    command= devices_and_commands[len(devices_and_commands)-1]
    command = command.rstrip("'").replace('+', ' ')
    print(devices_and_commands, "", "Command: ", command, "Devices: ", devices)
    #p = subprocess.Popen(['/Cisco/netapp/connector.py', devices, command], stdout=subprocess.PIPE )
    command = command.replace("%7C","|").replace("%2F", "/")
    print(devices, "------")
    print(command, "------")
    p = Popen(['/Cisco/netapp/connector.py', devices, command], stdout=PIPE )
    out, err = p.communicate()
    out = str(out)
    out = out.lstrip('b').strip()
    print(out)
    data = []
    for i in out.split('\\n'):
        i = i.replace(' ', "&nbsp;")
        data.append(i)
    print('----------------------------------')
    for i in out.split('\\n'):
        print(i)
    return render_template("cisco_output.html", output=data)
	

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
