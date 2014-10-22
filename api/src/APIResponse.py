import hashlib
from common import ArrayUtil
from api.APISettings import MY_WECHAT_TOKEN

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
        return request.msg_id

