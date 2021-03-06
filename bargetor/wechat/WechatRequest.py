#-*- coding: utf-8 -*-
import json
import time
import random
import os
import urllib
import urllib2
import cookielib
import MultipartPostHandler

from bargetor.common.web.WebRequest import WebRequest
from bargetor.wechat.Common import build_wechat_base_request_headers, build_wechat_base_request_params
from bargetor.wechat.WechatModel import *
from bargetor.common import HTMLUtil, ReUtil, StringUtil, ArrayUtil
from bargetor.common.JsonUtil import JsonObject

import logging
import traceback

log = logging.getLogger(__name__)

class WechatRequest(WebRequest):
    """docstring for WechatRequest"""
    def __init__(self, request_token):
        super(WechatRequest, self).__init__(None)
        self.request_token = request_token

        self.base_url = None
        self.url = self.base_url
        self.referer_url = None

    def open(self):
        self.__set_header_referer()
        self.url = self._build_url()
        self.__add_url_request_token()
        super(WechatRequest, self).open()

    def __add_url_request_token(self):
        if not self.url : return
        if not self.request_token : return
        self.url = "%s&token=%s" % (self.url, self.request_token)

    def _build_url(self):
        return self.base_url

    def _build_header_referer(self):
        if not self.referer_url : return None
        if not self.request_token : return self.referer_url
        return "%s&token=%s" % (self.referer_url, self.request_token)

    def __set_header_referer(self):
        header = dict()
        referer_url = self._build_header_referer()
        if not referer_url : return
        header['Referer'] = referer_url
        self.headers = ArrayUtil.merged_dict(self.headers, header)

    def _build_headers(self):
        headers = build_wechat_base_request_headers()
        return headers



class WechatDataRequest(WechatRequest):
    """docstring for WechatDataRequest"""
    def __init__(self, request_token):
        super(WechatDataRequest, self).__init__(request_token)

        self.response_json = None
        self.response_ret = 99999999
        self.response_msg = None

    def _on_open_url_after(self):
        super(WechatDataRequest, self)._on_open_url_after()
        self.response_json = json.loads(self.content)
        if not self.response_json : return
        if self.response_json.get('base_resp'):
            self.response_ret = self.response_json.get('base_resp').get('ret')
            self.response_msg = self.response_json.get('base_resp').get('err_msg')
            return
        if self.response_json.get('msg') and self.response_json.get('ret'):
            self.response_msg = self.response_json.get('msg')
            self.response_ret = self.response_json.get('ret')
            return

class WechatLoginRequest(WechatDataRequest):
    def __init__(self, username = None, password = None):
        super(WechatLoginRequest, self).__init__(None)
        self.base_url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN"
        self.is_need_cookes = True

        self.username = username
        self.password = password
        self.request_token = None
        self.login_ret = 99999999

        self.setting_page = None
        self.follower_page = None

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
        print token
        return token

    def is_login(self):
        return self.login_ret == 0

