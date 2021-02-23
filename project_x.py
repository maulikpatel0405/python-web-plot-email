import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email.encoders import encode_base64
import os

file = 'stock_price.txt'
username = 'maulikdevpatel@gmail.com'
password = ''
send_from = 'maulikdevpatel@gmail.com'
send_to = 'maulikdevpatel@gmail.com'
Cc = 'mananpandya1990@gmail.com'
msg = MIMEMultipart()
msg['From'] = send_from
msg['To'] = send_to
msg['Cc'] = Cc
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = 'Hello Friends!! This is a python constructed email.'
# server = smtplib.SMTP('smtp.gmail.com')
port = '587'
fp = open(file, 'rb')
part = MIMEBase('application', 'vnd.ms-excel')
part.set_payload(fp.read())
fp.close()
encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename='stock_price.txt')
msg.attach(part)
smtp = smtplib.SMTP('smtp.gmail.com', port)
smtp.ehlo()
# print(smtp.ehlo())
smtp.starttls()
# print(smtp.starttls())
'''
smtp.login(username, password)
smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
smtp.quit()
'''