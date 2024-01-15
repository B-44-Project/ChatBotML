# MOdel: https://colab.research.google.com/drive/1dCwP2CtLm7GRv5mnnmuREYgrdhmr-O1s?usp=sharing

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

sender_name = "Support Team"
sender_email = "ChatBotWithML@gmail.com"


# Gmail SMTP server and port
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Gmail credentials
username = #gmail
password = #password


API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = #api here  


def sendmail(recipient_email, otp):
    body = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        .container {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
        }

        h1 {
            color: #333;
        }

        p {
            color: #666;
        }

        .otp {
            font-size: 24px;
            font-weight: bold;
            color: #0088cc;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OTP Verification</h1>
        <p>Please use the following OTP to verify your account:</p>
        <div class="otp">otp_value</div>
        <p>This OTP is valid for a short duration of 10 minutes.</p>
    </div>
</body>
</html>
''' 
    body = body.replace("otp_value",otp)
    
    message = MIMEMultipart()
    message.attach(MIMEText(body, "html")) 
    message["Subject"] = "Subject: OTP Received"
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = recipient_email

        
    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS for security
        server.starttls()
        
        # Login to your Gmail account
        server.login(username, password)
        
        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

    print("Email sent successfully!")
    
    
def openaichat(message):
        user_text = message
        headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
        }    

        data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_text}],
        "temperature": 0.7
        }

        try:
            response = requests.post(API_URL, headers=headers, json=data)
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"].strip() 
            return content, 200
        except Exception as e: 
            return f"Error making request to OpenAI: {e}", 404
        
def getintent(message):
    import pandas 
    from joblib import dump, load
    model = load('model/intent.joblib')
    new_query = [message]
    prediction = model.predict(new_query)
    #print("Predicted Intent:", prediction)
    return prediction[0]
    
def chatwithollama(message):
    import json
    body = {
    "model": "ThinkBot",
    "prompt": message,
    "stream": False
}
    json_body = json.dumps(body)

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    res = requests.post(url, headers=headers, data=json_body)
    decoded_response = res.json()
    response_content = decoded_response["response"] 
    return response_content, 200