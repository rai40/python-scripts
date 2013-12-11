import urllib, urllib2
import time,traceback
from time import sleep

def format_number(line=''):
	line = line.replace("-","")
	line = line.replace(" ","")
	if line.startswith("0"):
		line = line[1:]
	if "+92" not in line:
		line = "+92"+line
	return line

print "Running SMS Sender..."
def send_message(message="", from_no="8001", to_no='+923344156260', coding=0, priority='2'):
    try:
	values = {'username' : 'smsall' , 'password' : 'smsall' , 'text' : message,'from': from_no, 'to' :to_no , 'priority' : priority , 'coding' : str(coding), 'charset' : 'utf-8'}
	rs=urllib2.urlopen(urllib2.Request('http://65.98.91.178:13013/cgi-bin/sendsms?' + urllib.urlencode(values))).read()
	print to_no, from_no
	sleep(0.0333)
    except Exception:
        print traceback.format_exc()
    return


import MySQLdb
q = """SELECT mem.Cell_Number FROM new_corporate_db.corporate_main_corporate_membership cmem
		INNER JOIN new_corporate_db.corporate_main_member mem
		ON (mem.id=cmem.FK_Member_ID)
		WHERE cmem.FK_Corporation_ID=47 or cmem.FK_Corporation_ID=5"""
db = MySQLdb.connect("65.98.23.42","smsall","UWI$m$@ll-2342","new_corporate_db" )
cursor = db.cursor()
cursor.execute(q)
data = cursor.fetchall()

db.close()

message = """Application forms for Prime Minister Youth Business Loans are available free of cost at all branches of National Bank and First Women Bank. 
For information, complaints and suggestions, you may call 0800-77000 or visit http://pmybl.pmo.gov.pk or any branch of NBP or FWB. \n\n(Sent using SMSall.pk)\n"""
# Open database connection

i = 0
#data1 = ['03224954393','3214075192']
for row in data:
	num = row[0]
	num = format_number(str(num))
	print str(num)
	send_message(message, "80028", num, "0", "2")
	if i==200:
		break
	i=i+1
print "total sent %s" %i