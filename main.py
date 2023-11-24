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
import os, random, time
from db import db
from utils import sendmail

otpstore = {}

app = Flask(
    __name__,
    static_folder = os.path.abspath('static'),
    template_folder = os.path.abspath('templates')
    )
app.secret_key = 'mrvishal2k2'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/', methods=['GET',"POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        data = request.form.to_dict() 
        print(data)
        return "SUccess"
        
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
        x = db.users.find_one({"email":data.get('email')})
        if x and check_password_hash(x.get('pass'), data.get('pass')):
            session['email'] = data.get('email')
            return redirect(url_for('dashboard'))
        #flash("Wrong credentials!", "danger")
        return redirect(url_for('login'))



@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == 'GET':
        return render_template("reset.html")
    else:
        data = request.form.to_dict()
        otp = "".join([random.choice("0123456789") for _ in range(6)]) 
        print(otp) 
        sendmail(data["email"],otp)
        otpstore[data["email"]] = {"otp":str(otp), "time": time.time(), "isDone": False} 
        session["otp_page"] =True
        
        return redirect(url_for("verify", email=data["email"]))
        
        

@app.route("/verify", methods=["GET","POST"])
def verify():
    if request.method == 'GET':
        if not session.get("otp_page") or not session:
            return redirect(url_for("reset"))  
        else:
            return render_template("otp.html", email=request.args.get("email"))
    else:
        codes = ''.join(request.form.getlist("code"))

        email = request.form['email'] 
        
        if email in otpstore:
            daata = otpstore[email] 
            if int(time.time())-int(daata["time"]) <= 600: # 10 mins timeout
                if codes==daata["otp"]: # correct otp
                    print("passed")
                    otpstore[email]["isDone"] = True
                    return redirect(url_for("setpassword", email=email))
                else:
                    return "Wrong otp"
            else:
                return "Timeout, Try sending otp again later"
        else:
            return redirect(url_for("reset"))

@app.route("/setpassword", methods=["GET", "POST"])     
def setpassword():
    print(otpstore)
    if request.method == 'GET':
        if not session.get("otp_page") or not session:
            return redirect(url_for("reset"))  
        else:
            email = request.args.get("email", None)
            if email is None:
                return redirect(url_for("reset"))
            if otpstore[email]["isDone"]:
                return render_template("setpassword.html", email=request.args.get("email"))
            else:
                return "Incomplete, u not verified otp"
    else: 
        data = request.form.to_dict() 
        #print(data)
        # str(data) 
        email = data["email"]
        hashed_password = generate_password_hash(data["pass1"], method='pbkdf2:sha256')

        result = db.users.update_one(
        {"email": email.lower()},
        {"$set": {"pass": hashed_password}}
        ) 
        if result.matched_count == 1:
            return f"Password updated successfully for user with email: {email}"
        else:
            return f"No user found with email: {email}"
        
        
    
           
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
 
