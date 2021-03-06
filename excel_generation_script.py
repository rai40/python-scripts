import urllib, urllib2
import time
import api_client

#sys.path.append("/home/ehtisham/jango/survey")
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management import setup_environ
import settings
from django.db.models import Q
from wb_sanitation_survey.models import *
setup_environ(settings)

SERVER = api_client.SERVER
PORT = api_client.PORT
CLIENT = api_client.APIClient(SERVER, PORT)


if __name__ == "__main__":
	import xlwt
	q = """SELECT intr.id id,uc.district district,uc.markaz markaz,uc.name uc,vlg.name vlg,
		intr.username username,tm.name team,
		intr.latitude lati, intr.longitude longi,intr.image image
		FROM (SELECT * FROM new_survey_db.wb_sanitation_survey_interview group by latitude,longitude,image) intr
		INNER JOIN new_survey_db.wb_sanitation_survey_village vlg
		ON (vlg.id=intr.fk_village_id)
		INNER JOIN new_survey_db.wb_sanitation_survey_union_council uc
		ON (uc.id=vlg.fk_union_council_id)
		INNER JOIN new_survey_db.wb_sanitation_survey_users usr
		ON (intr.fk_user_id=usr.id)
		INNER JOIN new_survey_db.wb_sanitation_survey_team tm
		ON (tm.id=usr.fk_team_id)"""
	q+= """ group by intr.fk_village_id,intr.fk_user_id,intr.id"""
	q+= """ order by uc.district,uc.markaz,intr.username,uc.name,vlg.name"""
	wbk = xlwt.Workbook()
	sheet = wbk.add_sheet('sheet 1')

	# indexing is zero based, row then column
	rs = interview.objects.raw(q)
	#print rs.count()
	i = 1
	sheet.write(0,0,'District')
	sheet.write(0,1,'Markaz')
	sheet.write(0,2,'Username')
	sheet.write(0,3,'UC')
	sheet.write(0,4,'Village')
	sheet.write(0,5,'Team')
	sheet.write(0,6,'Latitude')
	sheet.write(0,7,'Longitude')
	sheet.write(0,8,'Image')
	for row in rs:
		sheet.write(i,0,row.district)
		sheet.write(i,1,row.markaz)
		sheet.write(i,2,row.username)
		sheet.write(i,3,row.uc)
		sheet.write(i,4,row.vlg)
		sheet.write(i,5,row.team)
		sheet.write(i,6,row.lati)
		sheet.write(i,7,row.longi)
		sheet.write(i,8,os.path.isfile('/home/ehtisham/jango/survey/survey_images/'+row.image+'.jpg'))
		i = i + 1

	wbk.save('/home/ehtisham/surveys_data.xls')
	#resp = CLIENT.post('/survey/questions/save_interview' , parameters=param)

	print "resp"




import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os

def sendMail(to, subject, text, files=[],server="smtp.gmail.com"):
	gmail_user = "rai.ehtisham@smsall.pk"
	gmail_pwd = "password"
	FROM = 'rai.ehtisham@smsall.pk'
	assert type(to)==list
	assert type(files)==list
	fro = "Ehtisham <rai.ehtisham@smsall.pk>"

	msg = MIMEMultipart()
	msg['From'] = fro
	msg['To'] = COMMASPACE.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach( MIMEText(text) )

	for file in files:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(file,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'% os.path.basename(file))
		msg.attach(part)

	server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pwd)
	server.sendmail(FROM, to, msg.as_string())
	server.close()

sendMail(["ddmnelgrdd@gmail.com"],"GPS Data Autogenerated Email","Survey Data file is attached. File contains up to date survey records.",["/home/ehtisham/surveys_data.xls"])



