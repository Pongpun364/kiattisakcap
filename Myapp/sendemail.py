
#################ส่งเมลล์ภาษาไทย########################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'ttoptap25@gmail.com'
	mypassword = 'YOB0123@#'
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'admin_cap sell'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
subject = 'ยืนยันการสมัครเว็บไซต์ ขายหมวกออนไลน์'
newmembername = 'สมพงษ์'
content = ''' เนื่งจากความปลอดภัยของการเข้าใช้ : 
กรุณายืนยันอีเมลล์ ผ่านลิงก์ที่เเนบมานี้
 '''
link = 'http://www.google.com/confirm/516516516'

msg = 'สวัสดีคุณ {}\n\n{}  \n Verify Link : {}'.format(newmembername,content,link)

sendthai('ttoptap25@gmail.com,pongpun364@hotmail.com',subject,msg)

# หากต้องการส่งหลายคนสามารถใส่คอมม่าใน string ได้เลย เช่น 'loongTu1@gmail.com,loongTu2@gmail.com'


'''
-------------------------
ตั้งค่าให้เป็นสีเขียวก่อนส่ง แล้วลองรีเฟรชดู ( on )
https://myaccount.google.com/lesssecureapps

'''




