# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import json
import hashlib
import random
import xml.etree.ElementTree as ET
from bargetor.common.web.WebPage import WebPage

from bargetor.common import HTMLUtil, ReUtil
from bargetor.common.JsonUtil import JsonObject

import logging
import traceback

log = logging.getLogger(__name__)

class WechatFollowerPage(WebPage):
    """docstring for WechatFollowerPage"""
    def __init__(self, request_token):
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&type=0&lang=zh_CN&token=%s" % request_token
        super(WechatFollowerPage, self).__init__(self.base_url)
        self.request_token = request_token
        self.follower_info = self.WechatFollowerInfo()

        self.__build_follower_info()

        follower = self.follower_info.followers.get('1159047001')

        send_text_request = WechatSingleSendTextRequest(self.request_token, follower['fake_id'])
        send_text_request.send()

    def __build_follower_info(self):
        self.__process_follower_page(0)

        lost_page_count = self.follower_info.page_count - self.follower_info.current_page_index
        if lost_page_count <= 1 : return

        for x in xrange(1,lost_page_count):
            self.__process_follower_page(x)


    def __process_follower_page(self, follower_page_index = 0, follower_page_size = 10):
        self.__request_wechat_follower_page(follower_page_index, follower_page_size)
        self.follower_home_page_dom = HTMLUtil.build_html_dom_from_str(self.content)
        follower_info_json = self.__find_follower_info_json()
        self.__process_follower_info_json(follower_info_json)

    def __request_wechat_follower_page(self, follower_page_index = 0, follower_page_size = 10):
        if not self.request_token: return
        self.url = "%s&pagesize=%s&pageidx=%s" % (self.base_url, str(follower_page_size), str(follower_page_index))

        self.headers = self.__build_follower_page_reqeust_headers()
        self.open()

    def __build_follower_page_reqeust_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=' + self.request_token
        return headers

    def __find_follower_info_json(self):
        follower_info_javascript = self.__find_follower_info_javascript()

        if not follower_info_javascript : return
        follower_info_json_str = self.exe_js_not_in_content(follower_info_javascript)
        return json.loads(follower_info_json_str)

    def __find_follower_info_javascript(self):
        body = self.follower_home_page_dom.getElementsByTagName('body')[0];
        javascript_elements = body.getElementsByTagName('script')
        follower_info_javascript_element = javascript_elements[len(javascript_elements) - 1]
        follower_info_javascript = HTMLUtil.find_element_content(follower_info_javascript_element)
        if follower_info_javascript is None : return

        return self.__process_follower_info_js(follower_info_javascript)

    def __process_follower_info_js(self, follower_info_javascript):
        if not follower_info_javascript : return None
        js = follower_info_javascript
        js = str(js).replace('\n', '')
        js = js.replace(' ', '')

        js =  js.replace("""seajs.use('user/index',wx_main);;""", '')
        js = "(function(){var wx = {};%s return wx.cgiData;})()" % js
        return js

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
        self.url = "https://mp.weixin.qq.com/cgi-bin/settingpage?t=setting/index&action=index&lang=zh_CN&token=" +request_token
        super(WechatSettingPage, self).__init__(self.url)

        self.request_token = request_token

        self.__request_user_setting_page()
        self.dom = HTMLUtil.build_html_dom_from_str(self.content)

        self.account_info = self.AccountInfo()
        self.__init_account_info()

    def __init_account_info(self):
        self.__parse_account_info()
        log.info(self.account_info)


    def __request_user_setting_page(self):
        if not self.request_token: return

        self.headers = self.__build_setting_page_request_headers()
        self.open()

    def __build_setting_page_request_headers(self):
        headers = build_wechat_base_request_headers()
        headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=' + self.request_token
        return headers

    def __parse_account_info(self):
        if not self.dom: return
        account_info_element_list = HTMLUtil.find_html_element_list_for_tag(self.dom, 'li', 'account_setting_item')
        for element in account_info_element_list:
            account_info_item = self.__parse_account_info_item(element)
            self.__confirm_account_info(account_info_item)

    def __parse_account_info_item(self, element):
        item = {}
        name_element = HTMLUtil.find_html_element_list_for_tag(element, 'h4')[0]
        if not name_element: return item
        name = HTMLUtil.find_element_content(name_element)
        content_element = HTMLUtil.find_html_element_list_for_tag(element, 'div', 'meta_content')[0]
        if not content_element: return item
        content = HTMLUtil.find_element_content(content_element)
        item['name'] = name
        item['content'] = content
        return item

    def __confirm_account_info(self, account_info_item):
        name = account_info_item['name'].encode('utf-8')
        content = account_info_item['content']
        if content is not None:
            content = content.encode('utf-8')
        if not name: return
        if name == '名称':
            self.account_info.name = content
        if name == '头像':
            self.account_info.pic = content
        if name == '登录邮箱':
            self.account_info.account_name = content
        if name == '原始ID':
            self.account_info.wechat_default_id = content
        if name == '微信号':
            self.account_info.wechat_id = content
        if name == '类型':
            self.account_info.wechat_type = content
        if name == '认证情况':
            self.account_info.is_authenticate = content
        if name == '主体信息':
            self.account_info.owner_info = content
        if name == '介绍':
            self.account_info.description = content
        if name == '所在地址':
            self.account_info.address = content
        if name == '二维码':
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


class WechatLoginRequest(WebPage):
    def __init__(self,  username = None, password = None):
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
        response_json = json.loads(self.content)
        ret = response_json['base_resp']['ret']
        self.login_ret = ret
        if not self.is_login() : return None

        token = response_json['redirect_url'][44:]

        self.request_token = token
        return token

    def is_login(self):
        return self.login_ret == 0

class WechatSingleSendRequest(WebPage):
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
        params = dict()
        params['token'] = self.request_token
        params['lang'] = "zh_CN"
        params['f'] = "json"
        params['ajax'] = "1"
        params['random'] = str(random.random())
        params['tofakeid'] = self.to_fake_id
        params['imgcode'] = ''
        return params

class WechatSingleSendTextRequest(WechatSingleSendRequest):
    def __init__(self, request_token, to_fake_id):
        super(WechatSingleSendTextRequest, self).__init__(request_token, to_fake_id)

    def _build_send_request_params(self):
        params = super(WechatSingleSendTextRequest, self)._build_send_request_params()
        params['type'] = "1"
        params['content'] = "你好"
        return params

# *************************public method ********************************* #

def build_wechat_base_request_headers():
    headers = dict()

    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Host'] = 'mp.weixin.qq.com'
    headers['Origin'] = 'https://mp.weixin.qq.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    return headers
