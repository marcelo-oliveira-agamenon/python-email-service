import smtplib, ssl, os, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL_PRO_SMTP = os.getenv("EMAIL_PRO_SMTP")
EMAIL_PRO_PORT = os.getenv("EMAIL_PRO_PORT")
EMAIL_PRO_PASSWORD = os.getenv("EMAIL_PRO_PASSWORD")
EMAIL_PRO = os.getenv("EMAIL_PRO")

context = ssl.create_default_context()

def chooseSubject(typeEmail):
    if typeEmail == "signup":
        return "Welcome to Cash And Grab"
    else:
        return ""

def chooseTemplate(typeEmail, user):
    if typeEmail == "signup":
        with open("./template/welcome.html", "r") as file:
            html_template = file.read()
            html_template = re.sub(r"{{\s*Time\s*}}", str(datetime.now().year), html_template)
            html_template = re.sub(r"{{\s*Name\s*}}", str(user["Name"]), html_template)
        return html_template
    else:
        return ""


def sendEmail(user, typeEmail):
    template = chooseTemplate(typeEmail, user)
    
    receiver_email = user["Email"]
    message = MIMEMultipart("alternative")
    message["Subject"] = chooseSubject(typeEmail)
    message["From"] = EMAIL_PRO
    message["To"] = receiver_email
        
    part = MIMEText(template, "html")
    message.attach(part)
  
    with smtplib.SMTP_SSL(EMAIL_PRO_SMTP, EMAIL_PRO_PORT, context=context) as srv:
        srv.login(EMAIL_PRO, EMAIL_PRO_PASSWORD)
        srv.sendmail(EMAIL_PRO, receiver_email, message.as_string())
        print("email sended")