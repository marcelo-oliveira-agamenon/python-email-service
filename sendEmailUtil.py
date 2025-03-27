import smtplib, ssl, os, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
from writeResponseEmail import writeEmailResponse

load_dotenv()

EMAIL_PRO_SMTP = os.getenv("EMAIL_PRO_SMTP")
EMAIL_PRO_PORT = os.getenv("EMAIL_PRO_PORT")
EMAIL_PRO_PASSWORD = os.getenv("EMAIL_PRO_PASSWORD")
EMAIL_PRO = os.getenv("EMAIL_PRO")

context = ssl.create_default_context()

def chooseSubject(typeEmail):
    if typeEmail == "signup":
        return "Bem vindo ao Cash And Grab"
    elif typeEmail == "newOrder":
        return "Seu Pedido foi realizado na Cash And Grab"
    elif typeEmail == "resetPassword": 
        return "Recuperação de Senha - Código de Verificação"
    else:
        return ""

def chooseTemplate(typeEmail, user):
    if typeEmail == "signup":
        with open("./template/welcome.html", "r") as file:
            html_template = file.read()
            html_template = re.sub(r"{{\s*Time\s*}}", str(datetime.now().year), html_template)
            html_template = re.sub(r"{{\s*Name\s*}}", str(user["Name"]), html_template)
        return html_template
    elif typeEmail == "newOrder":
        with open("./template/newOrder.html", "r") as file:
            html_template = file.read()
            order_value = "{:.2f}".format(user["Value"])
            html_template = re.sub(r"{{\s*Year\s*}}", str(datetime.now().year), html_template)
            html_template = re.sub(r"{{\s*OrderNumber\s*}}", str(user["OrderNumber"]), html_template)
            html_template = re.sub(r"{{\s*Name\s*}}", str(user["UserName"]), html_template)
            html_template = re.sub(r"{{\s*OrderQtd\s*}}", str(user["Quantity"]), html_template)
            html_template = re.sub(r"{{\s*OrderValue\s*}}", order_value, html_template)
        return html_template
    elif typeEmail == "resetPassword":
        with open("./template/resetPassword.html", "r") as file:
            html_template = file.read()
            html_template = re.sub(r"{{\s*Name\s*}}", str(user["Name"]), html_template)
            html_template = re.sub(r"{{\s*Hash\s*}}", str(user["Hash"]), html_template)
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
        writeEmailResponse(typeEmail, data=receiver_email)
        print("email sended")