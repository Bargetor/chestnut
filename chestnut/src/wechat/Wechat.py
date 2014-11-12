# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import json
import hashlib
import xml.etree.ElementTree as ET

from common import HTMLUtil
from common.JsonUtil import JsonObject

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

        self.setting_page = None

    def wechat_auto_login(self):

        if not self.username or not self.password: return

        # 网页请求为了安全，以MD5加密密码
        # pwd = md5(self.password)
        pwd = self.password

        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        #login
        paras = {'username':self.username,'pwd':pwd,'imgcode':'','f':'json'}
        req = urllib2.Request('https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN', urllib.urlencode(paras))
        req.add_header('Accept','application/json, text/javascript, */*; q=0.01')
        req.add_header('Accept-Encoding','gzip,deflate,sdch')
        req.add_header('Accept-Language','zh-CN,zh;q=0.8')
        req.add_header('Connection','keep-alive')
        req.add_header('Content-Length','79')
        req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
        req.add_header('Host','mp.weixin.qq.com')
        req.add_header('Origin','https://mp.weixin.qq.com')
        req.add_header('Referer','https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36')
        req.add_header('X-Requested-With','XMLHttpRequest')
        ret = urllib2.urlopen(req)
        response = ret.read()
        ret.close()
        response_json = json.loads(response)

        token = response_json['redirect_url'][44:]

        self.request_token = token
        return token

    def request_user_setting_page(self):
        self.setting_page = WechatSettingPage(self.request_token)
        return self.setting_page

class WechatSettingPage(object):
    """docstring for WechatSettingPage"""
    def __init__(self, request_token):
        super(WechatSettingPage, self).__init__()
        self.request_token = request_token

        setting_page_html = self.__request_user_setting_page()
        self.dom = HTMLUtil.build_html_dom_from_str(setting_page_html)

        self.account_info = self.AccountInfo()
        self.__init_account_info()

    def __init_account_info(self):
        self.__parse_account_info()
        log.info(self.account_info)


    def __request_user_setting_page(self):
        if not self.request_token: return
        url = "https://mp.weixin.qq.com/cgi-bin/settingpage?t=setting/index&action=index&lang=zh_CN&token=" + self.request_token
        req = urllib2.Request(url)
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        # req.add_header('Accept-Encoding','gzip,deflate,sdch')
        req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')
        req.add_header('Connection','keep-alive')
        req.add_header('Host','mp.weixin.qq.com')
        req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
        req.add_header('Origin','https://mp.weixin.qq.com')
        req.add_header('Referer','https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=' + self.request_token)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36')
        ret = urllib2.urlopen(req)
        response = ret.read()
        ret.close()

        return response

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
            self.account_info.wechat_defualt_id = content
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
            self.wechat_defualt_id = None
            self.wechat_id = None
            self.wechat_type = None
            self.description = None
            self.owner_info = None
            self.is_authenticate = False
            self.address = None
            self.qs_code = None

        def __str__(self):
            return 'name:%s pic:%s account_name:%s wechat_defualt_id:%s wechat_id:%s wechat_type:%s description:%s owner_info:%s is_authenticate:%s address:%s  qs_code:%s' % (self.name, self.pic, self.account_name, self.wechat_defualt_id, self.wechat_id, self.wechat_type, self.description, self.owner_info, self.is_authenticate, self.address, self.qs_code)

        def __unicode__(self):
            return self.__str__()

        def get_json_str(self):
            try:
                return JsonObject(self.__dict__).get_json_str()
            except Exception, e:
                exstr = traceback.format_exc()
                log.error(exstr)



def md5(string):
    md5 = hashlib.md5()
    md5.update(string)
    md5_str = md5.hexdigest()
    return md5_str


# wechat = Wechat()
# wechat.username = 'bargetor_public@sina.com'
# wechat.password = 'lanqiao@mj'

# token = wechat.wechat_auto_login()
# wechat.request_user_setting_page()
