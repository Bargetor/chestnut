# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
import Exescript
import json
import urllib
import urllib2
import cookielib
import json
import hashlib
import xml.etree.ElementTree as ET

class WebPage(object):
    """docstring for WebPage"""
    def __init__(self, url, params = None, headers = None):
        super(WebPage, self).__init__()
        self.url = url
        self.params = params
        self.headers = headers

        self.content = None

    def open(self, is_need_cookes = False):
        if is_need_cookes:
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        request = self.__build_request()
        if not request : return
        self.__set_headers(request)
        ret = urllib2.urlopen(request)
        self.content = ret.read()
        ret.close()


    def __build_request(self):
        if self.url is None : return None
        if self.params :
            return urllib2.Request(self.url, urllib.urlencode(self.params))
        return urllib2.Request(self.url)

    def _build_headers(self):
        return None

    def _build_parmas(self):
        return None

    def __set_headers(self, request):
        if request is None or self.headers is None: return
        for key,value in self.headers.items():
            request.add_header(key, value)

    def exe_js_not_in_content(self, js_str):
        if not js_str : return None
        browser = get_driver()

        exejs = Exescript.ExeJs(browser)
        exejs.exeWrap(js_str)
        result = exejs.getMsg().encode('utf-8')

        browser.close()
        return result

driver_class_list = [webdriver.PhantomJS, webdriver.Chrome, webdriver.Firefox, webdriver.Safari,]

def get_driver():
    for driver_class in driver_class_list:
        try:
            return driver_class()
            break
        except Exception, e:
            print e
            continue


# class WechatLoginTest(WebPage):
#     def __init__(self,  username = None, password = None):
#         self.url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
#         super(WechatLoginTest, self).__init__(self.url, params = None, headers = None)

#         self.username = username
#         self.password = password
#         self.request_token = None
#         self.login_ret = 99999999

#         self.setting_page = None
#         self.follower_page = None

#     def __build_home_page_header(self):
#         headers = dict()

#         headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
#         headers['Accept-Encoding'] = 'gzip,deflate,sdch'
#         headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
#         headers['Connection'] = 'keep-alive'
#         headers['Content-Length'] = '79'
#         headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
#         headers['Host'] = 'mp.weixin.qq.com'
#         headers['Origin'] = 'https://mp.weixin.qq.com'
#         headers['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN'
#         headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
#         headers['X-Requested-With'] = 'XMLHttpRequest'

#         self.headers = headers
#         return headers

#     def __build_request_param(self):
#         pwd = md5(self.password)
#         paras = {'username':self.username,'pwd':pwd,'imgcode':'','f':'json'}
#         self.params = paras
#         return paras

#     def wechat_auto_login(self):

#         if not self.username or not self.password: return

#         self.__build_request_param()
#         self.__build_home_page_header()

#         self.open(True)

#         response_json = json.loads(self.content)
#         ret = response_json['base_resp']['ret']
#         self.login_ret = ret
#         if not self.is_login() : return

#         token = response_json['redirect_url'][44:]

#         self.request_token = token
#         return token

#     def is_login(self):
#         return self.login_ret == 0

# def md5(string):
#     md5 = hashlib.md5()
#     md5.update(string)
#     md5_str = md5.hexdigest()
#     return md5_str

# wechat = WechatLoginTest('bargetor_public@sina.com', 'lanqiao@mj')
# print wechat.wechat_auto_login()



# browser = get_driver()


# script = """(function(){
#                        var wx = {};
#                        wx.cgiData={
#         isVerifyOn: "0"*1,
#         pageIdx : 0,
#             pageCount : 2,
#             pageSize : 10,
#             groupsList : ({"groups":[{"id":0,"name":"未分组","cnt":14},{"id":1,"name":"黑名单","cnt":0},{"id":2,"name":"星标组","cnt":0}]}).groups,
#                         friendsList : ({"contacts":[{"id":1269538680,"nick_name":"设计师Milk","remark_name":"","group_id":0},{"id":1012287535,"nick_name":"MI_Sunnywang","remark_name":"","group_id":0},{"id":1224124520,"nick_name":"娜娜","remark_name":"","group_id":0},{"id":1421696461,"nick_name":"三分之一理想","remark_name":"","group_id":0},{"id":1159047001,"nick_name":"蓝桥","remark_name":"","group_id":0},{"id":978392661,"nick_name":"青青","remark_name":"","group_id":0},{"id":975727223,"nick_name":"lip","remark_name":"","group_id":0},{"id":671434682,"nick_name":"Labber","remark_name":"","group_id":0},{"id":26285015,"nick_name":"Vlaminck","remark_name":"","group_id":0},{"id":161762635,"nick_name":"x z","remark_name":"","group_id":0}]}).contacts,
#                                     currentGroupId : '',
#                         type : "0" * 1 || 0,
#             userRole : '1' * 1,
#             verifyMsgCount : '0' * 1,
#             totalCount : '14' * 1
#     };
#     return wx.cgiData;
#     })()"""

# exejs = Exescript.ExeJs(browser)
# exejs.exeWrap(script)
# data_json_str = exejs.getMsg().encode('utf-8')

# print json.loads(str(data_json_str))



# browser.close()
