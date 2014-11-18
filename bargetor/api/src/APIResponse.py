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

