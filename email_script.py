import urllib, urllib2
import time


from django.core.management import setup_environ





	
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(to,bcc, subject, text,html, files=[],server="smtp.gmail.com"):
	gmail_user = "rai.ehtisham@smsall.pk"
	gmail_pwd = "admin999"
	FROM = 'rai.ehtisham@smsall.pk'
	assert type(to)==list
	assert type(files)==list
	fro = "SMSall <rai.ehtisham@smsall.pk>"

	msg = MIMEMultipart()
	msg['From'] = fro
	msg['To'] = COMMASPACE.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	#msg.attach( MIMEText(text) )

	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	msg.attach(part1)
	msg.attach(part2)

	server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pwd)
	server.sendmail(FROM, to, msg.as_string())
	server.close()
text = ""
html = """\
<html>
  <head></head>
  <body>
       <img src='http://s8.postimg.org/w5d9tuzw5/corporate1_1.png' width='100%' />
  </body>
</html>
"""
message = "<img src='corporate1.png' />"
sendMail(["cto@smsall.pk"],["aliya.ali@smsall.pk","rai.ehtisham@smsall.pk"],"New & Improved SMSall",text,html,[])
