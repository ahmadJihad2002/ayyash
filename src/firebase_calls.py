import firebase_admin
from firebase_admin import credentials, db
import os
from utills import root_path

class Firebase():

    def __init__(self):
        # setting up the firebase
        print(os.getcwd())
        cred = credentials.Certificate(root_path + "Data/ayyash-admin-credentials.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://ayyash-933b4-default-rtdb.firebaseio.com/'
        })
        # Get a reference to the database service
        self.ref = db.reference('ayyash/board/states')
        self.configRef = db.reference('ayyash/config')

    def set_value(self, relay_number, state):
        self.ref.update({
            relay_number: state
        })
        print('Data set successfully.')
        #
        # pass

    def fetch_remote_config(self):
        data = self.configRef.get()
        print("date fetched successfully")
        print(data)
        return data
