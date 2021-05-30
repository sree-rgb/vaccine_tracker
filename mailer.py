import smtplib, ssl

sender_email = ""
receiver_email = ""
message = """\
Subject: Hi there

This message is sent from Python.{}"""

port = 465  # For SSL
password = input("Type your password and press enter: ")

# Create a secure SSL context
def mailer(message):
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login("thengacoconut@gmail.com", password)
		server.sendmail(sender_email, receiver_email, message)

	# TODO: Send email here
# if __name__ == '__main__':
#