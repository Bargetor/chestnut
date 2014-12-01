# -*- coding:utf-8 -*-
import selenium
from selenium import webdriver
import Exescript
import json
import urllib
import urllib2
import cookielib
import MultipartPostHandler
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

        request = self._build_request()
        if not request : return
        self.__set_headers(request)
        ret = urllib2.urlopen(request)
        self.content = ret.read()
        ret.close()


    def _build_request(self):
        if self.url is None : return None
        if self.params :
            # 如果不把 url 转化成 str 类型 那么在 httplib 827 行就会出现编码错误
            return urllib2.Request(str(self.url), urllib.urlencode(self.params))
        return urllib2.Request(self.url)


    def __set_headers(self, request):
        if request is None or self.headers is None: return
        for key,value in self.headers.items():
            request.add_header(key, value)

    def exe_js_not_in_content(self, js_str):
        if not js_str : return None
        browser = get_driver()

        exejs = Exescript.ExeJs(browser)
        exejs.exeWrap(js_str)
        result = exejs.getMsg()

        browser.close()
        return result

class WebUpLoadRequest(WebPage):
    """docstring for WebUpLoadRequest"""
    def __init__(self, url, params = None, headers = None):
        super(WebUpLoadRequest, self).__init__(url, params, headers)

        self.file_param_name = None
        slef.file_name = None

    def upload(self, file_param_name, file_name):
        self.file_param_name = file_param_name
        self.file_name = file_name

        self.__build_file_upload_params()
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(opener)

        self.open()

    def __build_file_upload_params(self):
        if self.params is None:
            self.params = dict()
        if self.file_param_name is None : return
        self.params[self.file_param_name] = open(self.file_name, 'rb')

driver_class_list = [webdriver.PhantomJS, webdriver.Chrome, webdriver.Firefox, webdriver.Safari,]

def get_driver():
    for driver_class in driver_class_list:
        try:
            return driver_class()
            break
        except Exception, e:
            print e
            continue

