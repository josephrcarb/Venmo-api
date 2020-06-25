from venmo_api import Client
from venmo_api.utils.api_util import get_user_id
import json
import sys


#Login into the Venmo Api through command arguments
def login(name, passw):
    global venmo
    global activeUser
    access_token = Client.get_access_token(username=name, password=passw)
    venmo = Client(access_token=access_token)
    activeUser = venmo.user.get_my_profile()


#Print out all the transactions from user thats logged in
def getTransactions(userid):  
    def callback(transactions_list):
        for transaction in transactions_list:
            print(transaction.payment_id)
    venmo.user.get_user_transactions(user_id=userid, callback=callback)


def main():
    #Make sure valid arguments
    if(len(sys.argv) != 3):
        print("[Error] Invalid amount of arguments!\n")
        print("[Error] Use: 'v-test.py [email] [password]'\n")
        return None

    login(sys.argv[1], sys.argv[2])
    getTransactions(activeUser.id)


    return None

if __name__ == '__main__':
    main()