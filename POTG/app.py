from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
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
def view_product():
    page = request.args.get("page", 0, type = int)
    per_page = 10
    per_row = 5
    row_count = int(per_page/per_row)

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if(i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row]) 

    return render_template(
        "view_product.html",
        datas = data.items(),
        row1 = locals()['data_0'].items(),
        row2 = locals()['data_1'].items(),
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total = item_counts)

#동적라우팅
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("view_detail.html", name=name, data=data)

# 리뷰 등록 화면
@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    data = DB.get_item_byname(str(name))
    return render_template("review_write2.html", name=name, id=session['id'], data=data)

# 리뷰 db에 등록
@application.route("/reg_review", methods=['POST'])
def reg_review():
    data=request.form
    print(data['star'])
    item = DB.get_item_byname(data['name'])
    itemImgPath = item['img_path']
    image_file=request.files["file"]
    image_file.save("static/images/inputImages/{}".format(image_file.filename))
    DB.reg_review(data, image_file.filename, session, itemImgPath)
    return redirect(url_for('view_review'))

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

@application.route("/review_Vieweach")
def view_reviewEach():
    return render_template("review_Vieweach.html")

# 공동구매 전체 조회
@application.route("/grpurchase_ViewAll")
def grpPurchase():
    return render_template("grpurchase_ViewAll.html")

# 공동구매 상품 등록 페이지
@application.route("/view_grReg")
def view_grReg():
    return render_template("grpurchase_reg.html",user_id=session['id'])

# 공동구매 상품 업로드
@application.route("/submit_gr_post", methods=["POST"])
def gr_reg_item_submit_post():
    image_file = request.files['fileUpload']
    image_file.save("static/images/inputImages/{}".format(image_file.filename))
    data = request.form
    DB.insert_gr(data['name'], data, image_file.filename, session)
    return render_template("grpurchase_ViewAll.html", data=data, img_path="static/images/inputImages/{}".format(image_file.filename))

# 공동구매 상세페이지
@application.route("/grpurchaseDetail")
def grpurchase_Detail():
    return render_template("grpurchaseDetail.html")

# 리뷰 불러오기
@application.route("/review_ViewAll")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page=8 # item count to display per page
    per_row=4# item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_reviews() #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count -1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    
    return render_template(
        "review_ViewAll.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

#동적라우팅
@application.route("/review_Vieweach/<name>/")
def review_detail(name):
    print("###name:",name)
    data = DB.get_review_byname(str(name))
    print("####data:",data)
    return render_template("review_Vieweach.html", name=name, data=data)

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

@application.route("/cart", methods=["POST"])
def reg_item_submit_post():
    image_file = request.files["fileUpload"]
    image_file.save("static/images/inputImages/{}".format(image_file.filename))
    data = request.form
    print(data['name'], data['seller'], data['address'], data['category'], data['method'], data['status'], data['phone'])
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("cart.html", data=data, img_path="static/images/inputImages/{}".format(image_file.filename))

# 구매&교환 기능
@application.route("/buyExchange/<name>/")
def reg_buyExchange(name):
    data = DB.get_item_byname(name)
    DB.update_item(name, session['id'])
    DB.reg_buy(session['id'], data, name)
    return render_template("submit_item_result.html", data=data) 

# 장바구니
@application.route("/cart")
def view_cart():
    return render_template("cart.html")

# 좋아요 기능
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'], name)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    itemInfo = DB.get_item_byname(name)
    my_heart = DB.update_heart(session['id'], 'Y', itemInfo, name)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    itemInfo = DB.get_item_byname(name)
    my_heart = DB.update_heart(session['id'],'N',itemInfo, name)
    return jsonify({'msg': '안좋아요 완료!'})

# 좋아요 모아보기
@application.route("/heart")
def view_heart():
    page = request.args.get("page", 0, type = int)
    per_page = 12
    per_row = 4
    row_count = int(per_page/per_row)

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_heart_all(session['id'])
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if(i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row]) 

    return render_template(
        "heart.html",
        datas = data.items(),
        row1 = locals()['data_0'].items(),
        row2 = locals()['data_1'].items(),
        row3 = locals()['data_2'].items(),
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total = item_counts)


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)