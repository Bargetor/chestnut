#!/usr/bin/python
#coding:utf-8
import requests

url="http://sendcloud.sohu.com/webapi/mail.send.json"
#files={ "file1": (u"1.pdf", open(u"1.pdf", "rb")),
#        "file2": (u"2.pdf", open(u"2.pdf", "rb"))}

# 不同于登录SendCloud站点的帐号，您需要登录后台创建发信子帐号，使用子帐号和密码才可以进行邮件的发送。
params = {"api_user": "bargetor_test_C9Lnuz", \
    "api_key" : "va1NbZRs1VIQPk1b",\
    "to" : "madgin@qq.com", \
    "from" : "hello@bargetor.com", \
    "fromname" : "SendCloud测试邮件", \
    "subject" : "来自SendCloud的第一封邮件！", \
    "html": "你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！" \
}

r = requests.post(url, files={}, data=params)
print r.text
