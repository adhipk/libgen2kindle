from io import BufferedRandom
import tempfile
import os
from dotenv import load_dotenv
from email.message import Message
from urllib.request import urlretrieve
from flask import request
from libgen_api import LibgenSearch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests

load_dotenv()

# Access variables from environment
sender_email = os.getenv('SENDER_EMAIL',"testSender@example.com")
receiver_email = os.getenv('RECEIVER_EMAIL','test@example.com')
password = os.getenv('EMAIL_PASSWORD',"test_password")
smtp_server = os.getenv('SMTP_SERVER',"GSMTP")
smtp_port = int(os.getenv('SMTP_PORT',587))
subject = os.getenv('EMAIL_SUBJECT',"")
body = os.getenv('EMAIL_BODY',"")
download_path = "/tmp"

s = LibgenSearch()
extension = "epub"

def searchTitle(titleName:str) -> list[dict[str,str]]:

	title_filters = {'Extension':extension}
	results = s.search_title_filtered(titleName,title_filters)
	results.extend(s.search_author_filtered(titleName,title_filters))
	# print(results)
	return results

def generateDownloadLinks(title):
	return s.resolve_download_links(title)

def sendEmail(attachment,title):

	# Create the email message
	message = MIMEMultipart()
	message['Subject'] = subject
	message['From'] = sender_email
	message['To'] = receiver_email

	# Attach the email body
	message.attach(MIMEText(body, 'plain'))

	# Attach the file
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(attachment)

	# Encode the attachment in base64
	encoders.encode_base64(part)

	# Add header to the attachment
	part.add_header('Content-Disposition', f"attachment; filename={title}")

	# Attach the file to the message
	message.attach(part)

	# Convert the message to a string
	text = message.as_string()

	# Send the email
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
		smtp_server.login(sender_email, password)
		smtp_server.sendmail(sender_email, receiver_email, message.as_string())

	# remove tmp file

	print('Email sent!')
def send2kindle(mirror:str,title:str):
	try:
		downloadLinks = generateDownloadLinks({"Mirror_1":mirror});


		# download file to tmp
		with tempfile.NamedTemporaryFile(prefix=title,suffix=f".{extension}") as tmp:
			if downloadLinks:
				r = requests.get(downloadLinks["GET"],{"downloadFormat":extension})
				tmp.write(r.content)
				# seek(0) to read
				tmp.seek(0)
				attachment = tmp.read()
				sendEmail(attachment,f"{tmp.name.split('/')[-1]}")
	except Exception as e:
		print(e)
		return False
	return True
# def main():
# 	titleName = 'Pride and Prejudice'
# 	res = searchTitle(titleName)
# 	if not len(res):
# 		return 0
# 	book = res[0]

# 	send2kindle(book['Mirror_1'],book['Title'])


# if __name__=='__main__':
#     main()
