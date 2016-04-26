#encoding=utf-8

import imaplib
import smtplib
import email

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from Message import *

class Mail(object):

    def __init__(self, mailhost, account, password, port = 993, ssl = 1):
        self.receive_mail_host = 'imap.' + mailhost
        self.send_mail_host = 'smtp.' + mailhost
        self.account = account
        self.password = password
        self.port = port
        self.ssl = ssl

        self.send_email_from = 'J.A.R.V.I.S.<18188609675@126.com>'

        self.last_email_date = ''

    def send_mail(self,send_info, type = 'text'):
        msg = MIMEText(send_info.detail_msg,'html','utf-8')

        msg['Subject'] = send_info.subject
        msg['From'] = self.send_email_from
        msg['To'] = send_info.ip

        smtp = smtplib.SMTP()
        smtp.connect(self.send_mail_host)
        smtp.login(self.account, self.password)
        smtp.sendmail(self.account, [send_info.ip], msg.as_string())
        smtp.quit()


    def get_mail(self):
        #是否采用ssl
        if self.ssl == 1:
            imapServer = imaplib.IMAP4_SSL(self.receive_mail_host, self.port)
        else:
            print self.receive_mail_host
            imapServer = imaplib.IMAP4(self.receive_mail_host, self.port)
        imapServer.login(self.account, self.password)

        resp, items = imapServer.select('INBOX')
        resp, mailData = imapServer.fetch(items[0], "(RFC822)")
        mailText = mailData[0][1]
        msg = email.message_from_string(mailText)

        # print msg
        ls = msg["From"].split(' ')
        strfrom = ''
        if(len(ls) == 2):
           fromname = email.Header.decode_header((ls[0]).strip('\"'))
           strfrom = 'From : ' + self.my_unicode(fromname[0][0], fromname[0][1]) + ls[1]
           print ls[1]
        else:
           strfrom = 'From : ' + msg["From"]
        strdate = 'Date : ' + msg["Date"]
        subject = email.Header.decode_header(msg["Subject"])
        sub = self.my_unicode(subject[0][0], subject[0][1])
        strsub = 'Subject : ' + sub

        # mailContent, suffix = self.parseEmail(msg)

        mail_info = Message(ls[1],sub,msg['Date'],'')
        return mail_info


    #字符编码转换方法
    def my_unicode(self, s, encoding):
        if encoding:
            return unicode(s, encoding)
        else:
            return unicode(s)

    #解析IP地址
    def anlysis_ip(self, ip):
        pass




if __name__ == '__main__':
    wds = Mail('126.com', '18188609675@126.com', 'wds2006sdo', 143, 0)
    print wds.get_mail()

    string = '<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>good!'
    # wds.send_mail(u'本机IP报告 —— created by wds',u'Hello 温德斯\n   这里是你的智能机器人，专门帮你发送您的IP地址的\n您的IP地址为128.33.22.1')