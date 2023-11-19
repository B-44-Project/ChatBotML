from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Flask,
    render_template, 
    session, 
    redirect, 
    url_for, 
    flash, 
    request
)
from flask_session import Session
import os
from db import db

app = Flask(
    __name__,
    static_folder = os.path.abspath('static'),
    template_folder = os.path.abspath('templates')
    )

Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "GET":
        return 404
    #entries = request['entries'] #request.get_json()
    print(request)
    return "Success"
    
@app.route("/login", methods=["GET","POST"])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    
    data = request.form.to_dict() 
    print(data)
    x = db.users.find_one({"email":data.get('email')})
    if x and check_password_hash(x.get('password'), data.get('pass')):
        session['email'] = data.get('email')
        return redirect(url_for('dashboard'))
    flash("Wrong credentials!", "danger")
    return redirect(url_for('login'))

@app.route("/register", methods=["GET","POST"])
def register_user():
    if request.method == "GET":
        return render_template("register.html")
    data = request.form.to_dict() 
    print(data)
    x = db.users.find_one({"email":data.get('email')})
    if x:
        flash("User with this email already exist", "danger")
        return redirect(url_for('register'))
    flash("Account created!", "success")
    db.users.insert_one({"name":data.get('name'), "email":data.get('email').lower(), "password":generate_password_hash(data.get('pass'), method='sha256')})
    return redirect(url_for('login'))


@app.errorhandler(404)
def handle_404(e):
    return render_template('notfound.html')    

@app.errorhandler(505)
def handle_505(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 