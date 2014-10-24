from api.src.APIRequest import *
from api.APISettings import *

class BaseAPIParser(object):
    """docstring for BaseAPIParser"""
    def __init__(self):
        super(BaseAPIParser, self).__init__()

    def parse(self, request_data):
        return None

class SignatureRequestParser(BaseAPIParser):
    """docstring for SignatureRequestParser"""
    def __init__(self):
        super(SignatureRequestParser, self).__init__()

    def parse(self, request_data):
        if request_data.request_get_data.get('echostr'):
            return SignatureAPIRequest(request_data)
        return super(SignatureRequestParser, self).parse(request_data)

class MessageRequestParser(BaseAPIParser):
    """docstring for MessageRequestParser"""
    def __init__(self):
        super(MessageRequestParser, self).__init__()

    def parse(self, request_data):
        if request_data.request_method == "POST":
            if not request_data.request_post_xml_dic:
                return super(MessageRequestParser, self).parse(request_data)
            request_type = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_MSG_TYPE)
            if not request_type:
                return super(MessageRequestParser, self).parse(request_data)
            if request_type == POST_DATA_MSG_TYPE_TEXT:
                return TextAPIRequest(request_data)

            if request_type == POST_DATA_MSG_TYPE_IMAGE:
                return PicAPIRequest(request_data)

            if request_type == POST_DATA_MSG_TYPE_VIDEO:
                return VideoAPIRequest(request_data)

            if request_type == POST_DATA_MSG_TYPE_VOICE:
                return VoiceAPIRequest(request_data)

            if request_type == POST_DATA_MSG_TYPE_LOCATION:
                return LocationAPIRequest(request_data)

            if request_type == POST_DATA_MSG_TYPE_LINK:
                return LinkAPIRequest(request_data)

            return super(MessageRequestParser, self).parse(request_data)

class EventRequestParser(BaseAPIParser):
    """docstring for EventRequestParser"""
    def __init__(self):
        super(EventRequestParser, self).__init__()

    def parse(self, request_data):
        if request_data.request_method == "POST":
            if not request_data.request_post_xml_dic:
                return super(EventRequestParser, self).parse(request_data)
            request_type = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_MSG_TYPE)
            if not request_type:
                return super(EventRequestParser, self).parse(request_data)
            if request_type != POST_DATA_MSG_TYPE_EVENT:
                return super(EventRequestParser, self).parse(request_data)

            event_type = request_data.request_post_xml_dic.get(POST_DATA_TAG_NAME_EVENT)
            if not event_type:
                return super(EventRequestParser, self).parse(request_data)

            if event_type == POST_DATA_EVENT_TYPE_SUBSCRIBE:
                return SubscribeEventAPIRequest(request_data)

            if event_type == POST_DATA_EVENT_TYPE_UNSUBSCRIBE:
                return UnSubscribeEventAPIRequest(request_data)

            return super(EventRequestParser, self).parse(request_data)
