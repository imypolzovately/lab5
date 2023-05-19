
import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__, template_folder='template')

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="maxic3434",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if records:
                return render_template('account.html', full_name=records[0][1], username = username, password = password)
            else:
                return render_template('no_user.html')
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute('SELECT login FROM service.users')
        list_logins = cursor.fetchall()
        logins = []
        for i in list_logins:
            logins.append(i[0])
        if name == '' and login == '' and password == '':
            error = "Inputs Cannot Be Blank"
            return render_template('registration.html', error = error)
        elif login in logins:
            error = 'Login Already in Use'
            return render_template('registration.html', error = error)
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
            conn.commit()

            return redirect('/login/')


    return render_template('registration.html')

app.run(debug=True)
