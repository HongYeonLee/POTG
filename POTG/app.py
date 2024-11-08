from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

# 홈
@application.route("/")
def hello():
    return render_template("home.html")

# 로그인
@application.route("/login")
def view_logIn():
    return render_template("login.html")

# 회원가입
@application.route("/signup")
def view_signUp():
    return render_template("signup.html")

@application.route("/signup_post", methods=["POST"])
def register_user():
    data=request.form
    pw=request.form['pw'] #비밀번호만 데이터에서 가져와 해쉬코드로 변경 후 저장
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

def insert_user(self, data, pw):
    user_info ={
        "id": data['id'],
        "pw": pw,
        "name": data['name']
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

# 상품 조회
@application.route("/view_product")
def view_list():
    return render_template("view_product.html")

# 리뷰 조회
@application.route("/review_ViewAll")
def view_review():
    return render_template("review_ViewAll.html")

# 상품 등록
@application.route("/registerItem")
def reg_item():
    return render_template("registerItem.html")


@application.route("/review_write1")
def reg_review1():
    return render_template("review_write1.html")

# 리뷰 작성2
@application.route("/review_write2")
def reg_review2():
    return render_template("review_write2.html")

@application.route("/grpurchase_ViewAll")
def grpPurchase():
    return render_template("grpurchase_ViewAll.html")

@application.route("/submit_item")
def reg_item_submit():
    name = request.args.get("name")
    seller = request.args.get("seller")
    addr = request.args.get("addr")
    email = request.args.get("email")
    category = request.args.get("category")
    card = request.args.get("card")
    status = request.args.get("status")
    phone = request.args.get("phone")
    print(name, seller, addr, email, category, card, status, phone)
    # return render_template("reg_item.html")


@application.route("/submit_item_post", methods=["POST"])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    print(data['name'], data['seller'], data['addr'], data['email'], data['category'], data['card'], data['status'], data['phone'])
    # return render_template("submit_item_result.html", data=data,  img_path="static/images/{}".format(image_file.filename))
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("submit_item_result.html", data=data, img_path="static/images/{}".format(image_file.filename))


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)
