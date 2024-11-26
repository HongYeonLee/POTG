import pyrebase
import json
from datetime import datetime
    
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
        current_date=datetime.now().date()
        # 입력된 날짜 (data['date'])를 날짜 객체로 변환
        try:
            target_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Expected 'YYYY-MM-DD'.")
            return False
        # D-Day 계산
        d_day = (target_date - current_date).days
        d_day_display = f"D-{d_day}" if d_day > 0 else "D-Day" if d_day == 0 else f"D+{-d_day}"
        
        #개당 개수

        item_info ={
        "id": session['id'],
        "category": data['category'],
        "price": data['price'],
        "info": data['info'],
        "cnt":data['cnt'],
        "address": data['address'],
        "date":data['date'],
        "details": data['details'],
        "img_path": img_path,
        "d_day":d_day_display 
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
    
    def get_heart_all(self, uid):
        Allhearts = self.db.child("heart").child(uid).get()
        target_value = {}

        if Allhearts.val() == None:
            return target_value
        
        for heart in Allhearts.each():
            data = heart.val() 
            if data['interested'] == 'Y':
                target_value[heart.key()] = data
        
        return target_value

    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()

        return target_value

    def update_heart(self, user_id, isHeart, itemInfo, name):
        heart_info ={
        "interested": isHeart,
        "img_path": itemInfo['img_path'],
        "price": itemInfo['price'],
        "method": itemInfo['method'],
        "seller": itemInfo['seller']
        }
        self.db.child("heart").child(user_id).child(name).set(heart_info)
        return True
    
    # 구매 & 교환 기록 등록
    def reg_buy(self, user_id, data, name):
        buy_info = {
            "seller": data['seller'],
            "category": data['category'],
            "method": data['method'],
            "status": data['status'],
            "price": data['price'],
            "info": data['info'],
            "address": data['address'],
            "phone": data['phone'],
            "details": data['details'],
            "img_path": data['img_path']
        }
        self.db.child("buy&exchange").child(user_id).child(name).set(buy_info)
        return True
    
    def update_item(self, name, user_id):
        item = self.db.child("item").child(name).get()
        if(item):
            self.db.child("item").child(name).remove()
            self.db.child("heart").child(user_id).child(name).remove()
            return True
        else:
            print("해당 아이템이 없습니다")
            return False