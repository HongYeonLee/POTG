import pyrebase
import json
    
class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def insert_user(self, data, pw, pwConfirm):
        user_info ={
            "id": data['id'],
            "pw": pw,
            "pwConfirm": pwConfirm,
            "name" : data['name'],
            "emailId" : data['emailId'],
            "mobileNumber" : data['mobileNumber'],
            "gender" : data['gender'],
            "birthYear" : data['birthYear'],
            "birthMonth" : data['birthMonth'],
            "birthDay" : data['birthDay']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
    
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False

    def get_user_info(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return value

    
    def insert_item(self, name, data, img_path):
        item_info ={
        "seller": data['seller'],
        "category": data['category'],
        "method": data['method'],
        "status": data['status'],
        "price": data['price'],
        "date": data['date'],
        "info": data['info'],
        "address": data['address'],
        "phone": data['phone'],
        "purchase": data['purchase'],
        "details": data['details'],
        "img_path": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    

#상품 리스트 화면
#여기부터 수정#
    def get_items(self):
        items = self.db.child("item").get().val()

        if items is None:
            return{}
        
        items = {}

        for key, value in items.items():
            items[key] = {
                "info": key,
                "price": value['price'],
                "method": value['method'],
                "img_path": value['img_path']
            }
        return items #item 노드 값 가져오기
    
    # "info": data['info'],
    #"price": data['price'],
    #"method": data['method'],
    #"img_path": img_path

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""

        print("###########",name)

        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()

                item_info = {
                    "name": key_value,
                    "price": target_value['price'],
                    "method": target_value['method'],
                    "img_path": target_value['img_path'],
                    "seller": target_value['seller'],
                    "category": target_value['category'],
                    "status": target_value['status'],
                    "address": target_value['address'],
                    "phone": target_value['phone'],
                    "purchase": target_value['purchase'],
                    "details": target_value['details'],
                }
                return item_info
            
        return target_value