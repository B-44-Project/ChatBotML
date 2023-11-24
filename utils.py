import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

sender_name = "Support Team"
sender_email = "ChatBotWithML@gmail.com"


# Gmail SMTP server and port
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Your Gmail credentials
username = "ChatBotWithML@gmail.com"
password = "rbcuezxrezygoaek"




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