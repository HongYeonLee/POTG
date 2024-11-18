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

# 로그인 화면
@application.route("/login")
def view_logIn():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        user_info = DB.get_user_info(id_, pw_hash)
        session['name'] = user_info['name']
        return redirect(url_for('hello'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

# 회원가입
@application.route("/signup")
def view_signUp():
    return render_template("signup.html")

@application.route("/signup_post", methods=["POST"])
def register_user():
    data=request.form
    pw=request.form['pw'] #비밀번호만 데이터에서 가져와 해쉬코드로 변경 후 저장
    pwConfirm = request.form['pwConfirm']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    pwConfirm_hash = hashlib.sha256(pwConfirm.encode('utf-8')).hexdigest()

    if DB.insert_user(data, pw_hash, pwConfirm_hash): #아이디 중복체크
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

# 상품 조회
@application.route("/view_product")
def view_list():
    return render_template("view_product.html")

#상품 리스트 수정한 부분
#등록순
@application.route("/view_registration")
def view_registration():
    return render_template("view_registration.html")

@application.route("/")
def list():
    return redirect(url_for('view_list'))

@application.route("/list")
def view_list():

    per_page = 10
    per_row = 5
    row_count = int(per_page/per_row)
    
    data = DB.get_items()
    tot_count = len(data)

    for i in range(row_count):
        if(i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row]) 

    return render_template(
        "view_registration.html",
        datas = data.items(),
        row1 = locals()['data_0'].items(),
        row2 = locals()['data_1'].items(),
        total = tot_count)

#동적라우팅
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("view_detail.html", name=name, data=data)

#여기까지 수정



# 리뷰 조회
@application.route("/review_ViewAll")
def view_review():
    per_page=12
    per_row=4
    row_count=int(per_page/per_row)
    
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

@application.route("/review_Vieweach.html")
def view_reviewEach():
    return render_template("review_Vieweach.html")

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
    image_file = request.files["fileUpload"]
    image_file.save("static/images/inputImages/{}".format(image_file.filename))
    data = request.form
    print(data['name'], data['seller'], data['address'], data['category'], data['method'], data['status'], data['phone'])
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("submit_item_result.html", data=data, img_path="static/images/inputImages/{}".format(image_file.filename))

<<<<<<< Updated upstream

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)
=======
>>>>>>> Stashed changes