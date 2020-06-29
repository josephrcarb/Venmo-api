from flask import Flask, render_template, redirect, url_for, request, session
from v_test import login as loginApi, getTransactions
from venmo_api.models.exception import HttpCodeError
import sys
from auth_api import AuthenticationApi
app=Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': 
        try:
            session['var'] = loginApi(request.form['username'], request.form['password'])
        except HttpCodeError as e:
            print(e.msg)
            return redirect(url_for('error'))
        return redirect(url_for('access'))
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    new_arr = session.get('var', None)
    getTransactions(new_arr[1], new_arr[0].id)
    return 'Hello World!'

@app.route('/error', methods=['GET', 'POST'])
def error():
    
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('error.html')

@app.route('/access', methods=['GET','POST'])
def access():
    error = None
    new_arr = session.get('var', None)
    print(new_arr[2].otpCode)
    print(new_arr[2].needCode)
    if request.method == 'POST':
        while True:
            try: 
                new_arr[2].changeCode(False, request.form['password'])
                return redirect(url_for('home'))
            except:
                return redirect(url_for('error'))
    return render_template('access.html', error=error)


if __name__=="__main__":
    
    app.run(debug=True)