import hashlib
from common import ArrayUtil, XMLUtil


def signature(token, signature, timestamp, nonce, echostr):
    if token is None or signature is None or timestamp is None or nonce is None or echostr is None:
        return False
    array = [token, timestamp, nonce]
    array.sort()
    splice_str =  ArrayUtil.StrArraySplice(array)
    sha1= hashlib.sha1()
    sha1.update(splice_str)
    sha1_str = sha1.hexdigest()
    return sha1_str == signature


class APIRequestData(object):
    """docstring for APIRequestData"""
    def __init__(self, xml_data):
        super(APIRequestData, self).__init__()

        self.xml = xml_data
        self.request_dic = None

        self.__parseXML(self)

    def __parseXML(self):
        etree = XMLUtil.parseFromStr(self.xml)
        self.request_dic = XMLUtil.getChildrenTextDic(etree)



class SignatureAPIRequest(object):
    """docstring for SignatureAPIRequest"""
    def __init__(self, token, request):
        super(SignatureAPIRequest, self).__init__()

        self.token = token
        self.signature = None
        self.time_stamp = None
        self.nonce = None
        self.echostr = None

        __init_request(request)

    def __init_request(self, request):
        self.signature = request.GET.get('signature')
        self.timestamp = request.GET.get('timestamp')
        self.nonce = request.GET.get('nonce')
        self.echostr = request.GET.get('echostr')




class BaseAPIRequest(object):
    """docstring for BaseAPIRequest"""
    def __init__(self):
        super(BaseAPIRequest, self).__init__()

        self.to_user_name = None
        self.from_user_name = None
        self.create_time = None
        self.msg_type = None

class MessageAPIRequest(BaseAPIRequest):
    """docstring for MessageAPIRequest"""
    def __init__(self):
        super(MessageAPIRequest, self).__init__()

        self.msg_id = None



class TextAPIRequest(MessageAPIRequest):
    """docstring for TextAPIRequest"""
    def __init__(self):
        super(TextAPIRequest, self).__init__()

        self.content = None


class MediaAPIRequest(MessageAPIRequest):
    def __init__(self):
        super(MediaAPIRequest, self).__init__()

        self.media_id = None


class PicAPIRequest(MediaAPIRequest):
    """docstring for PicAPIRequest"""
    def __init__(self):
        super(PicAPIRequest, self).__init__()

        self.pic_url = None

class VoiceAPIRequest(MediaAPIRequest):
    """docstring for VoiceAPIRequest"""
    def __init__(self):
        super(VoiceAPIRequest, self).__init__()

        self.format = None

class VideoAPIRequest(MediaAPIRequest):
    """docstring for VideoAPIRequest"""
    def __init__(self):
        super(VideoAPIRequest, self).__init__()

        self.thumb_media_id = None

class LocationAPIRequest(MessageAPIRequest):
    """docstring for LocationAPIRequest"""
    def __init__(self):
        super(LocationAPIRequest, self).__init__()

        self.location_x = None
        self.location_y = None
        self.scale = None
        self.label = None

class LinkAPIRequest(MessageAPIRequest):
    """docstring for LinkAPIRequest"""
    def __init__(self):
        super(LinkAPIRequest, self).__init__()

        self.title = None
        self.description = None
        self.url = None

class EventAPIRequest(BaseAPIRequest):
    """docstring for EventAPIRequest"""
    def __init__(self):
        super(EventAPIRequest, self).__init__()

        self.event = None

