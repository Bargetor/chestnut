import hashlib
import time
from bargetor.common import ArrayUtil
from bargetor.api.APISettings import MY_WECHAT_TOKEN
from bargetor.api.src.APIRequest import *
from bargetor.common.XMLUtil import *
from bargetor.api.APISettings import *
from bargetor.api.src.ReplyData import *

from bargetor.common import EncryptionUtil

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
        # if self.__signature(MY_WECHAT_TOKEN, request.signature, request.timestamp, request.nonce, request.echostr):
        #     return request.echostr
        # return None
        return request.echostr

    def __signature(self, token, signature, timestamp, nonce, echostr):
        if token is None or signature is None or timestamp is None or nonce is None or echostr is None:
            return False
        array = [token, timestamp, nonce]
        array.sort()
        splice_str =  ArrayUtil.str_array_splice(array)
        sha1_str = EncryptionUtil.sha(splice_str)
        return sha1_str == signature

class MessageAPIResponse(BaseAPIResponse):
    """docstring for MessageAPIResponse"""
    def __init__(self):
        super(MessageAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(MessageAPIResponse, self).response(request)

        if isinstance(request, TextAPIRequest):
            response_data = TextReplyData(request)
            response_data.content = "hello, this's great system, it's called chestnut!"
            return response_data.get_xml_str()

        if isinstance(request, PicAPIRequest):
            response_data = ImageReplyData(request)
            response_data.media_id = "media_id12345678"
            return response_data.get_xml_str()

        if isinstance(request, VoiceAPIRequest):
            response_data = VoiceReplyData(request)
            response_data.media_id = "media_id12345678"
            return response_data.get_xml_str()

        if isinstance(request, VideoAPIRequest):
            response_data = VideoReplyData(request)
            response_data.media_id = "media_id12345678"
            response_data.thumb_media_id = "thumb_media_id1234"
            response_data.title = "bargetor"
            response_data.description = "bargetor and chestnut"
            return response_data.get_xml_str()

        if isinstance(request, LocationAPIRequest):
            response_data = NewsReplyData(request)
            response_data.set_article_item('BesideBamboo and Bargetor', 'Hybrid Species', 'http://www.bargetor.com/wp-content/themes/bargetor/images/img-home-banner.jpg', 'http://www.bargetor.com')
            response_data.set_article_item('mini-player', 'mini-player', 'http://www.bargetor.com/wp-content/uploads/2014/06/mini-player-150x150.png', 'http://www.bargetor.com/works/mini-play.html')
            return response_data.get_xml_str()

        if isinstance(request, LinkAPIRequest):
            response_data = MusicReplyData(request)
            response_data.media_id = "media_id12345678"
            response_data.music_url = "music url"
            response_data.hq_music_url = "hq music url"
            response_data.thumb_media_id = "thumb_media_id"
            response_data.title = "music title"
            response_data.description = "music description"
            return response_data.get_xml_str()

class EventAPIResponse(BaseAPIResponse):
    """docstring for EventAPIResponse"""
    def __init__(self):
        super(EventAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(EventAPIResponse, self).response(request)
        return request.event