class WechatGetFollowerInfoRequest(WechatDataRequest):
    """docstring for WechatFollowerInfoRequest"""
    def __init__(self, request_token, to_fake_id):
        super(WechatGetFollowerInfoRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/getcontactinfo?t=ajax-getcontactinfo&lang=zh_CN&fakeid=%s" % to_fake_id

        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&pagesize=10&pageidx=0&type=0&lang=zh_CN"
        self.follower_info = None

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


class WechatSingleSendRequest(WechatDataRequest):
    def __init__(self, request_token, to_fake_id):
        super(WechatSingleSendRequest, self).__init__(request_token)

        self.base_url = "https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&f=json&lang=zh_CN"
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/singlesendpage?t=message/send&action=index&lang=zh_CN"

        self.to_fake_id = to_fake_id

    def send(self):
        self.open()


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

        self.content = None

    def send(self, content):
        if not content : return
        self.content = content
        self.open()

    def _build_params(self):
        params = super(WechatSingleSendTextRequest, self)._build_params()
        params['type'] = "1"
        params['content'] = self.content
        return params

class WechatSingleSendAppMsgRequest(WechatSingleSendRequest):
    def __init__(self, request_token, to_fake_id):
        super(WechatSingleSendAppMsgRequest, self).__init__(request_token, to_fake_id)

        self.app_msg_id = None

    def send(self, app_msg_id):
        if not app_msg_id : return
        self.app_msg_id = app_msg_id
        self.open()

    def _build_params(self):
        params = super(WechatSingleSendAppMsgRequest, self)._build_params()
        params['type'] = "10"
        params['app_id'] = self.app_msg_id
        params['appmsgid'] = self.app_msg_id
        return params

class WechatMaterialUploadRequest(WechatDataRequest):
    """docstring for WechatMaterialUploadRequest"""
    def __init__(self, request_token, user_name, ticket):
        super(WechatMaterialUploadRequest, self).__init__(request_token)

        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&t=media/img_list&lang=zh_CN"

        self.is_multipart_post = True
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

class WechatImageMaterialUploadRequest(WechatMaterialUploadRequest):
    """docstring for WechatImageMaterialUploadRequest"""
    def __init__(self, request_token, user_name, ticket):
        super(WechatImageMaterialUploadRequest, self).__init__(request_token, user_name, ticket)
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload_material&f=json&writetype=doublewrite&groupid=1&lang=zh_CN"

    def _build_url():
        url = self.url = "%s&ticket_id=%s&ticket=%s" % (self.base_url, user_name, ticket)
        return url

class WechatGetMaterialListDataRequest(WechatDataRequest):
    """docstring for WechatGetMaterialListDataRequest"""
    def __init__(self, request_token):
        super(WechatGetMaterialListDataRequest, self).__init__(request_token)

        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN"

        self.begin = 0
        self.count = 10
        self.total_count = -1
        self.list = []

    def get(self):
        self.__request()

        last = self.begin + self.count
        while  last < self.total_count and self.total_count > 0:
            self.__request(last)
            last += self.count

    def __request(self, begin = 0):
        self.begin = begin
        self.url = self._build_url()
        self.open()

    def _get_data(self):
        return None


    def _get_list_total(self):
        return -1


    def _on_open_url_after(self):
        super(WechatGetMaterialListDataRequest, self)._on_open_url_after()
        self.total_count = self._get_list_total()
        data = self._get_data()
        if isinstance(data, list):
            self.list += data


    def _build_url(self):
        url = "%s&token=%s&begin=%s&count=%s" % (self.base_url, self.request_token, str(self.begin), str(self.count))
        return url



class WechatGetImageListRequest(WechatGetMaterialListDataRequest):
    """docstring for WechatGetImageListRequest"""
    def __init__(self, request_token):
        super(WechatGetImageListRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/filepage?1=1&lang=zh_CN&lang=zh_CN&f=json&ajax=1&random=0.314140283735469&group_id=1&type=2"

    def _get_data(self):
        datas = []
        page_info = self.response_json.get('page_info')
        if not page_info : return datas
        datas_json = page_info.get('file_item')
        if not datas_json : return datas
        for item in datas_json:
            img = self.__parse_data_item(item)
            datas.append(img)
        return datas


    def __parse_data_item(self, item):
        img = WechatImage()
        img.file_id = item['file_id']
        img.file_name = item['name']
        img.update_time = item['update_time']
        img.cdn_url = item['cdn_url']
        return img



    def _get_list_total(self):
        page_info = self.response_json.get('page_info')
        if not page_info : return -1
        file_cnt = page_info.get('file_cnt')
        if not file_cnt : return -1
        img_cnt = file_cnt.get('img_cnt')
        if not img_cnt : return -1
        return img_cnt


class WechatGetAppMsgListRequest(WechatGetMaterialListDataRequest):
    """docstring for WechatGetPhotoNewsListRequest"""
    def __init__(self, request_token):
        super(WechatGetAppMsgListRequest, self).__init__(self.base_url)
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/appmsg?type=10&action=list&f=json&lang=zh_CN&lang=zh_CN&f=json&ajax=1"
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&t=media/img_list&lang=zh_CN"

    def _get_data(self):
        return self.__process_app_msg_info()

    def _get_list_total(self):
        page_info = self.response_json.get('app_msg_info')
        if not page_info : return -1
        file_cnt = page_info.get('file_cnt')
        if not file_cnt : return -1
        cnt = file_cnt.get('app_msg_cnt')
        if not cnt : return -1
        return cnt

    def _on_open_url_after(self):
        super(WechatGetAppMsgListRequest, self)._on_open_url_after()
        self.__process_app_msg_info()

    def __process_app_msg_info(self):
        if not self.response_json : return
        app_msg_info = self.response_json.get('app_msg_info')
        if not app_msg_info : return
        app_msgs = self.__build_app_msgs(app_msg_info)
        return app_msgs

    def __build_app_msgs(self, app_msg_info):
        app_msgs = []
        item = app_msg_info.get('item')
        if not item : return app_msgs
        for info in item:
            app_msgs.append(self.__build_app_msg(info))
        return app_msgs

    def __build_app_msg(self, app_msg_info):
        app_msg = WechatAppMsg()
        app_msg.app_msg_id = app_msg_info.get('app_id')
        app_msg.create_time = long(app_msg_info.get('create_time'))
        app_msg.update_time = long(app_msg_info.get('update_time'))
        app_msg.items = self.__build_app_msg_items(app_msg_info)
        return app_msg

    def __build_app_msg_items(self, app_msg_info):
        items = []
        multi_items = app_msg_info.get('multi_item')
        if not multi_items : return items
        for item in multi_items:
            app_msg_item = WechatAppMsgItem()
            app_msg_item.title = item.get('title')
            app_msg_item.show_cover_pic = item.get('show_cover_pic')
            app_msg_item.author = item.get('author')
            app_msg_item.content_url = item.get('content_url')
            app_msg_item.img_url = item.get('cover')
            app_msg_item.source_url = item.get('source_url')
            app_msg_item.file_id = item.get('file_id')
            app_msg_item.digest = item.get('digest')
            app_msg_item.seq = item.get('seq')

            items.append(app_msg_item)
        return items




class WechatAppMsgProcessRequest(WechatDataRequest):
    """docstring for WechatPhotoNewsAddRequest, for wechat app msg create or update"""
    CREATE_METHOD = 'create'
    UPDATE_METHOD = 'update'

    def __init__(self, request_token):
        super(WechatAppMsgProcessRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&type=10&lang=zh_CN"
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN"
        self.app_msg = WechatAppMsg()
        # 你问我这里为什么要记录发送和响应时间？我只能告诉你，狗日的微信没有返回图文ID，奶奶的腿
        self.request_send_time = 9999999999
        self.request_response_time = -1

    def add_app_msg_item_by_info(self, title, content, file_id, author = None, source_url = None):
        self.app_msg.add_app_msg_item_by_info(title, content, file_id, author, source_url)

    def add_app_msg_item(self, app_msg_item):
        self.app_msg.add_app_msg_item(app_msg_item)

    def add_app_msg_items(self, app_msg_items):
        self.app_msg.add_app_msg_items(app_msg_items)

    def remove_item_by_index(self, index):
        self.app_msg.remove_item_by_index(index)

    def remove_item_by_seq(self, seq):
        self.app_msg.remove_item_by_seq(seq)

    def remove_all_items(self):
        self.app_msg.remove_all_items()

    def create(self, app_msg_items = None):
        if app_msg_items :
            self.add_app_msg_items(app_msg_items)
        self.url = self.base_url + "&sub=%s" % self.CREATE_METHOD

        self.open()

    def update(self):
        self.url = self.base_url + "&sub=%s" % self.UPDATE_METHOD

        self.open()

    def _on_open_url_before(self):
        self.request_send_time = long(time.time())

    def _on_open_url_after(self):
        self.request_response_time = long(time.time())
        super(WechatAppMsgProcessRequest, self)._on_open_url_after()


    def _build_params(self):
        params = build_wechat_base_request_params()
        params['ajax'] = '1'
        params['token'] = self.request_token
        params['AppMsgId'] = self.app_msg.app_msg_id
        params['vid'] = ''
        params = self.__build_app_msg_process_params(params, self.app_msg.items)
        print params
        return params

    def __build_app_msg_process_params(self, base_params, app_msg_items):
        params = dict()
        if not app_msg_items : return base_params
        for i in xrange(len(app_msg_items)):
            app_msg_item = app_msg_items[i]
            if not app_msg_item.title or not app_msg_item.content or not app_msg_item.file_id : continue

            params['title' + str(i)] = app_msg_item.title
            params['content' + str(i)] = app_msg_item.content
            params['digest' + str(i)] = app_msg_item.digest
            params['author' + str(i)] = app_msg_item.author
            params['fileid' + str(i)] = app_msg_item.file_id
            show_cover_pic = None
            if app_msg_item.show_cover_pic :
                show_cover_pic = '1'
            else:
                show_cover_pic = '0'
            params['show_cover_pic' + str(i)] = show_cover_pic
            params['source_url' + str(i)] = app_msg_item.source_url

        params['count'] = str(len(app_msg_items))
        return ArrayUtil.merged_dict(base_params, params)

class WechatAppMsgCreateRequest(WechatDataRequest):
    """docstring for WechatAppMsgCreateRequest
    由于微信在创建图文信息时没有返回图文ID，故这个类是一个讨巧方式的存在
    先以标题为一随机数创建，再取图文列表，找到该随机数，再修改"""
    def __init__(self, request_token):
        super(WechatAppMsgCreateRequest, self).__init__(None)

        self.request_token = request_token
        self.process = WechatAppMsgProcessRequest(request_token)
        self.random_title = StringUtil.get_random_str()
        self.app_msg_id = None

    def __build_random_app_msg(self):
        random_app_msg = WechatAppMsg()
        random_app_msg.add_app_msg_item_by_info(self.random_title, self.random_title, '200447249')
        return random_app_msg

    def create(self, app_msg):
        if not app_msg : return
        random_app_msg = self.__build_random_app_msg()
        self.process.app_msg = random_app_msg
        self.process.create()

        print self.process.response_json

        request = WechatGetAppMsgListRequest(self.request_token)
        request.get()
        app_msgs = request.list

        random_title_app_msg = self.__find_random_title_app_msg(app_msgs)
        if not random_title_app_msg : return
        app_msg.app_msg_id = random_title_app_msg.app_msg_id
        self.process.app_msg = app_msg
        self.process.update()

        self.app_msg_id = random_title_app_msg.app_msg_id

        print self.app_msg_id

    def open(self):
        # open重写不可用
        return

    def __find_random_title_app_msg(self, app_msgs):
        if not app_msgs : return None
        if not isinstance(app_msgs, list) : return None
        for app_msg in app_msgs:
            base_item = app_msg.items[0]
            print base_item.title
            if base_item.title == self.random_title :
                return app_msg
        return None





class WechatDevServerSettingRequest(WechatDataRequest):
    """docstring for WechatDevSettingRequest"""
    def __init__(self, request_token, operation_seq):
        super(WechatDevServerSettingRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/advanced/callbackprofile?t=ajax-response&lang=zh_CN"
        self.referer_url = "https://mp.weixin.qq.com/advanced/advanced?action=interface&t=advanced/interface&lang=zh_CN"
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
        print self.response_json

    def _build_params(self):
        params = dict()
        params['url'] = self.server_url
        params['callback_token'] = self.callback_token
        params['encoding_aeskey'] = self.encoding_aeskey
        params['callback_encrypt_mode'] = self.callback_encrypt_mode
        params['operation_seq'] = self.operation_seq
        return params


class WechatGetTicketRequest(WechatDataRequest):
    """docstring for WechatGetTicketResquest"""
    def __init__(self, request_token):
        super(WechatGetTicketRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/misc/safeassistant?1=1&lang=zh_CN"
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&lang=zh_CN"
        self.ticket = None
        self.operation_seq = None

    def get_ticket(self):
        self.open()
        return self.ticket

    def _on_open_url_after(self):
        super(WechatGetTicketRequest, self)._on_open_url_after()
        self.ticket = self.response_json.get('ticket')
        self.operation_seq = self.response_json.get('operation_seq')

    def _build_params(self):
        params = build_wechat_base_request_params()
        params['ajax'] = '1'
        params['action'] = 'get_ticket'
        params['token'] = self.request_token
        return params

class WechatGetSafeUUIDRequest(WechatDataRequest):
    """docstring for WechatGetSafeUUIDRequest"""
    def __init__(self, request_token):
        super(WechatGetSafeUUIDRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/safe/safeqrconnect?1=1&lang=zh_CN"
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&lang=zh_CN"
        self.ticket = None
        self.uuid = None
        self.app_name = None
        self.app_desc = None

    def get_uuid(self, ticket):
        if not ticket : return
        self.ticket = ticket
        self.open()
        return self.uuid

    def _on_open_url_after(self):
        super(WechatGetSafeUUIDRequest, self)._on_open_url_after()
        self.uuid = self.response_json.get('uuid')
        self.app_name = self.response_json.get('appname')
        self.app_desc = self.response_json.get('appdesc')

    def _build_params(self):
        params = build_wechat_base_request_params()
        params['ajax'] = '1'
        params['scope'] = 'snsapi_contact'
        params['state'] = '0'
        params['appid'] = 'wx3a432d2dbe2442ce'
        params['ticket'] = self.ticket
        params['redirect_uri'] = 'https://mp.weixin.qq.com'
        params['login_type'] = 'safe_center'
        params['type'] = 'json'
        params['token'] = self.request_token
        return params

class WechatDownloadSafeQRCodeRequest(WebRequest):
    """docstring for WechatDownloadSafeQRCodeRequest"""
    def __init__(self, request_token):
        super(WechatDownloadSafeQRCodeRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/safe/safeqrcode?action=check&type=cburl"
        self.referer_url = "https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&lang=zh_CN"
        self.is_file_down = True
        self.file_ext = 'png'

        self.ticket = None
        self.uuid = None
        self.msg_id = None

    def download(self, path, file_name = None):
        if not self.ticket or not self.uuid or not self.msg_id : return
        if not path : return
        self.download_path = path
        if file_name : self.download_file_name = file_name
        self.url = self._build_url()
        super(WechatDownloadSafeQRCodeRequest, self).open()

    def _build_url(self):
        url = "%s&ticket=%s&uuid=%s&msgid=%s" % (self.base_url, self.ticket, self.uuid, self.msg_id)
        return url

class WechatQRCodeCheckRequest(WechatDataRequest):
    """docstring for WechatQRCodeCheckRequest"""
    def __init__(self, request_token):
        super(WechatQRCodeCheckRequest, self).__init__(request_token)
        self.base_url = "https://mp.weixin.qq.com/safe/safeuuid?lang=zh_CN"
        self.referer_url = "https://mp.weixin.qq.com/advanced/advanced?action=interface&t=advanced/interface&lang=zh_CN"
        self.uuid = None

    def _build_url(self):
        url = "%s&timespam=%d" % (self.base_url, long(time.time()))
        return url

    def check(self, uuid):
        if not uuid : return
        self.uuid = uuid
        self.open()
        print self.response_json

    def _build_params(self):
        params = build_wechat_base_request_params()
        params['type'] = 'json'
        params['token'] = self.request_token
        params['f'] = 'josn'
        params['ajax'] = '1'
        params['action'] = 'json'
        params['uuid'] = self.uuid
        return params

