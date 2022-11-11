from flask import Flask, render_template, redirect, url_for, request
import csv
app = Flask(__name__)

@app.route('/')
def loginPage():
    return render_template('./static/login.html')
@app.route('/makeAccount',methods=["POST"])
def makeAccount():
    email = request.form["email"]
    password = request.form["password"]


    return render_template("./static/form.html")
@app.route('/form',methods=["POST"])
def formPage():
    email = request.form["email"]
    password = request.form["password"]
    with open('userCredentials.csv') as credentials:
        reader = csv.reader(credentials,delimiter=',')
        for row in reader:
            if email == row[0]:
                if password == row[1]:
                    return render_template('./static/form.html',email = email, password = password)
                else:
                    break
        return render_template('/static/login.html',invalidLogin = True)