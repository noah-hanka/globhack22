from flask import Flask, render_template, redirect, url_for, request
import csv
from csv import DictWriter
app = Flask(__name__)


@app.route('/makeAccount',methods=["POST"])
def makeAccount():
    email = request.form["email"]
    password = request.form["password"]


    return render_template("form.html")

@app.route('/form',methods=["POST"])
def form():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)
    with open('userCredentials.csv') as credentials:
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
    return render_template('./static/login.html')
@app.route('/makeAccount',methods=["POST"])
def makeAccount():
    user = request.form["username"]
    pw = request.form["pw"]

    fields = ['email', 'user']
    row_app = {'email':user, 'password':pw} # row to append to csv

    with open('globhack2022/db/userCredentials.csv', 'a') as cred:
        csv_reader = csv.reader(cred, delimiter=",")
        for row in csv_reader:
            if user in row[0]:
                pass # redirect to invalid login
            else:
                csv_writer = DictWriter(cred, fieldnames=fields)
                csv_writer.writerow(row_app)
    cred.close()


    return render_template("./static/form.html")
@app.route('/form',methods=["POST"]):
def formPage():
    user = request.form["username"]
    pw = request.form["pw"]
