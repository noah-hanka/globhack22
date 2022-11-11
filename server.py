from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def loginPage():
    return render_template('./static/login.html')
@app.route('/makeAccount',methods=["POST"])
def makeAccount():
    user = request.form["username"]
    pw = request.form["pw"]


    return render_template("./static/form.html")
@app.route('/form',methods=["POST"]):
def formPage():
    user = request.form["username"]
    pw = request.form["pw"]