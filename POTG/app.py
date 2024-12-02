from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys
import random

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

# 로그인 버튼 클릭
@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        user_info = DB.get_user_info(id_, pw_hash)
        session['name'] = user_info['name']
        session['address'] = user_info['address']
        return redirect(url_for('hello'))
    else:
        flash("아이디나 비밀번호가 잘못되었습니다")
        return render_template("login.html")

# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

# 회원가입 페이지
@application.route("/signup")
def view_signUp():
    return render_template("signup.html")

# 회원가입 버튼 클릭
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
        flash("동일한 아이디가 존재합니다")
        return redirect(url_for('view_signUp'))

# 상품 조회
@application.route("/view_product")
def view_product():
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all") #화면에서 셀렉트박스 선택한 카테고리 값 받아오기
    per_page = 10
    per_row = 5
    row_count = int(per_page / per_row)
        
    # 페이징 처리
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    # 상품 데이터 가져오기
    data = DB.get_items()
    item_counts = len(data)
    # 랜덤으로 5개 상품 선택
    popular_items = random.sample(list(data.items()), 5) if item_counts >= 5 else list(data.items())
    # 카테고리별로 db에서 데이터 받아오기
    if category!="all":
        data = DB.get_items_bycategory(category)
        item_counts = len(data)
    
    data = dict(sorted(data.items(), key = lambda x: x[0], reverse = False)) #상품 정렬
    paged_data = dict(list(data.items())[start_idx:end_idx])

    # 데이터 개수가 limit보다 크지 않은 경우 처리
    if item_counts<=per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(paged_data)
    # 행 별로 나누기
    rows = []
    for i in range(row_count):
        start = i * per_row
        end = (i + 1) * per_row
        if i == row_count - 1 and tot_count % per_row != 0:
            rows.append(dict(list(paged_data.items())[start:]))
        else:
            rows.append(dict(list(paged_data.items())[start:end]))

    page_counts = (item_counts + per_page - 1) // per_page  # 페이지 수 계산

    # 템플릿 렌더링
    return render_template(
        "view_product.html",
        datas=paged_data.items(),
        row1=rows[0].items() if len(rows) > 0 else [],
        row2=rows[1].items() if len(rows) > 1 else [],
        limit=per_page,
        page=page,
        page_count=page_counts,
        total=item_counts,
        popular_items=popular_items,  # 인기 상품 추가
        category=category
    )

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
    data = DB.get_item_byname_in_history(str(name), session['id'])
    print(data)
    return render_template("review_write2.html", name=name, id=session['id'], data=data)

# 리뷰 db에 등록
@application.route("/reg_review", methods=['POST'])
def reg_review():
    data=request.form
    print(data['star'])
    item = DB.get_item_byname_in_history(data['name'], session['id'])
    itemImgPath = item['img_path']
    image_file=request.files["file"]
    image_file.save("static/images/inputImages/{}".format(image_file.filename))
    DB.reg_review(data, image_file.filename, session, itemImgPath)
    return redirect(url_for('view_review'))

# 상품 등록
@application.route("/registerItem")
def reg_item():
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    return render_template("registerItem.html")

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
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    
    page = request.args.get("page", 0, type = int)
    per_page=9
    per_row=3
    row_count=int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    data=DB.gr_get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):
        if(i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row]) 
    
    return render_template(
        "grpurchase_ViewAll.html",
        datas=data.items(),
        row1 = locals()['data_0'].items(),
        row2 = locals()['data_1'].items(),
        row3 = locals()['data_2'].items(),
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total = item_counts
    )

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
    #return render_template("grpurchase_ViewAll.html", data=data, img_path="static/images/inputImages/{}".format(image_file.filename))
    return redirect(url_for('grpPurchase'))

#동적라우팅
@application.route("/grpurchaseDetail/<name>/")
def gr_view_item_detail(name):
    print("###name:",name)
    data = DB.gr_get_item_byname(str(name))
    print("####data:",data)
    return render_template("grpurchaseDetail.html", name=name, data=data)

