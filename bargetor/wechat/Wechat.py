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
        self.image_page = None
        self.dev_setting_page = None

    def wechat_login(self):
        if not self.username or not self.password: return None

        if not self.login_page:
            self.login_page = WechatLoginRequest(self.username, self.password)

        self.login_page.login()
        self.request_token = self.login_page.request_token
        return self.request_token

    def request_user_setting_page(self):
        self.setting_page = WechatSettingPage(self.request_token)
        self.setting_page.open()
        return self.setting_page

    def request_wechat_follower_page(self):
        self.follower_page = WechatFollowerPage(self.request_token)
        self.follower_page.find_all_followers()
        return self.follower_page

    def request_wechat_image_page(self):
        self.image_page = WecahtImageMaterialPage(self.request_token)
        self.image_page.open()

        self.image_page.upload('/Users/Bargetor/Documents/temp/user.png')

    def request_create_app_msg(self):
        # app_msgs_create_request = WechatAppMsgProcessRequest(self.request_token)
        # app_msgs_create_request.add_app_msg_item_by_info('测试', '<p>哈哈</p>', '201079878')
        # app_msgs_create_request.create()

        request = WechatAppMsgCreateRequest(self.request_token)
        app_msg = WechatAppMsg()
        app_msg.add_app_msg_item_by_info('正式创建', '<p>哈哈</p>', '201079878')
        request.create(app_msg)

        send_reqeust = WechatSingleSendAppMsgRequest(self.request_token, '1159047001')
        send_reqeust.send(request.app_msg_id)

    def request_get_app_msgs_list(self):
        request = WechatGetAppMsgListRequest(self.request_token)
        request.open()
        return request.app_msgs

    def request_update_app_msg(self, app_msg):
        app_msg.remove_all_items()
        app_msg.add_app_msg_item_by_info('修改', '<p>修改</p>', '201079878')
        request = WechatAppMsgProcessRequest(self.request_token)
        request.app_msg = app_msg
        request.update()

    def request_wechat_dev_setting_page(self):
        self.dev_setting_page = WechatDevSettingPage(self.request_token)
        self.dev_setting_page.open()

        self.dev_setting_page.modify_server_setting('http://www.bargetor.com/chestnut_proxy.php?wechat_user=bargetor_public@sina.com', 'bargetor_chestnut')

    def is_login(self):
        return self.login_page and self.login_page.is_login()



# wechat = Wechat()
# wechat.username = 'bargetor_public@sina.com'
# wechat.password = 'lanqiao@mj'

# token = wechat.wechat_auto_login()
# wechat.request_user_setting_page()

# follower =  WechatFollowerPage(token)
# print follower.request_wechat_follower_page()
