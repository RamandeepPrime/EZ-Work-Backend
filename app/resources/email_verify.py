import smtplib,os,ssl

# from dotenv import load_dotenv

# load_dotenv(dotenv_path='../.env')

SENDER_EMAIL= "ramandeep9540479976@gmail.com"
PASSWORD= os.getenv('PASSWORD')
SERVER= 'smtp.gmail.com'
# PORT= 587
PORT = 465

def send_verification_link(receiver_email, message):
	
	context=ssl.create_default_context() #gives more security
	with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
		server.login(SENDER_EMAIL, PASSWORD)
		server.sendmail(SENDER_EMAIL, receiver_email, message)


if __name__ == '__main__':
	
	send_verification_link(SENDER_EMAIL, "here is your pass")

