from flask import Flask, render_template, redirect, url_for, request, session
from v_test import Venmo_Data
from venmo_api.models.exception import HttpCodeError
import sys
import time
from auth_api import AuthenticationApi

#Current Data Structure to save data when flipping through pages.
class CurrentData():
    table = []
    results = None

#Init
app=Flask(__name__, static_folder='static', static_url_path='/static')
data = Venmo_Data()
curr = CurrentData()

#Home Page
@app.route('/', methods = ['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('home.html', error=error)

#Login Page, sent user and pass to data structure, return to access page if successful
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': 
        if(request.form["submit_login"] == "login"):
            try:
                #TODO: LOG SOMEONE OUT WHEN RE LOGGING IN
                if(data.loggedIn is True):
                    data.logout() #Create new Data Struct
                    curr.results = None #Create new CurrentData Struct
                    curr.table = []

                data.login(name=request.form['username'], passw=request.form['password'])
                return redirect(url_for('access'))
            except HttpCodeError as e:
                print(e.msg)
                return redirect(url_for('error'))
        elif(request.form["submit_login"] == "home"):
            return redirect(url_for('home'))
        elif(request.form["submit_login"] == "transactions"):
            return redirect(url_for('transactions'))
        else:
            pass
    return render_template('login.html', error=error)

#Transactions page, rendered upon user authentication with access page
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    Table = []
    if request.method == 'POST':
            return redirect(url_for('login'))
    while(True):
        if(data.isTrans()):
            results = data.getTrans()
            curr.results = results
            for key, value in results.items():
                temp = []
                temp2 = data.getuserProfile(key)
                userN, picUrl = temp2[0], temp2[1]
                temp.extend([picUrl, userN, value[0], value[1]])
                Table.append(temp)
            curr.table = Table
            return render_template('transactions.html', table=curr.table)
        if(data.loggedIn == False):
            break
    return render_template('transactions.html', table=curr.table)


#Error Page, rendered upon any error in login process
@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('error.html')


#Access Page, get code from user input html file, send to data structure
@app.route('/access', methods=['GET','POST'])
def access():
    error = None
    if request.method == 'POST':
        if(request.form["access_login"]=="login"):
            try:
                if(data.isApi()):
                    data.getAccessToken(code=request.form['password'])
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