# -*- coding: utf-8 -*-
import json
import re
import os
from bargetor.common.web.WebPage import WebPage
from bargetor.wechat.Common import build_wechat_base_request_headers, build_wechat_base_request_params
from bargetor.wechat.WechatRequest import *

from bargetor.common import HTMLUtil, ReUtil
from bargetor.common.JsonUtil import JsonObject

import logging
import traceback

log = logging.getLogger(__name__)


class WechatCGIDataPage(WebPage):
    """docstring for WechatRequest"""
    def __init__(self, url):
        super(WechatCGIDataPage, self).__init__(url)
        self.cgi_data = None

    def _on_open_url_after(self):
        self.cgi_data = self._process_cgi_data()

    def _process_cgi_data(self):
        js = self._find_cgi_data_javascript()
        js = self._format_cgi_data_javascript(js)
        if not js : return None
        cgi_data_json = self.exe_js_not_in_content(js)
        if cgi_data_json:
            cgi_data_json = cgi_data_json.replace('\t', '')
            return json.loads(cgi_data_json)
        return None

    def _find_cgi_data_javascript(self):
        results = re.findall(r'wx\.cgiData[^;]+};', self.content)
        if not results : return
        return results[0]

    def _format_cgi_data_javascript(self, js):
        return "var wx = {}; %s ; return wx.cgiData;" % js



class WechatFollowerPage(WechatCGIDataPage):
    """docstring for WechatFollowerPage"""
    def __init__(self, request_token):
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&type=0&lang=zh_CN&token=%s" % request_token
        super(WechatFollowerPage, self).__init__(self.base_url)
        self.request_token = request_token
        self.follower_info = self.WechatFollowerInfo()

    def find_all_followers(self):
        self.__build_follower_info()

        print self.follower_info.followers

        follower = self.follower_info.followers.get('1159047001')

        send_text_request = WechatSingleSendTextRequest(self.request_token, follower['fake_id'])
        send_text_request.send()

        get_follower_info_reqeust = WechatGetFollowerInfoRequest(self.request_token, follower['fake_id'])
        print get_follower_info_reqeust.get_info()

    def __build_follower_info(self):
        self.__process_follower_page(0)

        lost_page_count = self.follower_info.page_count - self.follower_info.current_page_index
        if lost_page_count <= 1 : return

        for x in xrange(1,lost_page_count):
            self.__process_follower_page(x)


    def __process_follower_page(self, follower_page_index = 0, follower_page_size = 10):
        self.__request_wechat_follower_page(follower_page_index, follower_page_size)
        self.__process_follower_info_json(self.cgi_data)

    def __request_wechat_follower_page(self, follower_page_index = 0, follower_page_size = 10):
        if not self.request_token: return
        self.url = "%s&pagesize=%s&pageidx=%s" % (self.base_url, str(follower_page_size), str(follower_page_index))

        self.open()

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=' + self.request_token
        return headers

    def __process_follower_info_json(self, follower_info_json):
        if not follower_info_json : return

        self.follower_info.total_count = int(follower_info_json.get('totalCount'))
        self.follower_info.page_count = int(follower_info_json.get('pageCount'))
        self.follower_info.current_page_index = int(follower_info_json.get('pageIdx'))

        self.__process_follower_groups_info(follower_info_json)
        self.__process_follower_list_info(follower_info_json)


    def __process_follower_groups_info(self, follower_info_json):
        # 因为每次处理都会有分组数据，故只处理一次
        if len(self.follower_info.groups.values()) > 0 : return
        groups_json = follower_info_json.get('groupsList')
        if not groups_json : return
        for key, value in groups_json.items():
            group = dict()
            group['id'] = value.get('id')
            group['name'] = value.get('name')
            group['follower_count'] = int(value.get('cnt'))
            self.follower_info.groups[group['id']] = group

    def __process_follower_list_info(self, follower_info_json):
        followers_json = follower_info_json.get('friendsList')
        if not followers_json : return
        for key, value in followers_json.items():
            follower = dict()
            follower['fake_id'] = value.get('id')
            follower['nick_name'] = value.get('nick_name')
            follower['remark_name'] = value.get('remark_name')
            follower['group_id'] = value.get('nick_name')
            self.follower_info.followers[follower['fake_id']] = follower


    class WechatFollowerInfo(object):
        """docstring for WecahtFollowerInfo"""
        def __init__(self):
            self.total_count = 0
            self.page_count = 0
            self.current_page_index = 0
            self.groups = dict()
            #为了排重，以ID为key
            self.followers = dict()


