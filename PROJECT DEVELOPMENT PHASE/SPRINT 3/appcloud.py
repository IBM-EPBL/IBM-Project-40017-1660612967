from flask import Flask, render_template, request, redirect, flash
import pickle
import pandas as pd
import joblib
import numpy as np
import sqlite3
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "G0-fTz5hk2xE6cxkk-PyyzQmio8NNqeMG_wTLTgCSqmU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,
                                                                                 "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
app.secret_key="21433253"
conn = sqlite3.connect("database1.db")
conn.execute("CREATE TABLE IF NOT EXISTS login(email TEXT PRIMARY KEY,password TEXT)")
conn.close()

@app.route('/')
def main():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            print("request1")
            fv = [x for x in request.form.values()]
            print(fv)
            print([x for x in request.form.values()])
            print(request.form["email"])
            email = request.form["email"]
            pswd = request.form["pswd"]
            print("request2")
            conn = sqlite3.connect("database1.db")
            cur = conn.cursor()
            print(email, pswd)
            cur.execute("SELECT password FROM login WHERE email=?;", (str(email),))
            print("select")

            result = cur.fetchone()
            cur.execute("SELECT * FROM login")
            print(cur.fetchall())
            print("fetch")
            if result:
                print("You've have been logged in")
                print(result)
                if result[0] == pswd:
                    flash("Login successfully", 'success')
                    return redirect('/home')
                else:
                    return render_template("login.html", error="Please enter correct password")

            else:
                print("register")
                flash("Please Register first to access", 'danger')

                return redirect('/reg')

        except Exception as e:
            print(e)
            print('danger-----------------------------------------------------------------')
            return "hello error"


@app.route('/reg')
def reg():
    return render_template("register.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            print("request1")
            fv = [x for x in request.form.values()]
            print(fv)
            print([x for x in request.form.values()])
            print(request.form["email"])
            email = request.form["email"]
            print(request.form["pswd"])
            pswd = request.form["pswd"]
            conn = sqlite3.connect("database1.db")
            print("database")
            cur = conn.cursor()
            print("cursor")
            cur.execute("SELECT * FROM login WHERE email=?;", (str(email),))
            print("fetch")
            result = cur.fetchone()
            if result:
                print("already")
                flash("User already exists,please login", 'danger')
                return redirect('/')
            else:
                print("insert")
                cur.execute("INSERT INTO  login(email,password)values(?,?)", (str(email), str(pswd)))
                conn.commit()
                cur.execute("SELECT * FROM login")
                print(cur.fetchall())
                flash("Registered successfully", 'success')
                return render_template('login.html')

        except Exception as e:
            print(e)
            # flash(e,'danger')
            return "hello error1"

            # return redirect('/')
# return render_template('login.html')


@app.route('/home')
def home():
    return render_template('Flightdelay.html')

@app.route('/result', methods=['POST'])
def predict():
    fl_num = int(request.form.get('fno'))
    month = int(request.form.get('month'))
    dayofmonth = int(request.form.get('daym'))
    dayofweek = int(request.form.get('dayw'))
    sdeptime = request.form.get('sdt')
    adeptime = request.form.get('adt')
    arrtime = int(request.form.get('sat'))
    depdelay = int(adeptime) - int(sdeptime)
    inputs = list()
    inputs.append(fl_num)
    inputs.append(month)
    inputs.append(dayofmonth)
    inputs.append(dayofweek)
    if (depdelay < 15):
        inputs.append(0)
    else:
        inputs.append(1)
    inputs.append(arrtime)
    origin = str(request.form.get("org"))
    dest = str(request.form.get("dest"))
    if (origin == "ATL"):
        a = [1, 0, 0, 0, 0]
        inputs.extend(a)
    elif (origin == "DTW"):
        a = [0, 1, 0, 0, 0]
        inputs.extend(a)
    elif (origin == "JFK"):
        a = [0, 0, 1, 0, 0]
        inputs.extend(a)
    elif (origin == "MSP"):
        a = [0, 0, 0, 1, 0]
        inputs.extend(a)
    elif (origin == "SEA"):
        a = [0, 0, 0, 0, 1]
        inputs.extend(a)

    if (dest == "ATL"):
        b = [1, 0, 0, 0, 0]
        inputs.extend(b)
    elif (dest == "DTW"):
        b = [0, 1, 0, 0, 0]
        inputs.extend(b)
    elif (dest == "JFK"):
        b = [0, 0, 1, 0, 0]
        inputs.extend(b)
    elif (dest == "MSP"):
        b = [0, 0, 0, 1, 0]
        inputs.extend(b)
    elif (dest == "SEA"):
        b = [0, 0, 0, 0, 1]
        inputs.extend(b)

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [
        ['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15']],
                                       "values": [inputs]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9d1fb3ed-8689-426b-aedc-bc2e35bedd81/predictions?version=2022-11-19',json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(response_scoring.json())

    predict = predictions['predictions'][0]['values'][0][0]

    return render_template('/result.html', prediction=predict)


if __name__ == '__main__':
    app.run(debug=True)
