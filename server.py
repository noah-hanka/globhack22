from flask import Flask, render_template, redirect, url_for, request
import matplotlib.pyplot as plt
import csv
from csv import DictWriter
app = Flask(__name__)

# langing page


@app.route('/')
def landingPage():
    return render_template('landingpage.html')

# general user login routing


@app.route('/userlogin')
def userLogin():
    return render_template('userlogin.html')


@app.route('/form', methods=["POST"])
def form():
    email = request.form["email"]
    password = request.form["password"]
    with open('./db/userCredentials.csv') as credentials:
        reader = csv.reader(credentials, delimiter=',')
        for row in reader:
            if email == row[0]:
                if password == row[1]:
                    return render_template('form.html', email=email, password=password)
                else:
                    break
    return render_template('userlogin.html', invalidLogin=True)


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

    fields = ["email", "password", "street_address", "city", "state",
              "zipCode", "water", "food", "electricity", "shelter", "tp"]
    row_app = {"email": email, "password": password, "street_address": address, "city": city, "state": state,
               "zipCode": zipCode, "water": water, "food": food, "electricity": elec, "shelter": shelter, "tp": tp}

    with open('./db/formEntry.csv', 'r') as formR:
        lines = list()
        reader = csv.reader(formR, delimiter=",")
        rewrite = False
        for row in reader:
            if email != row[0]:
                lines.append(row)
            else:
                rewrite = True
    if rewrite:
        # update row
        with open('./db/formEntry.csv', 'w') as formW:
            # formW.write(','.join(fields)+'\n')
            writer = csv.writer(formW)
            writer.writerows(lines)
    with open('./db/formEntry.csv', 'a') as formW:
        writer = DictWriter(formW, fieldnames=fields)
        writer.writerow(row_app)
    return render_template('complete.html', email=email, password=password)


# administrator login routing
@app.route('/adminlogin')
def adminLogin():
    return render_template('adminlogin.html')


@app.route('/admin', methods=["POST"])
def admin():
    email = request.form["email"]
    password = request.form["password"]
    with open('./db/adminCredentials.csv') as credentials:
        reader = csv.reader(credentials, delimiter=',')
        for row in reader:
            if email == row[0] and password == row[1]:
                people = []
                fields = ["email", "password", "street_address", "city", "state",
                          "zipCode", "water", "food", "electricity", "shelter", "tp"]
                with open('./db/formEntry.csv') as peopleFile:
                    reader = csv.reader(peopleFile, delimiter=',')
                    for row in reader:
                        newDic = {fields[i]: row[i]
                                  for i in range(len(fields))}
                        people.append(newDic)
                n = len(people)
                myCounts = getCounts(people)
                makeGraph(myCounts)
                return render_template('admin.html', email=email, password=password, people=people, count=n)
    return render_template('adminlogin.html', invalidLogin=True)

def sortPeople(people):
    pass


# creating account routing
@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html')


@app.route('/makeAccount', methods=["POST"])
def makeAccount():
    email = request.form["email"]
    pw = request.form["password"]
    bd = request.form['birthdate']
    licno = request.form['license_number']
    ssn = request.form['social_security_number']

    fields = ['email', 'password', 'birthdate', 'lic_no', 'ssn']
    # row to append to csv
    row_app = {'email': email, 'password': pw,
               'birthdate': bd, 'lic_no': licno, 'ssn': ssn}

    with open('./db/userCredentials.csv', 'r+') as cred:
        csv_reader = csv.reader(cred, delimiter=",")
        csv_writer = DictWriter(cred, fieldnames=fields)
        for row in csv_reader:
            if email == row[0]:
                # redirect to invalid login
                return render_template("createAccount.html", invalidLogin=True)
        csv_writer.writerow(row_app)
        return render_template("form.html", email=email, password=pw)


def getCounts(somePeople):
    counts = [0, 0, 0, 0, 0]
    for person in somePeople:
        if person['water'] == 'yes':
            counts[0] += 1
        if person['food'] == 'yes':
            counts[1] += 1
        if person['electricity'] == 'yes':
            counts[2] += 1
        if person['tp'] == 'yes':
            counts[3] += 1
        if person['shelter'] == 'yes':
            counts[4] += 1

    return counts


def makeGraph(actualCount):

    topics = ['Water', 'Food', 'Electricity', 'Toiletries', 'Shelter']
    x_pos = [i for i, _ in enumerate(topics)]

    plt.bar(x_pos, actualCount, color='blue')
    plt.xlabel("Citizen Needs")
    plt.ylabel("Total Citizens in Need")
    plt.title("What Our Citizens Need")
    plt.xticks(x_pos, topics)

    plt.savefig("./static/output.jpg")
