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
            "birthDay" : data['birthDay'],
            "address" : data['address']
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
    
    def get_user_info_byId(self, id_):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id'] == id_:
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
        per_price=int(data['price'])/int(data['cnt'])

        #quantity 기본값
        initial_quantity = int(data.get('quantity', 0)) 
        

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
        "d_day":d_day_display,
        "per_price":per_price,
        "quantity": initial_quantity,
        "updated_cnt": data['cnt']
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
    
    # 거래 내역 db에 있는 값 가져오기
    def get_history_items(self, user_id):
        history_items = self.db.child("buy&exchange").child(user_id).get().val()
        if not history_items:
            return {}  # 장바구니가 비어있는 경우 빈 딕셔너리 반환
        return history_items  # 사용자 장바구니 데이터를 반환
    
    def get_item_byname_in_history(self, name, user_id):
        items = self.db.child("buy&exchange").child(user_id).get()
        target_value=""

        print("###########",name)

        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
            
        return target_value
    #공동구매 수량 등록
    def update_quantity(self,data):
        #현재 데이터 가져오기
        current_item = self.db.child("gr_item").child(data['name']).get().val()
        # 남은 수량 계산
        new_quantity = int(data['quantity'])
        current_quantity = int(current_item.get('quantity', 0))
        remain_cnt = int(current_item['cnt']) - new_quantity
        if remain_cnt < 0:
            raise ValueError("Insufficient stock.")
        
        # 업데이트할 데이터 병합
        updated_item = {
            "updated_cnt": remain_cnt,
            "quantity": current_quantity+new_quantity
        }
        current_item.update(updated_item)
        self.db.child("gr_item").child(data['name']).set(current_item)

        return True

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
    
    # 좋아요 누르기
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
    
    # 좋아요 누른 상품 지우기
    def remove_heart_item(self, name, user_id):
        item = self.db.child("heart").child(user_id).child(name).get()
        if(item):
            self.db.child("heart").child(user_id).child(name).remove()
            return True
        else:
            print("해당 아이템이 없습니다")
            return False
    
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
    
    # 장바구니 상품 구매&교환 기록 등록
    def reg_buy_all_in_cart(self, user_id):
        cart_items = self.db.child("cart").child(user_id).get()
        
        if not cart_items.val():
            print("장바구니가 비어 있습니다.")
            return False

        for item in cart_items.each():
            item_name = item.key()  # 아이템 이름 가져오기
            item_data = item.val()  # 아이템 데이터 가져오기
            
            # 구매 데이터 등록
            self.reg_buy(user_id, item_data, item_name)
            
            # 장바구니에서 아이템 제거
            self.remove_cart_item(item_name, user_id)

            # 상품등록에서 아이템 제거
            self.remove_item(item_name, user_id)

            # 좋아요에서 아이템 제거
            self.remove_heart_item(item_name, user_id)

        return True
    
    # 장바구니 아이템 등록
    def reg_cart(self, user_id, data, name):
        cart_info = {
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
        self.db.child("cart").child(user_id).child(name).set(cart_info)
        return True
    
    # 장바구니 db에 있는 값 가져오기
    def get_cart_items(self, user_id):
        cart_items = self.db.child("cart").child(user_id).get().val()
        if not cart_items:
            return {}  # 장바구니가 비어있는 경우 빈 딕셔너리 반환
        return cart_items  # 사용자 장바구니 데이터를 반환
    
    # 장바구니 아이템 지우기
    def remove_cart_item(self, name, user_id):
        item = self.db.child("cart").child(user_id).child(name).get()
        if(item):
            self.db.child("cart").child(user_id).child(name).remove()
            return True
        else:
            print("해당 아이템이 없습니다")
            return False
    
    # 장바구니 아이템 모두 지우기
    def remove_cart_item_All(self, user_id):
        items = self.db.child("cart").child(user_id).get()
        if items.val():  # 장바구니가 비어 있지 않은 경우
            for item in items.each():
                self.db.child("cart").child(user_id).child(item.key()).remove()
            return True
        else:
            print("해당 아이템이 없습니다")
            return False

    # 상품 등록에서 아이템 지우기
    def remove_item(self, name, user_id):
        item = self.db.child("item").child(name).get()
        if(item):
            self.db.child("item").child(name).remove()
            self.db.child("heart").child(user_id).child(name).remove()
            return True
        else:
            print("해당 아이템이 없습니다")
            return False