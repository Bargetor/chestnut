from django.http import HttpResponse
from bargetor.api.src.APIParser import BaseAPIParser
from bargetor.api.src.APIRequest import APIRequestData
from bargetor.api.src.APIProcesser import APIProcesser
from bargetor.common import ClassUtil
import bargetor.api.APISettings as settings

import logging
import traceback

log = logging.getLogger(__name__)

class APICenter(object):
    """docstring for APICenter"""
    _instance = None
    _isInit = False
    _processer_chain = None

    def __new__(clz, *args, **kwargs):
        if not clz._instance:
            clz._instance = super(APICenter, clz).__new__(clz, *args, **kwargs)
        return clz._instance

    def __init__(self):
        super(APICenter, self).__init__()
        if not self._isInit:
            self.__processer_init()
            self._isInit = True
            log.info('APICenter init done!')

    def __processer_init(self):
        self._processer_chain = APIProcesser(None)
        for process_config_item in settings.request_processer_list:
            self._processer_chain.append_processer(APIProcesser(process_config_item))

    def process_request(self, http_request):
        request_data = APIRequestData(http_request)
        log.info(request_data)
        response = None
        try:
            response = self._processer_chain.process(request_data)
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
        if not response:
            response = HttpResponse(None)
        return response