class WechatSettingPage(WebPage):
    """docstring for WechatSettingPage"""
    def __init__(self, request_token):
        self.url = "https://mp.weixin.qq.com/cgi-bin/settingpage?t=setting/index&action=index&lang=zh_CN&token=%s" % request_token
        super(WechatSettingPage, self).__init__(self.url)

        self.request_token = request_token

    def _on_open_url_after(self):
        self.dom = HTMLUtil.build_html_dom_from_str(self.content)
        self.account_info = self.AccountInfo()
        self.__init_account_info()

    def __init_account_info(self):
        self.__parse_account_info()
        log.info(self.account_info)


    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=' + self.request_token
        return headers

    def __parse_account_info(self):
        if not self.dom: return
        account_info_element_list = HTMLUtil.find_html_element_list_for_tag(self.dom, 'li', 'account_setting_item')
        for element in account_info_element_list:
            name, content = self.__parse_account_info_item(element)
            self.__confirm_account_info(name, content)

    def __parse_account_info_item(self, element):
        name_element = HTMLUtil.find_html_element_list_for_tag(element, 'h4')[0]
        if not name_element: return item
        name = HTMLUtil.find_element_content(name_element)
        content_element = HTMLUtil.find_html_element_list_for_tag(element, 'div', 'meta_content')[0]
        if not content_element: return item
        content = HTMLUtil.find_element_content(content_element)
        return name, content

    def __confirm_account_info(self, name, content):
        if not name: return
        if name == u'名称':
            self.account_info.name = content
        if name == u'头像':
            self.account_info.pic = content
        if name == u'登录邮箱':
            self.account_info.account_name = content
        if name == u'原始ID':
            self.account_info.wechat_default_id = content
        if name == u'微信号':
            self.account_info.wechat_id = content
        if name == u'类型':
            self.account_info.wechat_type = content
        if name == u'认证情况':
            self.account_info.is_authenticate = content
        if name == u'主体信息':
            self.account_info.owner_info = content
        if name == u'介绍':
            self.account_info.description = content
        if name == u'所在地址':
            self.account_info.address = content
        if name == u'二维码':
            self.account_info.qs_code = content

    class AccountInfo(object):
        """docstring for AccountInfo"""
        def __init__(self):
            self.name = None
            self.pic = None
            self.account_name = None
            self.wechat_default_id = None
            self.wechat_id = None
            self.wechat_type = None
            self.description = None
            self.owner_info = None
            self.is_authenticate = False
            self.address = None
            self.qs_code = None

        def __str__(self):
            return 'name:%s pic:%s account_name:%s wechat_default_id:%s wechat_id:%s wechat_type:%s description:%s owner_info:%s is_authenticate:%s address:%s  qs_code:%s' % (self.name, self.pic, self.account_name, self.wechat_default_id, self.wechat_id, self.wechat_type, self.description, self.owner_info, self.is_authenticate, self.address, self.qs_code)

        def __unicode__(self):
            return self.__str__()

        def get_json_str(self):
            try:
                return JsonObject(self.__dict__).get_json_str()
            except Exception, e:
                exstr = traceback.format_exc()
                log.error(exstr)


class WechatMaterialPage(WechatCGIDataPage):
    """docstring for WechatMaterialPage"""
    def __init__(self, url, request_token):
        super(WechatMaterialPage, self).__init__(url)

        self.request_token = request_token
        self.ticket = None
        self.uin = None
        self.uin_base64 = None
        self.user_name = None
        self.nick_name = None

    def open(self):

        super(WechatMaterialPage, self).open()
        self._process_material_params()

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "https://mp.weixin.qq.com/cgi-bin/appmsg?begin=0&count=10&t=media/appmsg_list&type=10&action=list&lang=zh_CN&token=%s" % self.request_token
        return headers

    def _process_material_params(self):
        params_javascript = self._find_material_params_javascript()
        format_parasm_javascript = self._format_material_params_javascript(params_javascript)
        params_json_str = self.exe_js_not_in_content(format_parasm_javascript)
        params_json = json.loads(params_json_str)

        if not params_json : return None
        data = params_json.get('data')

        self.ticket = data.get('ticket')
        self.uin = data.get('uin')
        self.uin_base64 = data.get('uin_base64')
        self.user_name = data.get('user_name')
        self.nick_name = data.get('nick_name')

    def _find_material_params_javascript(self):
        results = re.findall(r'window\.wx[^;]+};', self.content)
        if not results : return
        return results[0]

    def _format_material_params_javascript(self, js):
        if not js : return None
        return '%s; return window.wx;' % js

class WecahtImageMaterialPage(WechatMaterialPage):
    """docstring for WecahtImageMaterialPage"""
    def __init__(self, request_token):
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&t=media/img_list&lang=zh_CN"
        self.url = "%s&token=%s" % (self.base_url, request_token)
        super(WecahtImageMaterialPage, self).__init__(self.url, request_token)

        self.file_count = 0
        self.file_list = dict()

    def _on_open_url_after(self):
        super(WecahtImageMaterialPage, self)._on_open_url_after()
        self.__build_file_data()

    def upload(self, file_name):
        if not self.user_name or not self.ticket : return

        upload_request = WechatImageMaterialUploadRequest(self.request_token, self.user_name, self.ticket)
        upload_request.upload(file_name)
        print upload_request.response_json

    def __build_file_data(self):
        if self.cgi_data is None : return
        self.file_count = int(self.cgi_data.get('page').get('file_cnt').get('img_cnt'))
        file_items = self.cgi_data.get('page').get('file_item')
        for key,value in file_items.items():
            f = dict()
            f['file_id'] = value['file_id']
            f['file_name'] = value['name']
            f['update_time'] = value['update_time']
            f['cdn_url'] = value['cdn_url']
            self.file_list[f['file_id']] = f


class WechatDevSettingPage(WechatCGIDataPage):
    """docstring for WechatDevSettingPage"""
    def __init__(self, request_token):
        self.base_url = "https://mp.weixin.qq.com/advanced/advanced?action=dev&t=advanced/dev&lang=zh_CN"
        self.url = "%s&token=%s" % (self.base_url, request_token)
        super(WechatDevSettingPage, self).__init__(self.url)
        self.request_token = request_token

        self.operation_seq = None

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = "https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s" % self.request_token
        return headers

    def _on_open_url_after(self):
        super(WechatDevSettingPage, self)._on_open_url_after()
        if not self.cgi_data : return
        self.operation_seq = self.cgi_data.get('operation_seq')

    def modify_server_setting(self, server_url, callback_token):
        if not server_url or not callback_token : return
        modify_server_setting_request = WechatDevServerSettingRequest(self.request_token, self.operation_seq)
        modify_server_setting_request.modify_setting(server_url, callback_token)

        print modify_server_setting_request.response_json
