# -*- coding:utf-8 -*-
import selenium
from selenium import webdriver
import Exescript
import os
import json
import urllib
import urllib2
import cookielib
import MultipartPostHandler
import json
import hashlib
import xml.etree.ElementTree as ET

from urlparse import urlsplit

from bargetor.common import ArrayUtil, StringUtil

class WebRequest(object):
    """docstring for WebRequest"""
    def __init__(self, url, params = None, headers = None):
        super(WebRequest, self).__init__()
        self.url = url
        self.params = params
        self.headers = headers

        self.is_need_cookes = False
        self.is_multipart_post = False
        self.is_file_down = False
        self.download_path = None
        self.download_file_name = None

        self.content = None

    def _prepare_request(self):
        headers = ArrayUtil.merged_dict(self.headers, self._build_headers())
        params = ArrayUtil.merged_dict(self.params, self._build_params())

        opener = self._build_opener()
        self._install_opener(opener)

        request = self._build_request()

        if not request : return
        self._set_headers(request, headers)
        self._set_params(request, params)

        return request

    def open(self):
        request = self._prepare_request()
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

    def _install_opener(self, opener):
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


class WebDownloadRequest(WebRequest):
    """docstring for WebDownloadRequest"""
    def __init__(self, url, params = None, headers = None):
        super(WebDownloadRequest, self).__init__(url, params, headers)

        self.block_sz = 8192
        self.file_ext = 'tmp'

        self.download_path = None
        self.download_file_name = None

    def open(self):
        if not self.download_path : return
        # 流程有所变更，重写此方法
        request = self._prepare_request()
        self._on_open_url_before()
        ret = urllib2.urlopen(request)
        self._save_file(ret)
        ret.close()
        self._on_open_url_after()

    def _save_file(self, response):
        file_name = self._get_file_name(response)
        full_file_name = "%s%s" % (self.download_path, file_name)
        f = open(full_file_name, 'wb')
        meta = response.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (full_file_name, file_size)
        file_size_dl = 0
        while True:
            buffer = response.read(self.block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()

    def _get_file_name(self, response):
        if self.download_file_name : return self.download_file_name
        content_disposition = response.info().getheaders('Content-Disposition')
        if content_disposition and content_disposition[0]:
            localName = content_disposition[0].split('filename=')[1]
            return localName
        url_file_name = url2name(self.url)
        if StringUtil.isNone(url_file_name) :
            url_file_name += "." + self.ext
        if not url_file_name : return StringUtil.get_random_str()
        return url_file_name



    def _on_open_url_before(self):
        super(WebDownloadRequest, self)._on_open_url_before()
        if not self.download_path : return
        if not os.path.isdir(self.download_path) : os.makedirs(self.download_path)


def url2name(url):
    if not url : return None
    url_split = urlsplit(url)
    if not url_split.path : return url_split.netloc
    return os.path.basename(url_split.path)

driver_class_list = [webdriver.PhantomJS, webdriver.Chrome, webdriver.Firefox, webdriver.Safari,]

def get_driver():
    for driver_class in driver_class_list:
        try:
            return driver_class()
            break
        except Exception, e:
            print e
            continue

