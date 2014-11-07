#-*- coding: utf-8 -*-

from api.src.APIParser import BaseAPIParser
from api.src.APIRequest import BaseAPIRequest
from api.src.APIResponse import BaseAPIResponse
from api.src.APIListener import BaseAPIListener
from api.src.ReplyData import NewsReplyData
from common.TimeUtil import *
from common.UserUtil import *
from chestnut.src.ModelDao import *

from chestnut.models import *

import logging

log = logging.getLogger(__name__)

class ChestnutAPIParser(BaseAPIParser):
    """docstring for ChestnutShellAPIRarser"""
    def __init__(self):
        super(ChestnutAPIParser, self).__init__()

    def parse(self, request_data):
        if request_data.request_method == "POST" and request_data.request_get_data.get('chestnut_user'):
            return ChestnutAPIRequest(request_data)
        return super(ChestnutAPIParser, self).parse(request_data)

class ChestnutAPIRequest(BaseAPIRequest):
    """docstring for ChestnutShellAPIRarser"""
    def __init__(self, request_data):
        super(ChestnutAPIRequest, self).__init__(request_data)

        self.chestnut_user = None
        self.chestnut_password = None
        self.chestnut_wechat_id = None
        self.chestnut_wechat_token = None

        self.post_id = None
        self.post_author = None
        self.post_date = None
        self.post_date_gmt = None
        self.post_content = None
        self.post_pic = None
        self.post_title = None
        self.post_excerpt = None
        self.post_status = None
        self.comment_status = None
        self.ping_status = None
        self.post_password = None
        self.post_name = None
        self.to_ping = None
        self.pinged = None
        self.post_modified = None
        self.post_modified_gmt = None
        self.post_content_filtered = None
        self.post_parent = None
        self.guid = None
        self.menu_order = None
        self.post_type = None
        self.post_mime_type = None
        self.comment_count = None
        self.filter = None

        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.post_id = request_data.request_post_data.get('ID')
        # self.chestnut_user = request_data.request_get_data.get('chestnut_user')

        for key, value in request_data.request_get_data.items():
            try:
                self.__dict__[key] = value
            except Exception, e:
                print e

        for key in self.__dict__:
            value = request_data.request_post_data.get(key)
            if value is not None:
                self.__dict__[key] = value

        self.post_date = str_to_date(self.post_date)
        self.post_date_gmt = str_to_date(self.post_date_gmt)

        self.post_modified = str_to_date(self.post_modified)
        self.post_modified_gmt = str_to_date(self.post_modified_gmt)


    def __str__(self):
        return "post_id:%s post_content:%s post_pic:%s" % (self.post_id, self.post_content, self.post_pic)

    def __unicode__(self):
        return self.__str__()

class ChestnutAPIResponse(BaseAPIResponse):
    """docstring for ChestnutAPIResponse"""
    def __init__(self):
        super(ChestnutAPIResponse, self).__init__()

    def response(self, request):

        user_name = request.chestnut_user
        chestnut_user = get_chestnut_user(user_name)
        if not chestnut_user:
            return
        save_post_for_request(chestnut_user, request)

        return "chestnut_user:%s post_id:%s post_content:%s" % (request.chestnut_user, request.post_id, request.post_content)


class ChestnutWeChatTextMessageAPIListener(BaseAPIListener):
    """docstring for ChestnutWeChatTextMessageAPIListener"""

    def listen(self, request):
        pass


class ChestnutWeChatMessageAPIResponse(BaseAPIResponse):
    def __init__(self):
        super(ChestnutWeChatMessageAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(MessageAPIResponse, self).response(request)

        response_data = NewsReplyData(request)
        # response_data.set_article_item('BesideBamboo and Bargetor', 'Hybrid Species', 'http://www.bargetor.com/wp-content/themes/bargetor/images/img-home-banner.jpg', 'http://www.bargetor.com')
        # response_data.set_article_item('mini-player', 'mini-player', 'http://www.bargetor.com/wp-content/uploads/2014/06/mini-player-150x150.png', 'http://www.bargetor.com/works/mini-play.html')

        post_list = get_post_list_for_wechat_id(request.to_user_name, 5)
        for post in post_list:
            response_data.set_article_item(post.post_title, '', post.post_pic, post.guid)

        log.info(response_data.get_xml_str())
        return response_data.get_xml_str()

class ChestnutSignupAPIParser(BaseAPIParser):
    def __init__(self):
        super(ChestnutSignupAPIParser, self).__init__()

    def parse(self, request_data):
        if request_data.request_method == "POST" and request_data.request_get_data.get('method') == 'signup':
            return ChestnutAPIRequest(request_data)
        return super(ChestnutSignupAPIParser, self).parse(request_data)

class ChestnutSignupAPIResponse(BaseAPIResponse):
    """docstring for ChestnutSignupAPIResponse"""
    def __init__(self):
        super(ChestnutSignupAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return None
        create_chestnut_user_for_request(request)

        django_user = get_django_user_by_username(request.chestnut_user)
        if not django_user:
            create_normal_django_user(request.chestnut_user, request.chestnut_password)
        else:
            reset_django_user_password(django_user, request.chestnut_password)

