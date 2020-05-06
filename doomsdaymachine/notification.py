import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_notification(config, notification):
    if "email_notification" not in config:
        return
    if config["email_notification"]["ssl"]:
        smtp = smtplib.SMTP_SSL(config["email_notification"]["host"])
    else:
        smtp = smtplib.SMTP(config["email_notification"]["host"])
    if config["email_notification"]["tls"]:
        smtp.starttls()
    smtp.login(config["email_notification"]["username"], config["email_notification"]["password"])
    message = MIMEMultipart()
    message["From"] = config["email_notification"]["from"]
    message["To"] = config["email_notification"]["to"]
    message["Subject"] = f"Doomsday Machine Notification {str(datetime.datetime.now())}"
    message.attach(MIMEText(notification, "plain"))
    smtp.sendmail(config["email_notification"]["from"], config["email_notification"]["to"], message.as_string())

