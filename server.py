from flask import Flask, render_template, redirect, url_for, request
import csv
from csv import DictWriter
app = Flask(__name__)

@app.route('/form',methods=["POST"])
def form():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)
    with open('./db/userCredentials.csv') as credentials:
        reader = csv.reader(credentials,delimiter=',')
        for row in reader:
            if email == row[0]:
                if password == row[1]:
                    return render_template('form.html',email = email, password = password)
                else:
                    break
        return render_template('login.html',invalidLogin = True)

@app.route('/')
def loginPage():
    return render_template('userlogin.html')

@app.route('/makeAccount',methods=["POST"])
def makeAccount():
    user = request.form["username"]
    pw = request.form["pw"]

    fields = ['email', 'password']
    row_app = {'email':user, 'password':pw} # row to append to csv

    with open('./db/userCredentials.csv', 'a') as cred:
        csv_reader = csv.reader(cred, delimiter=",")
        for row in csv_reader:
            if user in row[0]:
                pass # redirect to invalid login
            else:
                csv_writer = DictWriter(cred, fieldnames=fields)
                csv_writer.writerow(row_app)
    return render_template("form.html")
