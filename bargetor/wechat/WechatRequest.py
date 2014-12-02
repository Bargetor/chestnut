#-*- coding: utf-8 -*-
import json
import random
import os
import urllib
import urllib2
import cookielib
import MultipartPostHandler

from bargetor.common.web.WebPage import WebPage
from bargetor.wechat.Common import build_wechat_base_request_headers, build_wechat_base_request_params
from bargetor.common import HTMLUtil, ReUtil, StringUtil
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

    def _on_open_url_after(self):
        super(WechatRequest, self)._on_open_url_after()
        self.response_json = json.loads(self.content)
        if not self.response_json : return
        self.response_ret = self.response_json['base_resp']['ret']
        self.response_msg = self.response_json['base_resp']['err_msg']

class WechatLoginRequest(WechatRequest):
    def __init__(self, username = None, password = None):
        self.url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
        super(WechatLoginRequest, self).__init__(self.url)
        self.is_need_cookes = True

        self.username = username
        self.password = password
        self.request_token = None
        self.login_ret = 99999999

        self.setting_page = None
        self.follower_page = None

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Accept-Encoding'] = 'gzip,deflate,sdch'
        headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN'
        return headers

    def _build_params(self):
        params = {'username':self.username, 'pwd':self.password, 'imgcode':'', 'f':'json'}
        return params

    def login(self):
        if not self.username or not self.password: return
        self.open()
        return self.request_token

    def _on_open_url_after(self):
        super(WechatLoginRequest, self)._on_open_url_after()
        self.__find_token()

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

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize=10&pageidx=0&type=0&token=%s&lang=zh_CN" % self.request_token
        return headers

    def _build_params(self):
        params = build_wechat_base_request_params()
        params['token'] = self.request_token
        params['json'] = '1'
        return params

    def get_info(self):
        self.open()
        return self.follower_info

    def _on_open_url_after(self):
        super(WechatGetFollowerInfoRequest, self)._on_open_url_after()
        self.follower_info = self.__process_response_info(self.content)

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
        self.open()

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "%s&token=%s&tofakeid=%s" % (self.base_referer_url, self.request_token, self.to_fake_id)
        return headers

    def _build_params(self):
        params = build_wechat_base_request_params()
        params['token'] = self.request_token
        params['ajax'] = "1"
        params['tofakeid'] = self.to_fake_id
        params['imgcode'] = ''
        return params

class WechatSingleSendTextRequest(WechatSingleSendRequest):
    def __init__(self, request_token, to_fake_id):
        super(WechatSingleSendTextRequest, self).__init__(request_token, to_fake_id)

    def _build_params(self):
        params = super(WechatSingleSendTextRequest, self)._build_params()
        params['type'] = "1"
        params['content'] = "该消息来自伟大的chestnut!"
        return params

class WechatMaterialUploadRequest(WechatRequest):
    """docstring for WechatMaterialUploadRequest"""
    def __init__(self, request_token, user_name, ticket):
        super(WechatMaterialUploadRequest, self).__init__(self.url)
        self.is_multipart_post = True
        self.request_token = request_token
        self.user_name = user_name
        self.ticket = ticket

        self.file_name = None

    def upload(self, file_name):

        if not file_name : return
        if not os.path.exists(file_name) : return
        self.file_name = file_name

        self.open()

    def _set_params(self, request, params):
        if request is None or params is None: return
        request.add_data(params)

    def _build_params(self):
        params = dict()
        file_name = os.path.basename(self.file_name)
        params['Filename'] = file_name
        params['folder'] = '/cgi-bin/uploads'
        params['Upload'] = 'Submit Query'
        params['file'] = open(self.file_name, 'rb')
        return params

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&t=media/img_list&lang=zh_CN&token=%s" % self.request_token
        return headers

class WechatImageMaterialUploadRequest(WechatMaterialUploadRequest):
    """docstring for WechatImageMaterialUploadRequest"""
    def __init__(self, request_token, user_name, ticket):
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload_material&f=json&writetype=doublewrite&groupid=1&lang=zh_CN"
        self.url = "%s&ticket_id=%s&ticket=%s&token=%s" % (self.base_url, user_name, ticket, request_token)
        super(WechatImageMaterialUploadRequest, self).__init__(request_token, user_name, ticket)

class WechatDevServerSettingRequest(WechatRequest):
    """docstring for WechatDevSettingRequest"""
    def __init__(self, request_token, operation_seq):
        self.base_url = "https://mp.weixin.qq.com/advanced/callbackprofile?t=ajax-response&lang=zh_CN"
        self.url = "%s&token=%s" % (self.base_url, request_token)
        super(WechatDevServerSettingRequest, self).__init__(self.url)
        self.request_token = request_token
        self.operation_seq = operation_seq

        self.server_url = None
        self.callback_token = None
        self.callback_encrypt_mode = "0"
        self.encoding_aeskey = StringUtil.get_random_str(43)

    def modify_setting(self, server_url, callback_token):
        if not server_url or not callback_token : return
        self.server_url = server_url
        self.callback_token = callback_token

        self.open()

    def _build_params(self):
        params = dict()
        params['url'] = self.server_url
        params['callback_token'] = self.callback_token
        params['encoding_aeskey'] = self.encoding_aeskey
        params['callback_encrypt_mode'] = self.callback_encrypt_mode
        params['operation_seq'] = self.operation_seq
        return params

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "https://mp.weixin.qq.com/advanced/advanced?action=interface&t=advanced/interface&lang=zh_CN&token=%s" % self.request_token
        return headers

