from flask import Flask, render_template, redirect, url_for, request, session
from v_test import login as loginApi, getTransactions, getAccessToken
from venmo_api.models.exception import HttpCodeError
import sys
from auth_api import AuthenticationApi
app=Flask(__name__)

class DataStore():
    secret = None
    api = None
    user = None
    venmo = None
    trans = None

data = DataStore()

@app.route('/', methods = ['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('home.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': 
        if(request.form["submit_login"] == "login"):
            try:
                data.api, data.secret = loginApi(request.form['username'], request.form['password'])
                return redirect(url_for('access'))
            except HttpCodeError as e:
                print(e.msg)
                return redirect(url_for('error'))
        elif(request.form["submit_login"] == "home"):
            return redirect(url_for('home'))
        else:
            pass
    return render_template('login.html', error=error)

@app.route('/transactions')
def transactions():
    if(data.venmo is not None):
        data.trans = getTransactions(data.venmo, data.user.id)
        print(data.trans)
    return 'Hello World!'

@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('error.html')

@app.route('/access', methods=['GET','POST'])
def access():
    error = None
    if request.method == 'POST':
        if(request.form["access_login"]=="login"):
            try:
                if(data.api is not None):
                    data.user, data.venmo = getAccessToken(data.api, request.form['password'], data.secret)
                    return redirect(url_for('transactions'))
            except HttpCodeError as e:
                print(e.msg)
                return redirect(url_for('error'))
        elif(request.form["access_login"]=="back"):
            return redirect(url_for('login'))
        else:
            pass
    return render_template('access.html', error=error)


if __name__=="__main__":
    
    app.run(debug=True)