from flask import Flask, render_template, redirect, url_for, request
import csv
from csv import DictWriter
from tempfile import NamedTemporaryFile
import shutil
app = Flask(__name__)

# langing page
@app.route('/')
def landingPage():
    return render_template('landingpage.html')

# general user login routing
@app.route('/userlogin')
def userLogin():
    return render_template('userlogin.html')
@app.route('/form',methods=["POST"])
def form():
    email = request.form["email"]
    password = request.form["password"]
    with open('./db/userCredentials.csv') as credentials:
        reader = csv.reader(credentials,delimiter=',')
        for row in reader:
            if email == row[0]:
                if password == row[1]:
                    return render_template('form.html',email = email, password = password)
                else:
                    break
    return render_template('userlogin.html',invalidLogin = True)
@app.route('/submitForm', methods=["POST"])
def submitForm():
    
    email = request.form["email"]
    password = request.form["password"]
    address = request.form["address"]
    city = request.form["city"]
    state = request.form["state"]
    zipCode = request.form["zipcode"]
    water = request.form["group1"]
    food = request.form["group2"]
    elec = request.form["group3"]
    shelter = request.form["group4"]
    tp = request.form["group5"]

    fields = ["email", "password", "street_address", "city", "state", "zipCode", "water", "food", "electricity", "shelter", "tp"]
    row_app = {"email":email, "password":password, "street_address":address, "city":city, "state":state, "zipCode":zipCode, "water":water, "food":food, "electricity":elec, "shelter":shelter, "tp":tp}

    with open('./db/formEntry.csv', 'r') as formR:
        lines = list()
        reader = csv.reader(formR, delimiter=",")
        writer = DictWriter(formR, fieldnames=fields)
        rewrite = False
        for row in reader:
            if email != row[0]:
                lines.append(row)
            else:
                rewrite = True
    if rewrite:
        # update row
        with open('./db/formEntry.csv', 'w') as formW:
            writer.writerows(lines)
    writer.writerow(row_app)
                    
    

# administrator login routing
@app.route('/adminlogin')
def adminLogin():
    return render_template('adminlogin.html')

@app.route('/admin',methods=["POST"])
def admin():
    email = request.form["email"]
    password = request.form["password"]
    with open('./db/adminCredentials.csv') as credentials:
        reader = csv.reader(credentials,delimiter=',')
        for row in reader:
            if email == row[0] and password == row[1]:
                people = []
                with open('formEntry.csv') as peopleFile:
                    reader = csv.reader(credentials,delimiter=',')
                    for row in reader:
                        people.append(row)
                n = len(people)
                return render_template('admin.html',email = email, password = password, people = people, count = n)
    return render_template('adminlogin.html',invalidLogin = True)


# creating account routing
@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html')
@app.route('/makeAccount',methods=["POST"])
def makeAccount():
    email = request.form["email"]
    pw = request.form["password"]
    bd = request.form['birthdate']
    licno = request.form['license_number']
    ssn = request.form['social_security_number']

    fields = ['email', 'password', 'birthdate', 'lic_no', 'ssn']
    # row to append to csv
    row_app = {'email':email, 'password':pw, 'birthdate':bd, 'lic_no':licno, 'ssn':ssn} 

    with open('./db/userCredentials.csv', 'r+') as cred:
        csv_reader = csv.reader(cred, delimiter=",")
        csv_writer = DictWriter(cred, fieldnames=fields)
        for row in csv_reader:
            if email == row[0]:
                # redirect to invalid login
                return render_template("createAccount.html",invalidLogin=True)
        csv_writer.writerow(row_app)
        return render_template("form.html",email=email,password=pw)

