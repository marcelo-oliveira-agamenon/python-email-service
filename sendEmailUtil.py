import smtplib, ssl, os
from dotenv import load_dotenv

load_dotenv()

EMAIL_PRO_SMTP = os.getenv("EMAIL_PRO_SMTP")
EMAIL_PRO_PORT = os.getenv("EMAIL_PRO_PORT")
EMAIL_PRO_PASSWORD = os.getenv("EMAIL_PRO_PASSWORD")
EMAIL_PRO = os.getenv("EMAIL_PRO")

context = ssl.create_default_context()

def sendEmail(receiver_email, message):
    with smtplib.SMTP_SSL(EMAIL_PRO_SMTP, EMAIL_PRO_PORT, context=context) as srv:
        srv.login(EMAIL_PRO, EMAIL_PRO_PASSWORD)
        srv.sendmail(EMAIL_PRO, receiver_email, message)
        print("email sended")