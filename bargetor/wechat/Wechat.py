# -*- coding: utf-8 -*-
from bargetor.wechat.WechatPage import *
from bargetor.wechat.WechatRequest import *

import logging
import traceback

log = logging.getLogger(__name__)

class Wechat(object):
    """docstring for Wechat"""
    def __init__(self, username = None, password = None):
        super(Wechat, self).__init__()
        self.username = username
        self.password = password
        self.request_token = None

        self.login_page = None
        self.setting_page = None
        self.follower_page = None

    def wechat_login(self):
        if not self.username or not self.password: return None

        if not self.login_page:
            self.login_page = WechatLoginRequest(self.username, self.password)

        self.login_page.login()
        self.request_token = self.login_page.request_token
        return self.request_token

    def request_user_setting_page(self):
        self.setting_page = WechatSettingPage(self.request_token)
        return self.setting_page

    def request_wechat_follower_page(self):
        self.follower_page = WechatFollowerPage(self.request_token)
        return self.follower_page

    def is_login(self):
        return self.login_page and self.login_page.is_login()



# wechat = Wechat()
# wechat.username = 'bargetor_public@sina.com'
# wechat.password = 'lanqiao@mj'

# token = wechat.wechat_auto_login()
# wechat.request_user_setting_page()

# follower =  WechatFollowerPage(token)
# print follower.request_wechat_follower_page()
