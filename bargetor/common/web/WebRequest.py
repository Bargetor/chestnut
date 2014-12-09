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

from bargetor.common import ArrayUtil

class WebRequest(object):
    """docstring for WebRequest"""
    def __init__(self, url, params = None, headers = None):
        super(WebRequest, self).__init__()
        self.url = url
        self.params = params
        self.headers = headers

        self.is_need_cookes = False
        self.is_multipart_post = False

        self.content = None

    def open(self):
        headers = ArrayUtil.merged_dict(self.headers, self._build_headers())
        params = ArrayUtil.merged_dict(self.params, self._build_params())

        opener = self._build_opener()
        self.__install_opener(opener)

        request = self._build_request()

        if not request : return
        self._set_headers(request, headers)
        self._set_params(request, params)

        self._on_open_url_before()
        ret = urllib2.urlopen(request)
        self.content = ret.read()
        ret.close()
        self._on_open_url_after()

    def _build_headers(self):
        return None

    def _build_params(self):
        return None

    def _build_opener(self):
        handlers = []

        if self.is_need_cookes :
            cj = cookielib.LWPCookieJar()
            cookes_handler = urllib2.HTTPCookieProcessor(cj)
            handlers.append(cookes_handler)

        if self.is_multipart_post :
            handlers.append(MultipartPostHandler.MultipartPostHandler)

        if len(handlers) > 0 :
            return urllib2.build_opener(*handlers)
        return None

    def __install_opener(self, opener):
        if not opener : return
        urllib2.install_opener(opener)

    def _build_request(self):
        if self.url is None : return None
        return urllib2.Request(str(self.url))


    def _set_headers(self, request, headers):
        if request is None or headers is None: return
        for key,value in headers.items():
            request.add_header(key, value)

    def _set_params(self, request, params):
        if request is None or params is None: return
        request.add_data(urllib.urlencode(params))

    def _on_open_url_before(self):
        pass

    def _on_open_url_after(self):
        pass

    def exe_js_not_in_content(self, js_str):
        if not js_str : return None
        browser = get_driver()

        exejs = Exescript.ExeJs(browser)
        exejs.exeWrap(js_str)
        result = exejs.getMsg()

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

