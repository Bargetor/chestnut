import hashlib
import time
from common import ArrayUtil
from api.APISettings import MY_WECHAT_TOKEN
from common.XMLUtil import *
from api.APISettings import *

class BaseAPIResponse(object):
    """docstring for BaseAPIResponse"""
    def __init__(self):
        super(BaseAPIResponse, self).__init__()

    def response(self, reqeust):
        return None

class SignatureAPIResponse(BaseAPIResponse):
    """docstring for SignatureAPIResponse"""
    def __init__(self):
        super(SignatureAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(SignatureAPIResponse, self).response(request)
        if self.__signature(MY_WECHAT_TOKEN, request.signature, request.timestamp, request.nonce, request.echostr):
            return request.echostr
        return None

    def __signature(self, token, signature, timestamp, nonce, echostr):
        if token is None or signature is None or timestamp is None or nonce is None or echostr is None:
            return False
        array = [token, timestamp, nonce]
        array.sort()
        splice_str =  ArrayUtil.str_array_splice(array)
        sha1= hashlib.sha1()
        sha1.update(splice_str)
        sha1_str = sha1.hexdigest()
        return sha1_str == signature

class MessageAPIResponse(BaseAPIResponse):
    """docstring for MessageAPIResponse"""
    def __init__(self):
        super(MessageAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(MessageAPIResponse, self).response(request)
        response_data = TextResponseXMLData(request)
        response_data.content = "HAHA"
        return response_data.get_xml_str()

class EventAPIResponse(BaseAPIResponse):
    """docstring for EventAPIResponse"""
    def __init__(self):
        super(EventAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(EventAPIResponse, self).response(request)
        return request.event



class BaseResponseXMLData(object):
    """docstring for BaseResponseXMLData"""
    def __init__(self, request):
        super(BaseResponseXMLData, self).__init__()

        self.to_user_name = request.from_user_name
        self.from_user_name = request.to_user_name
        self.create_time = str(time.time())
        self.msg_type = None

    def build_xml_tree(self):
        etree = get_new_etree('xml')
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_TO_USER_NAME, self.to_user_name)
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_FROM_USER_NAME, self.from_user_name)
        write_text_child(etree.getroot(), POST_DATA_TAG_NAME_CREATE_TIME, self.create_time)
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_MSG_TYPE, self.msg_type)
        return etree

    def get_xml_str(self):
        etree = self.build_xml_tree()
        return to_etree_xml_str(etree)

class TextResponseXMLData(BaseResponseXMLData):
    """docstring for TextResponseXMLData"""
    def __init__(self, request):
        super(TextResponseXMLData, self).__init__(request)

        self.content = None
        self.msg_type = POST_DATA_MSG_TYPE_TEXT

    def build_xml_tree(self):
        etree = super(TextResponseXMLData, self).build_xml_tree()
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_CONTENT, self.content)
        return etree

