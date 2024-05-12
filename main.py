import re, json, os
from datetime import datetime
from sendEmailUtil import *
from kafka import KafkaConsumer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

ORDER_TOPIC = os.getenv("ORDER_TOPIC")
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")
EMAIL_PRO = os.getenv("EMAIL_PRO")

consumer = KafkaConsumer(ORDER_TOPIC, bootstrap_servers=BOOTSTRAP_SERVER)

print("start listen")

with open("./template/welcome.html", "r") as file:
    html_template = file.read()
    html_template = re.sub(r"{{\s*Time\s*}}", str(datetime.now().year), html_template)

while True:
    for msg in consumer:
        user = json.loads(msg.value.decode("utf-8"))
        html_template = re.sub(r"{{\s*Name\s*}}", str(user["Name"]), html_template)
        
        receiver_email = user["Email"]
        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to Cash And Grab"
        message["From"] = EMAIL_PRO
        message["To"] = receiver_email
        
        part = MIMEText(html_template, "html")
        message.attach(part)

        sendEmail(receiver_email, message.as_string())
