#!/usr/bin/python
#coding:utf-8
import requests

SEND_CLOUD_URL = "http://sendcloud.sohu.com/webapi/mail.send.json"
BASE_PARAMS = {"api_user": "bargetor_test_C9Lnuz",
                "api_key" : "va1NbZRs1VIQPk1b"}

def send_email(from_addr, from_name, to, subject, content):
    params = dict(BASE_PARAMS)
    params['from'] = from_addr
    params['fromname'] = from_name
    params['to'] = to
    params['subject'] = subject
    params['html'] = content

    print params

    r = requests.post(SEND_CLOUD_URL, files = {}, data = params)
    return r.text


url = "http://sendcloud.sohu.com/webapi/mail.send.json"
# files={ "file1": (u"1.pdf", open(u"1.pdf", "rb")),
#        "file2": (u"2.pdf", open(u"2.pdf", "rb"))}

# 不同于登录SendCloud站点的帐号，您需要登录后台创建发信子帐号，使用子帐号和密码才可以进行邮件的发送。
params = {"api_user": "bargetor_test_C9Lnuz", \
    "api_key" : "va1NbZRs1VIQPk1b",\
    "to" : "madgin@qq.com", \
    "from" : "chestnut@bargetor.com", \
    "fromname" : "SendCloud测试邮件", \
    "subject" : "来自SendCloud的第一封邮件！", \
    "html": "你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！" \
}

print params

r = requests.post(url, files = {}, data = params)
print r.text

print send_email('chestnut@bargetor.com', 'chestnut', 'madgin@qq.com', 'Chestnut系统通知', '您有一个事务需要处理！')
