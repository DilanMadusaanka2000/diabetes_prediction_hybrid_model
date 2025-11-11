import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Brevo SMTP settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp-relay.brevo.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "Predict Diabetics")


def send_otp_email(to_email: str, otp: str):
    """Send OTP email using Brevo SMTP"""
    try:
        msg = MIMEMultipart()
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = to_email
        msg["Subject"] = "Your OTP Code for Login"

        html = f"""
        <html>
            <body>
                <h2>OTP Verification</h2>
                <p>Your OTP is: <b>{otp}</b></p>
                <p>Expires in 5 minutes.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f" OTP email sent to {to_email}")
        return True

    except Exception as e:
        print(f" SMTP Error: {e}")
        return False
