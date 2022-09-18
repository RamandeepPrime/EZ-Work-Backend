import smtplib
import os
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from dotenv import load_dotenv

# load_dotenv(dotenv_path='../.env')

SENDER_EMAIL = "ramandeep9540479976@gmail.com"
PASSWORD = os.getenv('PASSWORD')
SERVER = 'smtp.gmail.com'
# PORT= 587
PORT = 465
msg = MIMEMultipart('alternative')


def send_verification_link(receiver_email, hashed_token):

    html = """
	<html>
  <head>
  </head>
  <body>
    <p>
      Hi!<br />
      How are you?<br />
      <a style="padding:0.75rem;border-radius:10px;background-color:rgb(65, 199, 65);display:flex;width:fit-content;cursor:pointer;text-decoration: none;color:white" href="http://localhost:8000/auth/verify?hashed_token={hashed_token}&user_email={receiver_email}">Verification Link </a>Click above
      button to get verified
    </p>
  </body>
</html>

	""".format(hashed_token=hashed_token, receiver_email=receiver_email)

    html = MIMEText(html, 'html')
    msg.attach(html)

    context = ssl.create_default_context()  # gives more security
    with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())


if __name__ == '__main__':

    send_verification_link(SENDER_EMAIL, "here is your pass")
