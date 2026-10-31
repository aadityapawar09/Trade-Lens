import os
import smtplib
from email.message import EmailMessage


def send_email(to_address, filename):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    if not sender or not password:
        print("Please add EMAIL_ADDRESS and EMAIL_PASSWORD to your .env file.")
        return

    # Build the email: subject, sender, receiver and body text
    message = EmailMessage()
    message["Subject"] = "Your TradeLens Stock Research Report"
    message["From"] = sender
    message["To"] = to_address
    message.set_content("Hello,\n\nPlease find your stock research report attached.\n\nTradeLens")

    # Attach the PDF file ("rb" means read the file as raw bytes)
    with open(filename, "rb") as file:
        message.add_attachment(file.read(), maintype="application", subtype="pdf", filename=filename)

    # Log in to Gmail and send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password.replace(" ", ""))
            server.send_message(message)
        print("Email sent successfully to", to_address)
    except Exception as error:
        print("Could not send the email:", error)
