import os
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER")
USER_TOPIC = os.getenv("USER_TOPIC")

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)

def writeEmailResponse(typeEmail,data):
    if typeEmail == "signup":
        value = str(data)
        key = "welcomeEmailSended"
        producer.send(USER_TOPIC, value.encode(), key.encode())
        return
    return