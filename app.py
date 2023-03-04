from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import bcrypt
#set app as a Flask instance 
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.secret_key = "testing"

# connect to your Mongo DB database

client = MongoClient("mongodb+srv://b21124:f8Yuo2hEHui6YC3i@cluster0.2kag3bh.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('total_records')
records = db.register

db1 = client.get_database('AddedItems')
addItems = db1.register

def foo():
    bar= db1.get_collection('register')
    return bar

    

@app.route("/", methods=["POST", "GET"])
def main():
    return render_template("main.html")


#assign URLs to have a particular route 
@app.route("/shopkeeper_signup", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        ShopName = request.form.get("ShopName")
        type = request.form.get("typeOfShop")
        reg = request.form.get("reg")
        username = request.form.get("username")
        location = request.form.get("location")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed, 'type': type, 'location': location, 'reg': reg, 'username': username, 'ShopName': ShopName}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')

@app.route("/shopkeeper_login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("shopkeeper_login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

# render home page
@ app.route('/')
def home():
    title = 'Home'
    return render_template('dash.html', title=title)

@app.route("/dashboard", methods=["POST", "GET"])
def dash():
    return render_template("dash.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("users-profile.html")



@app.route("/stock", methods=["POST", "GET"])
def stock(foobar):

    if request.method=="POST":
        itemId = request.form.get("itemId")
        name = request.form.get("name")
        quantity = request.form.get("quantity")
        brand = request.form.get("brand")
        cp = request.form.get("cp")
        sp = request.form.get("sp")

        user_input = {'itemId': itemId, 'name': name, 'quantity': quantity, 'brand':brand, 'cp':cp, 'sp':sp}

        addItems.insert_one(user_input)

    
    
    return render_template("stock.html", foobar=foo())


@app.route("/sales", methods=["POST", "GET"])
def sales():
    return render_template("sales.html")


@app.route("/dues", methods=["POST", "GET"])
def dues():
    return render_template("dues.html")




if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)