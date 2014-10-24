# -*- coding: utf-8 -*-
import hashlib
from common import ArrayUtil, XMLUtil
from api.APISettings import *

class APIRequestData(object):
    """docstring for APIRequestData"""
    def __init__(self, http_request):
        super(APIRequestData, self).__init__()

        self.request_method = http_request.method
        self.request_get_data = http_request.GET
        # self.request_post_xml_data = http_request.POST.get(POST_DATA_NAME)
        self.request_post_xml_data = http_request.body
        self.request_post_xml_dic = None

        self.__parse_xml_data()

    def __parse_xml_data(self):
        etree = XMLUtil.parse_from_str(self.request_post_xml_data)
        self.request_post_xml_dic = XMLUtil.get_children_text_dic(etree, CHARSET)

    def __str__(self):
        return self.request_post_xml_dic.tostring()

    def __unicode__(self):
        return self.request_post_xml_dic.tostring()



class SignatureAPIRequest(object):
    """docstring for SignatureAPIRequest"""
    def __init__(self, request_data):
        super(SignatureAPIRequest, self).__init__()

        self.token = None
        self.signature = None
        self.time_stamp = None
        self.nonce = None
        self.echostr = None

        self.__init_request(request_data)

    def __init_request(self, request_data):
        self.signature = request_data.request_get_data.get('signature')
        self.timestamp = request_data.request_get_data.get('timestamp')
        self.nonce = request_data.request_get_data.get('nonce')
        self.echostr = request_data.request_get_data.get('echostr')




class BaseAPIRequest(object):
    """docstring for BaseAPIRequest"""
    def __init__(self, request_data):
        super(BaseAPIRequest, self).__init__()

        self.to_user_name = None
        self.from_user_name = None
        self.create_time = None
        self.msg_type = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.to_user_name = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_TO_USER_NAME)
        self.from_user_name = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_FROM_USER_NAME)
        self.create_time = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_CREATE_TIME)
        self.msg_type = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_MSG_TYPE)

class MessageAPIRequest(BaseAPIRequest):
    """docstring for MessageAPIRequest"""
    def __init__(self, request_data):
        super(MessageAPIRequest, self).__init__(request_data)

        self.msg_id = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.msg_id = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_MSG_ID)


class TextAPIRequest(MessageAPIRequest):
    """docstring for TextAPIRequest"""
    def __init__(self, request_data):
        super(TextAPIRequest, self).__init__(request_data)

        self.content = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.content = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_CONTENT)

class MediaAPIRequest(MessageAPIRequest):
    def __init__(self, request_data):
        super(MediaAPIRequest, self).__init__(request_data)

        self.media_id = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.media_id = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_MEDIA_ID)

class PicAPIRequest(MediaAPIRequest):
    """docstring for PicAPIRequest"""
    def __init__(self, request_data):
        super(PicAPIRequest, self).__init__(request_data)

        self.pic_url = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.pic_url = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_PIC_URL)


class VoiceAPIRequest(MediaAPIRequest):
    """docstring for VoiceAPIRequest"""
    def __init__(self, request_data):
        super(VoiceAPIRequest, self).__init__(request_data)

        self.format = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.format = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_FORMAT)

class VideoAPIRequest(MediaAPIRequest):
    """docstring for VideoAPIRequest"""
    def __init__(self, request_data):
        super(VideoAPIRequest, self).__init__(request_data)

        self.thumb_media_id = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.thumb_media_id = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_THUMB_MEDIA_ID)

class LocationAPIRequest(MessageAPIRequest):
    """docstring for LocationAPIRequest"""
    def __init__(self, request_data):
        super(LocationAPIRequest, self).__init__(request_data)

        self.location_x = None
        self.location_y = None
        self.scale = None
        self.label = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.location_x = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_LOCATION_X)
        self.location_y = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_LOCATION_Y)
        self.label = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_LABEL)
        self.scale = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_SCALE)

class LinkAPIRequest(MessageAPIRequest):
    """docstring for LinkAPIRequest"""
    def __init__(self, request_data):
        super(LinkAPIRequest, self).__init__(request_data)

        self.title = None
        self.description = None
        self.url = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.title = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_TITLE)
        self.description = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_DESCRIPTION)
        self.url = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_URL)

class EventAPIRequest(BaseAPIRequest):
    """docstring for EventAPIRequest"""
    def __init__(self, request_data):
        super(EventAPIRequest, self).__init__(request_data)
        self.event = None
        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        self.event = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_EVENT)

class SubscribeEventAPIRequest(EventAPIRequest):
    """docstring for subscribeEventAPIRequest"""
    def __init__(self, request_data):
        super(SubscribeEventAPIRequest, self).__init__(request_data)


class UnSubscribeEventAPIRequest(EventAPIRequest):
    """docstring for UnSubscribeEventAPIRequest"""
    def __init__(self, request_data):
        super(UnSubscribeEventAPIRequest, self).__init__(request_data)

