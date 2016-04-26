#encoding=utf-8

import imaplib
import email

class Mail(object):

    def __init__(self, mailhost, account, password, port = 993, ssl = 1):
        self.mailhost = mailhost
        self.account = account
        self.password = password
        self.port = port
        self.ssl = ssl

    def getMail(self):
        #是否采用ssl
        if self.ssl == 1:
            imapServer = imaplib.IMAP4_SSL(self.mailhost, self.port)
        else:
            imapServer = imaplib.IMAP4(self.mailhost, self.port)
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

        mailContent, suffix = self.parseEmail(msg)

        print '\n'
        print strfrom
        print strdate
        print strsub


    #字符编码转换方法
    def my_unicode(self, s, encoding):
        if encoding:
            return unicode(s, encoding)
        else:
            return unicode(s)

    #获得字符编码方法
    def get_charset(self, message, default="ascii"):
        #Get the message charset
        return message.get_charset()
        return default

    #解析邮件方法（区分出正文与附件）
    def parseEmail(self, msg):
        mailContent = None
        contenttype = None
        suffix =None
        for part in msg.walk():
            if not part.is_multipart():
                contenttype = part.get_content_type()
                filename = part.get_filename()
                charset = self.get_charset(part)
                #是否有附件
                if filename:
                    h = email.Header.Header(filename)
                    dh = email.Header.decode_header(h)
                    fname = dh[0][0]
                    encodeStr = dh[0][1]
                    if encodeStr != None:
                        if charset == None:
                            fname = fname.decode(encodeStr, 'gbk')
                        else:
                            fname = fname.decode(encodeStr, charset)
                    data = part.get_payload(decode=True)
                    print('Attachment : ' + fname)

                else:
                    if contenttype in ['text/plain']:
                        suffix = '.txt'
                    if contenttype in ['text/html']:
                        suffix = '.htm'
                    if charset == None:
                        mailContent = part.get_payload(decode=True)
                    else:
                        mailContent = part.get_payload(decode=True).decode(charset)
        return  (mailContent, suffix)

if __name__ == '__main__':
    wds = Mail('imap.126.com', '18188609675@126.com', 'wds2006sdo', 143, 0)
    wds.getMail()
