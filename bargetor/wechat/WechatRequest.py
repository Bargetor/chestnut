# -*- coding: utf-8 -*-
import json
import random

from bargetor.common.web.WebPage import WebPage
from bargetor.wechat.Common import build_wechat_base_request_headers, build_wechat_base_request_params
from bargetor.common import HTMLUtil, ReUtil
from bargetor.common.JsonUtil import JsonObject

import logging
import traceback

log = logging.getLogger(__name__)


class WechatRequest(WebPage):
    """docstring for WechatRequest"""
    def __init__(self, url, params = None, headers = None):
        super(WechatRequest, self).__init__(url)

        self.response_json = None
        self.response_ret = 99999999
        self.response_msg = None

    def open(self, is_need_cookes = False):
        super(WechatRequest, self).open(is_need_cookes)

        self.response_json = json.loads(self.content)
        if not self.response_json : return
        self.response_ret = self.response_json['base_resp']['ret']
        self.response_msg = self.response_json['base_resp']['err_msg']

class WechatLoginRequest(WechatRequest):
    def __init__(self, username = None, password = None):
        self.url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
        super(WechatLoginRequest, self).__init__(self.url)

        self.username = username
        self.password = password
        self.request_token = None
        self.login_ret = 99999999

        self.setting_page = None
        self.follower_page = None

    def __build_home_page_header(self):
        headers = build_wechat_base_request_headers()
        headers['Accept-Encoding'] = 'gzip,deflate,sdch'
        headers['Content-Length'] = '79'
        headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN'
        self.headers = headers
        return headers

    def __build_request_param(self):
        paras = {'username':self.username, 'pwd':self.password, 'imgcode':'', 'f':'json'}
        self.params = paras
        return paras

    def login(self):

        if not self.username or not self.password: return

        self.__build_request_param()
        self.__build_home_page_header()

        self.open(True)
        self.__find_token()
        return self.request_token

    def __find_token(self):
        self.login_ret = self.response_ret
        if not self.is_login() : return None

        token = self.response_json['redirect_url'][44:]

        self.request_token = token
        return token

    def is_login(self):
        return self.login_ret == 0

class WechatGetFollowerInfoRequest(WechatRequest):
    """docstring for WechatFollowerInfoRequest"""
    def __init__(self, request_token, to_fake_id):
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/getcontactinfo?t=ajax-getcontactinfo&lang=zh_CN&fakeid=%s" % to_fake_id
        super(WechatGetFollowerInfoRequest, self).__init__(self.base_url)
        self.request_token = request_token

        self.follower_info = None

    def __build_get_follower_info_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize=10&pageidx=0&type=0&token=%s&lang=zh_CN" % self.request_token
        return headers

    def __build_get_follower_info_params(self):
        params = build_wechat_base_request_params()
        params['token'] = self.request_token
        params['json'] = '1'
        return params

    def get_info(self):
        self.headers = self.__build_get_follower_info_headers()
        self.params = self.__build_get_follower_info_params()

        self.open()
        self.follower_info = self.__process_response_info(self.content)
        return self.follower_info

    def __process_response_info(self, response_info):
        if not self.response_json : return None
        if self.response_ret != 0 : return None

        contact_info = self.response_json['contact_info']
        info = dict()
        info['fake_id'] = str(contact_info['fake_id'])
        info['nick_name'] = contact_info['nick_name']
        info['user_name'] = contact_info['user_name']
        info['signature'] = contact_info['signature']
        info['city'] = contact_info['city']
        info['province'] = contact_info['province']
        info['country'] = contact_info['country']
        info['gender'] = contact_info['gender']
        info['remark_name'] = contact_info['remark_name']
        info['group_id'] = str(contact_info['group_id'])
        return info


class WechatSingleSendRequest(WechatRequest):
    def __init__(self, request_token, to_fake_id):
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&f=json&lang=zh_CN"
        self.base_referer_url = "https://mp.weixin.qq.com/cgi-bin/singlesendpage?t=message/send&action=index&lang=zh_CN"
        self.url = "%s&token=%s" % (self.base_url, request_token)
        super(WechatSingleSendRequest, self).__init__(self.url)

        self.request_token = request_token
        self.to_fake_id = to_fake_id

    def send(self):
        self.headers = self._build_send_request_headers()
        self.params = self._build_send_request_params()

        self.open()

    def _build_send_request_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "%s&token=%s&tofakeid=%s" % (self.base_referer_url, self.request_token, self.to_fake_id)
        return headers

    def _build_send_request_params(self):
        params = build_wechat_base_request_params()
        params['token'] = self.request_token
        params['ajax'] = "1"
        params['tofakeid'] = self.to_fake_id
        params['imgcode'] = ''
        return params

class WechatSingleSendTextRequest(WechatSingleSendRequest):
    def __init__(self, request_token, to_fake_id):
        super(WechatSingleSendTextRequest, self).__init__(request_token, to_fake_id)

    def _build_send_request_params(self):
        params = super(WechatSingleSendTextRequest, self)._build_send_request_params()
        params['type'] = "1"
        params['content'] = "你好，该消息来自伟大的chestnut!"
        return params

class WechatMaterialUploadRequest(WechatRequest):
    """docstring for WechatMaterialUploadRequest"""
    def __init__(self, request_token, ticket):
        self.url = ''
        super(WechatMaterialUploadRequest, self).__init__(self.url)
        self.request_token = request_token
        self.ticket = ticket

