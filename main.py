import json, os
from sendEmailUtil import *
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

ORDER_TOPIC = os.getenv("ORDER_TOPIC")
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")
EMAIL_PRO = os.getenv("EMAIL_PRO")

consumer = KafkaConsumer(ORDER_TOPIC, bootstrap_servers=BOOTSTRAP_SERVER)
print("start listen")

while True:
    for msg in consumer:
        typeEmail = msg.key.decode("utf-8")
        user = json.loads(msg.value.decode("utf-8"))
        receiver_email = user["Email"]
        sendEmail(user, typeEmail)
