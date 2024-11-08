import pyrebase
import json
class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def insert_item(self, name, data, img_path):
        item_info ={
        "seller": data['seller'],
        "addr": data['addr'],
        "email": data['email'],
        "category": data['category'],
        "card": data['card'],
        "status": data['status'],
        "phone": data['phone'],
        "img_path": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True