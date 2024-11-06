from flask import Flask, render_template, request
import sys

application = Flask(__name__)

# 홈
@application.route("/")
def hello():
    return render_template("index.html")

# 회원가입
@application.route("/signUp.html")
def view_signUp():
    return render_template("signUp.html")

# 상품 조회
@application.route("/fullproduct.html")
def view_list():
    return render_template("fullproduct.html")

# 리뷰 조회
@application.route("/review_ViewAll.html")
def view_review():
    return render_template("review_ViewAll.html")

# 상품 등록
@application.route("/registerItem.html")
def reg_item():
    return render_template("registerItem.html")

# 리뷰 작성1
@application.route("/review_write1.html")
def reg_review1():
    return render_template("review_write1.html")

# 리뷰 작성2
@application.route("/review_write2.html")
def reg_review2():
    return render_template("review_write2.html")

@application.route("/grpurchase_ViewAll.html")
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
    return render_template("submit_item_result.html", data=data,  img_path="static/images/{}".format(image_file.filename))


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)
