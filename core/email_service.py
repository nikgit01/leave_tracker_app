import smtplib
from email.message import EmailMessage

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SENDER_EMAIL = "projectpy.sender@gmail.com"
SENDER_PASSWORD = "ufccxtohefzuoxnn"


def send_mail(recipient, subject, body):

    if not recipient:
        print("[Email Service] Skipped: No recipient email provided.")
        return
    
    try:
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        print(f"[Email Sent] To: {recipient} | Subject: {subject}")

    except Exception as e:
        print(f"[Email Service Error] Could not send email to {recipient}: {e}")