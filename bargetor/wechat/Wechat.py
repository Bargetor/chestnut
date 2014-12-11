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
        app_msg.add_app_msg_item_by_info('该消息来自伟大的chestnut', '<p>哈哈</p>', '200447249', '打扰，得罪')
        # app_msg.add_app_msg_item_by_info('该消息来自伟大的chestnut', '<p>哈哈</p>', '203189048', '打扰，得罪')
        request.create(app_msg)
        # todo delete
        # self.request_send_app_msg_all_follower(app_msg.app_msg_id)

    def request_send_app_msg_all_follower(self, app_msg_id):
        if not app_msg_id : return
        send_request = WechatSingleSendAppMsgRequest(self.request_token, None)
        if not self.follower_page : return
        if not self.follower_page.follower_info : return
        for follower_id in self.follower_page.follower_info.followers.keys():
            print follower_id
            send_request.to_fake_id = follower_id
            send_request.send(app_msg_id)
            print send_request.response_json

    def request_get_app_msgs_list(self):
        request = WechatGetAppMsgListRequest(self.request_token)
        request.open()
        return request.list

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

    def request_get_wechat_image_list(self):
        request = WechatGetImageListRequest(self.request_token)
        request.get()

    def request_get_wechat_ticket(self):
        request = WechatGetTicketRequest(self.request_token)
        print request.get_ticket()

    def is_login(self):
        return self.login_page and self.login_page.is_login()



# wechat = Wechat()
# wechat.username = 'bargetor_public@sina.com'
# wechat.password = 'lanqiao@mj'

# token = wechat.wechat_auto_login()
# wechat.request_user_setting_page()

# follower =  WechatFollowerPage(token)
# print follower.request_wechat_follower_page()
