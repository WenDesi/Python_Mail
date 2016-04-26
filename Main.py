#encoding=utf-8

import time

from Ip import *


event_list = {}
last_mail_date = ''
mail = Mail('126.com', '18188609675@126.com', 'wds2006sdo', 143)
wait_second = 20

def event_ip(message):
    return_ip(message,mail)


# 对邮件名与对应函数进行绑定
def event_register():
    global event_list

    # 收到ip自动返回本机ip
    event_list['ip'] = event_ip

def receiver_mail():
    global last_mail_date
    global event_list

    receive_msg = mail.get_mail()
    if receive_msg.date == last_mail_date:
        return
    if receive_msg.subject not in event_list:
        last_mail_date = receive_msg.date
        return

    last_mail_date = receive_msg.date
    event_list[receive_msg.subject](receive_msg)


if __name__ =="__main__":
    event_register()

    while True:
        receiver_mail()
        time.sleep(wait_second)

