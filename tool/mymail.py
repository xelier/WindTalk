#coding:utf-8
"""
send email module
"""

import os
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

_mail_host = ''
_user = ''


def constructEmail(subject, message, attachFileList=None):
    """
    construct email
    """
    if attachFileList is None:
        attachFileList = []
    parentDir = os.path.dirname(os.path.dirname(__file__))
    _mailTo = open(os.path.join(parentDir, 'config', 'mailto.txt')).read()
    msg = MIMEMultipart()
    for attachFile in attachFileList:
        if attachFile is not None and attachFile != '':
            print(attachFile)
            att = MIMEText(open(attachFile, 'rb').read(), 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment;filename="%s"' % os.path.split(attachFile)[1]
            msg.attach(att)
    body = MIMEText(message, _subtype='html', _charset='gb2312')
    msg.attach(body)
    msg['To'] = _mailTo
    msg['from'] = _user
    msg['subject'] = subject
    return msg, _mailTo


def sendEmailToUser(subject, message, mailTo, ccTo=None):
    """
    发送邮件给指定用户
    :param subject: 邮件标题
    :param message: 邮件内容(html格式)
    :param mailTo: 收件人(字符串，逗号分隔)
    """
    mailHead = '<html><head><style>\
    body{font-family:  "Microsoft YaHei", Helvetica, Arial, sans-serif;}\
    </style></head><body>'
    mailEnd = '</body></html>'
    msg = MIMEMultipart()
    message = message.replace('\n', '<br>')
    body = MIMEText(mailHead + message + mailEnd, _subtype='html', _charset='utf-8')
    msg.attach(body)
    msg['To'] = mailTo
    msg['cc'] = ccTo
    msg['from'] = _user
    msg['subject'] = subject
    try:
        smtpServer = smtplib.SMTP(host=_mail_host, port=25)
        mailtoList = mailTo.split(',')
        ccTo = ccTo.split(',')
        mailTo = mailtoList + ccTo if ccTo else mailtoList
        smtpServer.sendmail(_user, mailTo, msg.as_string())
        print(time.ctime())
        print("邮件已通过%s，发送至%s" % (_user, mailTo))
        smtpServer.close()
    except Exception as e:
        print('Exception got when sending email. Exception: %s' % e)



if __name__ == '__main__':
    sendEmailToUser('测试', '哈哈', ','.join(['1047094261@qq.com']), ','.join(['1047094261@qq.com']))