# 공동구매 상세페이지
@application.route("/grpurchaseDetail")
def grpurchaseDetail():
    return render_template("grpurchaseDetail.html")


# 공동구매 수량 db에 등록
@application.route("/gr_quantity", methods=['POST'])
def gr_quantity():
    data = {
            'name': request.form['name'],
            'quantity': int(request.form['quantity']),
            'cnt': int(request.form['cnt'])  # 주문 가능 수량이 필요하면 추가
        }
    # 데이터 업데이트
    DB.update_quantity(data)
    updated_item = DB.db.child("gr_item").child(data['name']).get().val()
    return redirect(url_for('grpPurchase'))

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

    page_counts = int((item_counts / per_page)+1)

    if(item_counts%per_page==0):
        page_counts -= 1


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
        page_count=page_counts,
        total=item_counts)

#동적라우팅
@application.route("/review_Vieweach/<name>/")
def review_detail(name):
    print("###name:",name)
    data = DB.get_review_byname(str(name))
    print("####data:",data)
    return render_template("review_Vieweach.html", name=name, data=data)

# 상품등록
@application.route("/submit_item", methods=["POST"])
def reg_item_submit_post():
    image_file = request.files["fileUpload"]
    image_file.save("static/images/inputImages/{}".format(image_file.filename))
    data = request.form
    print(data['name'], data['seller'], data['address'], data['category'], data['method'], data['status'], data['phone'])
    DB.insert_item(data['name'], data, image_file.filename)
    return redirect(url_for('view_product'))

# 구매&교환 기능
@application.route("/buyExchange/<name>/")
def reg_buyExchange(name):
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    data = DB.get_item_byname(name)
    DB.reg_buy(session['id'], data, name)
    flash("상품이 거래 완료되었습니다")
    return redirect(url_for('view_history'))

# 장바구니에 담기 기능
@application.route("/cart/<name>/")
def reg_cart(name):
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    
    data = DB.get_item_byname(name)
    DB.reg_cart(session['id'], data, name)
    return redirect(url_for('view_cart'))

# 장바구니 모아보기 기능
@application.route("/cart")
def view_cart():
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    
    # DB에서 사용자 장바구니 데이터 가져오기
    user_info = DB.get_user_info_byId(user_id)
    cart_items = DB.get_cart_items(user_id)

    # 총합계 계산
    total_price = sum(int(item['price']) for item in cart_items.values())

    return render_template(
        "cart.html",
        cart_items=cart_items,  # 템플릿에서 사용할 데이터
        user_info=user_info,
        total_price=total_price
    )

# 장바구니 상품 구매 기능
@application.route("/buyInCart")
def buyInCart():
    flash("구매 완료 되었습니다!")
    DB.reg_buy_all_in_cart(session['id'])
    return render_template("review_write1.html")

# 장바구니 삭제 기능
@application.route("/removeCart/<name>/")
def remove_cart(name):
    DB.remove_cart_item(name, session['id'])
    return redirect(url_for('view_cart'))

# 구매내역 모아보기 기능
@application.route("/history")
def view_history():
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    
    # DB에서 사용자 장바구니 데이터 가져오기
    user_info = DB.get_user_info_byId(user_id)
    history_items = DB.get_history_items(user_id)
    print(history_items)
    return render_template(
        "review_write1.html",
        history_items=history_items,  # 템플릿에서 사용할 데이터
        user_info=user_info
    )

# 좋아요 기능
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'], name)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):    
    itemInfo = DB.get_item_byname(name)
    DB.update_heart(session['id'], 'Y', itemInfo, name)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    itemInfo = DB.get_item_byname(name)
    DB.update_heart(session['id'],'N',itemInfo, name)
    return jsonify({'msg': '안좋아요 완료!'})

# 좋아요 모아보기
@application.route("/heart")
def view_heart():
    user_id = session.get('id')  # 현재 로그인한 사용자 ID
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('view_logIn'))
    
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