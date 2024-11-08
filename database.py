import pyrebase
import json
class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
            
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()