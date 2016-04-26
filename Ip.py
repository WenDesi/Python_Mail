#encoding=utf-8

import socket

from Mail import *
from Message import *

def get_ip():
    #获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())

    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    return myaddr

def return_ip(message, mail):
    address = message.address
    subject = u'本机IP报告'
    date = ''
    detail_msg = u'Hello 温德斯\n   这里是你的智能机器人，专门帮你发送您的IP地址的\n您的IP地址为%s'.replace('%s',str(get_ip()))

    if address != '641614152@qq.com':
        return

    send_msg = Message(address,subject,date,detail_msg)
    mail.send_mail(send_msg,'html')