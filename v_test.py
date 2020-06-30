from venmo_api import Client, ApiClient
from auth_api import AuthenticationApi

import json
import sys


#Login into the Venmo Api through command arguments

#TO-DO: Login does not work. Needs access token from from /access page,
#therefor function fails and return an error
def login(name, passw):
    api = AuthenticationApi(ApiClient())
    otp_secret = api.login_using_credentials(name, passw)

    return api, otp_secret
    
def getAccessToken(api, code, secret):
    access_token = api.codeRecieved(code, secret)
    venmo = Client(access_token=access_token)
    activeUser = venmo.user.get_my_profile()

    return activeUser, venmo

#Print out all the transactions from user thats logged in
def getTransactions(aUser, userid): 
    trans = dict() #{User_id: Paid, Recieved}
    def callback(transactions_list):
        for transaction in transactions_list:
            #Paying person is not activeUser
            if(transaction.actor.id != userid):
                 
                #Person is not currently in history
                if(transaction.actor.id not in trans):
                    trans[transaction.actor.id] = [0, transaction.amount]
                
                #Person is in history, update total
                else:
                    trans[transaction.actor.id][1] += transaction.amount

            #Recieving person is not activeUser
            elif(transaction.target.id != userid):

                #Person is not currently in history
                if(transaction.target.id not in trans):
                    trans[transaction.target.id] = [transaction.amount, 0]

                #Person is in history, update total
                else:
                    trans[transaction.target.id][0] += transaction.amount
        print(trans)
        return trans
    aUser.user.get_user_transactions(user_id=userid, callback=callback)
    return trans
    


def main():
    #Make sure valid arguments
    if(len(sys.argv) != 3):
        print("[Error] Invalid amount of arguments!\n")
        print("[Error] Use: 'v-test.py [email] [password]'\n")
        return None

    # activeUser, aUser, api = login(sys.argv[1], sys.argv[2])
    # getTransactions(aUser, activeUser.id)

    return None

if __name__ == '__main__':
    main()