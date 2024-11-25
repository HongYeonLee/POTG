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
        "info": data['info'],
        "address": data['address'],
        "phone": data['phone'],
        "details": data['details'],
        "img_path": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
    # 공동구매 화면
    # 공동구매_상품등록
    def insert_gr(self, name, data, img_path, session):
        item_info ={
        "id": session['id'],
        "category": data['category'],
        "price": data['price'],
        "info": data['info'],
        "cnt":data['cnt'],
        "address": data['address'],
        "date":data['date'],
        "details": data['details'],
        "img_path": img_path
        }
        self.db.child("gr_item").child(name).set(item_info)
        print(data,img_path)
        return True

    #공동구매_상품가져오기
    def gr_get_items(self):
        items = self.db.child("gr_item").get().val()
        return items #gr_item노드 값 가져오기

    def gr_get_item_byname(self, name):
        items = self.db.child("gr_item").get()
        target_value=""

        print("###########",name)

        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
            
        return target_value

    
    #상품 리스트 화면
    #여기부터 수정#
    def get_items(self):
        items = self.db.child("item").get().val()
        return items #item 노드 값 가져오기

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""

        print("###########",name)

        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
            
        return target_value
    
    #리뷰 등록
    def reg_review(self, data, img_path, session, itemImgPath):
        review_info ={
        "title": data['title'],
        "rate": data['star'],
        "content": data['review-content'],
        "author": session['id'],
        "review_img": img_path, #리뷰 이미지
        "product_img": itemImgPath,
        "origin_price": data['price'],
        # "discount_price": data['discount_price'],
        }
        self.db.child("review").child(data['name']).set(review_info)
        return True

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews
    
    def get_review_byname(self, name):
        items = self.db.child("review").get()
        target_value=""

        print("###########",name)

        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
            
        return target_value
