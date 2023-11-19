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
app.secret_key = 'mrvishal2k2'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    user = session.get('email', None)
    if not user:
        #flash("Please login first!")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "GET":
        return 404
    
    print(request.form.to_dict())
    return "Success"
    
    
@app.route("/logout")
def logout():
    session["email"] = None 
    return render_template(url_for("index"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        data = request.form.to_dict() 
        #print(data)
        x = db.users.find_one({"email":data.get('email')})
        if x and check_password_hash(x.get('pass'), data.get('pass')):
            session['email'] = data.get('email')
            return redirect(url_for('dashboard'))
        #flash("Wrong credentials!", "danger")
        return redirect(url_for('login'))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html") 
    else:
        data = request.form.to_dict() 
        print(data)
        x = db.users.find_one({"email":data.get('email')})
        if x:
            #flash("User with this email already exist", "danger")
            return redirect(url_for('register'))
        #flash("Account created!", "success")
        db.users.insert_one({"fname":data.get('fname'), "email":data.get('email').lower(), "pnum":data.get('pnum'), "pass":generate_password_hash(data.get('pass'), method='pbkdf2:sha256')})
        return redirect(url_for('login'))


@app.errorhandler(404)
def handle_404(e):
    return render_template('notfound.html')    

@app.errorhandler(505)
def handle_505(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 