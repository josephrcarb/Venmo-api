from venmo_api import Client, ApiClient
from auth_api import AuthenticationApi

import json
import sys

class Venmo_Data():
    secret = None
    api = AuthenticationApi(ApiClient())
    user = None
    userApi = None
    venmo = None
    trans = dict()
    loggedIn = False
    data_trans = dict()
    aCode = None

    #Login into the Venmo Api
    def login(self, name, passw):
        self.secret = self.api.login_using_credentials(name, passw)
    
    def logout(self):
        self.loggedIn = False
        self.api.log_out(self.aCode)
        self.secret = None
        self.user = None
        self.userApi = None
        self.venmo = None
        self.trans = dict()
        self.api = AuthenticationApi(ApiClient())
        self.data_trans = dict()
        self.aCode = None

    def getAccessToken(self, code):
        self.aCode = self.api.codeRecieved(code, self.secret)
        self.venmo = Client(access_token=self.aCode)
        self.userApi=self.venmo.user
        self.user = self.venmo.user.get_my_profile()
        self.loggedIn = True
        self.getTransactions()

    def getuserProfile(self, uid):
        u = self.userApi.get_user(uid)
        return [u.username, u.profile_picture_url]

#Print out all the transactions from user thats logged in
    def getTransactions(self): 
        def callback(transactions_list):
            for transaction in transactions_list:
                #Paying person is not activeUser
                if(transaction.actor.id != self.user.id):
                    
                    #Person is not currently in history
                    if(transaction.actor.id not in self.trans):
                        self.trans[transaction.actor.id] = [0, transaction.amount]
                    
                    #Person is in history, update total
                    else:
                        self.trans[transaction.actor.id][1] += transaction.amount

                #Recieving person is not activeUser
                elif(transaction.target.id != self.user.id):

                    #Person is not currently in history
                    if(transaction.target.id not in self.trans):
                        self.trans[transaction.target.id] = [transaction.amount, 0]

                    #Person is in history, update total
                    else:
                        self.trans[transaction.target.id][0] += transaction.amount    
            self.data_trans = self.trans   
        self.venmo.user.get_user_transactions(user_id=self.user.id, callback=callback)
    
    def getTrans(self):
        return self.data_trans

    def isTrans(self):
        if(len(self.data_trans) != 0 ):
            return True
        return False

    def isApi(self):
        if(self.api is not None):
            return True
        return False


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