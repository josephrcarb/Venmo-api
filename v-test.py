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
    trans = dict() #{User_id: Paid, Recieved}
    def callback(transactions_list):
        for transaction in transactions_list:

            #Paying person is not activeUser
            if(transaction.actor.id != activeUser.id):
                 
                #Person is not currently in history
                if(transaction.actor.id not in trans):
                    trans[transaction.actor.id] = [0, transaction.amount]
                
                #Person is in history, update total
                else:
                    trans[transaction.actor.id][1] += transaction.amount

            #Recieving person is not activeUser
            elif(transaction.target.id != activeUser.id):

                #Person is not currently in history
                if(transaction.target.id not in trans):
                    trans[transaction.target.id] = [transaction.amount, 0]

                #Person is in history, update total
                else:
                    trans[transaction.target.id][0] += transaction.amount

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