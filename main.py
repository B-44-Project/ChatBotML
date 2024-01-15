import sys
# uncomment below line in mac
#sys.path.append('/Users/dheeraj/Documents/Project/venv/lib/python3.9/site-packages')

import os
import random
import time
import re

from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request,
    jsonify
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import json

from db import db
from utils import sendmail, openaichat, getintent, chatwithollama


otpstore = {}
conversation_history = []


app = Flask(
    __name__,
    static_folder = os.path.abspath('static'),
    template_folder = os.path.abspath('templates')
    )
app.secret_key = 'mrvishal2k2'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

#index page
@app.route('/', methods=['GET',"POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        data = request.form.to_dict() 
        print(data)
        return "SUccess"
        
#dashboard page        
@app.route('/dashboard')
def dashboard():
    user = session.get('email', None)
    if not user:
        flash("Please login first!", "success")
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session["fname"])


@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "GET":
        return 404
    else:  
        # Ref: https://gist.github.com/mberman84/a1291cfb08d0a37c3d439028f3bc5f26
        user_text = request.json["userText"]  
        conversation_history.append(f"User: {user_text}")

        full_prompt = "\n".join(conversation_history)
        
        
        intent = getintent(user_text)
        print(intent) 
        # Add intent details to final msg if found, else do nothing
        opintent = f"Detected Intent is:{intent}\n\n" if intent != "unknown" else ""
            
        # search order id
        pattern = r"\b[1-3][0-9]{1,2}\b"  # 1-300 order id
        
        match = re.search(pattern, user_text) 
        if match:
            order_id = match.group(0) 
            print("order id detected", order_id)
            # get order details from db and append it to user msg within bracket
            # can pass order details here from db
            ordermsg = f"(Order id detected, order details: {order_id}, status: delayed by 2 days)"
            user_text += ordermsg
            full_prompt += ordermsg
        
        full_prompt += f"\nBot: " 
        
        print(full_prompt) 
        #content, rtype = openaichat(full_prompt)  
        content, rtype = chatwithollama(user_text)  
        
        conversation_history.append(f"Bot: {content}")

        if rtype==404:
            return jsonify({"error": "Not Found"}), 404 
        else:
            return jsonify({"message": f"{opintent}{content}"}), 200

    
    
@app.route("/chathistory", methods=["POST", "GET"])
def chathistory():
    if request.method == "GET":
        return render_template("chathistory.html")

#help page
@app.route("/help", methods=["POST", "GET"])
def help():
    if request.method == "GET":
        return render_template("help.html")

#logout page    
@app.route("/logout")
def logout():
    session["email"] = None 
    return render_template(url_for("index"))

#login page
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        data = request.form.to_dict() 
        x = db.users.find_one({"email":data.get('email')})
        if x and check_password_hash(x.get('pass'), data.get('pass')):
            session["fname"] = x.get('fname')
            session['email'] = data.get('email')
            return redirect(url_for('dashboard'))
        flash("Wrong credentials!", "error") 
        return redirect(url_for('login'))

#reset password page
@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == 'GET':
        return render_template("reset.html")
    else:
        data = request.form.to_dict() 
        email_exists = bool(db.users.find_one({"email": data["email"]})) 
        if not email_exists:
            flash("Account with the mail doesn't exist", "error")
            return redirect(url_for('register'))     

        otp = "".join([random.choice("0123456789") for _ in range(6)]) 
        print(otp) 
        sendmail(data["email"], otp)
        otpstore[data["email"]] = {"otp":str(otp), "time": time.time(), "isDone": False} 
        session["otp_page"] =True
        
        return redirect(url_for("verify", email=data["email"]))
        
#verifying otp page        
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
                    otpstore[email]["isDone"] = True
                    return redirect(url_for("setpassword", email=email))
                else:
                    flash("Invalid OTP, Try again", "error")
                    return redirect(url_for("verify", email=email))
            else:
                flash("Timeout, Try sending otp again later","error") 
                return redirect(url_for("verify", email=email))
        else:
            return redirect(url_for("reset"))


@app.route("/setpassword", methods=["GET", "POST"])     
def setpassword():
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
        email = data["email"]
        hashed_password = generate_password_hash(data["pass1"], method='pbkdf2:sha256')

        result = db.users.update_one(
        {"email": email.lower()},
        {"$set": {"pass": hashed_password}}
        ) 
        if result.matched_count == 1:
            return render_template("exit.html")
        else:
            return f"No user found with email: {email}"
        
#register page                   
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html") 
    else:
        data = request.form.to_dict() 
        print(data)
        x = db.users.find_one({"email":data.get('email')})
        if x:
            flash("User with this email already exist", "error")
            return redirect(url_for('register'))
        flash("Account created!", "success")
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
 
