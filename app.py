from flask import Flask, render_template, request  

application = Flask(__name__)  

@application.route("/")  
def hello():  
    return render_template("index.html")  

@application.route("/list")   
def view_list():  
    return render_template("list.html")  

@application.route("/review")   
def view_review():  
    return render_template("review.html")  

@application.route("/reg_items")   
def reg_item():  
    return render_template("reg_items.html")  

@application.route("/reg_reviews")   
def reg_review():  
    return render_template("reg_reviews.html")  

@application.route("/submit_item", methods=["GET", "POST"])  
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
    return render_template("reg_item.html")  # Adjust the template as needed  
