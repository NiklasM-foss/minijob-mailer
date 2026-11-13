import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv 
load_dotenv()

konto = {
    "host": "smtp.gmail.com",
    "port": 465,
    "user": os.getenv("SMTP_USER"),
    "passwort": os.getenv("SMTP_PASS")
}
mail = {
    "empfaenger": os.getenv("SMTP_USER"),
    "betreff": "Test",
    "text": "Hallo, das ist ein test",
}

def sende_smtp(konto,mail):
    msg = EmailMessage()
    msg["From"] = konto["user"]
    msg["To"] = mail["empfaenger"]
    msg["Subject"] = mail["betreff"]
    msg.set_content(mail["text"]) 
    with smtplib.SMTP_SSL(konto["host"], konto["port"]) as server:
        server.login(konto["user"], konto["passwort"]) 
        server.send_message(msg)

try:
    sende_smtp(konto, mail)
    print("Gesendet")
except Exception as e:
    print("Fehler:", e)