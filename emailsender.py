import smtplib
from email.mime.text import MIMEText

def sendmail(frm,to,subject,message,login,password):
	msg = MIMEText(message, 'html')
	msg['Subject'] = subject
	msg['From'] = frm
	msg['To'] = to

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(login,password)
	s.sendmail(frm, [to], msg.as_string())
	s.quit()
