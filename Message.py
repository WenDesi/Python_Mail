#encoding=utf-8

class Message(object):

    def __init__(self,ip,subject,date,detail_msg):
        self.ip = ip
        self.subject = subject
        self.date = date
        self.detail_msg = detail_msg

    def __repr__(self):
        string =  '\nip: ' + self.ip
        string += '\ndate: ' + self.date
        string += '\nsubject: ' + self.subject
        string += '\ndetail_msg: ' + self.detail_msg

        return string