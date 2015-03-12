#!--*--coding:utf8--*--


import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config import config

def send_mail(sender, sender_pw, receiver, subject, mail_info):
    msg = MIMEText(mail_info, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect() 
    smtp.login(sender, sender_pw) 
    smtp.set_debuglevel(1)
    smtp.sendmail(sender, receiver, msg.as_string()) 
    smtp.quit()
