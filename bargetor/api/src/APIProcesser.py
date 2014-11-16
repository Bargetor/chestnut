from bargetor.api.src.APIParser import BaseAPIParser
from bargetor.api.src.APIResponse import BaseAPIResponse
from bargetor.api.src.APIListener import BaseAPIListener
from django.http import HttpResponse
from bargetor.common.ClassUtil import *
from bargetor.api.APISettings import *

import traceback
import logging

log = logging.getLogger(__name__)

class APIProcesser(object):
    """docstring for APIProcesser"""

    def __init__(self, request_processer_data):
        super(APIProcesser, self).__init__()

        self.next_processer = None

        self.request_processer_data = request_processer_data
        self.parser = None
        self.responser = None
        self.listener_list = []
        self.__init_processer(self.request_processer_data)

    def __init_processer(self, request_processer_data):
        self.__init_parser(request_processer_data)
        self.__init_responser(request_processer_data)
        self.__init_listener(request_processer_data)

    def __init_parser(self, request_processer_data):
        try:
            if not request_processer_data:
                return
            parser_name = request_processer_data[REQUEST_PARSER_CONFIG_NAME]
            log.info(parser_name)
            if not parser_name:
                return
            parser_clz = get_class_for_full_name(parser_name)
            if issubclass(parser_clz, BaseAPIParser):
                self.parser = parser_clz()
        except Exception, e:
            log.info('this processer not parser')
            traceback.print_exc()

    def __init_responser(self, request_processer_data):
        try:
            if not request_processer_data:
                return
            responser_name = request_processer_data[REQUEST_RESPONSER_CONFIG_NAME]
            log.info(responser_name)
            if not responser_name:
                return
            responser_clz = get_class_for_full_name(responser_name)
            if issubclass(responser_clz, BaseAPIResponse):
                self.responser = responser_clz()
        except Exception, e:
            log.info('this processer not responser')
            traceback.print_exc()

    def __init_listener(self, request_processer_data):
        try:
            if not request_processer_data:
                return
            listener_name_list = request_processer_data[REQUEST_LISTENER_CONFIG_NAME]
            log.info(listener_name_list)
            if not listener_name_list:
                return
            for listener_name in listener_name_list:
                listener_clz = get_class_for_full_name(listener_name)
                if not listener_clz:
                    continue
                if issubclass(listener_clz, BaseAPIListener):
                    self.listener_list.append(listener_clz())

        except Exception, e:
            log.info('this processer not responser')
            traceback.print_exc()

    def process(self, request_data):
        request = self.parse(request_data)
        if not request:
            return self.pass_request(request_data)
        self.notify_listener(request)
        return self.response(request)

    def pass_request(self, request_data):
        if not self.next_processer:
            return None
        return self.next_processer.process(request_data)

    def parse(self, request_data):
        if not self.parser:
            return None
        return self.parser.parse(request_data)

    def response(self, request):
        if not self.responser:
            return HttpResponse(None)
        return HttpResponse(self.responser.response(request))

    def notify_listener(self, request):
        for listener in self.listener_list:
            listener.listen(request)

    def append_processer(self, processer):
        if not self.next_processer:
            self.next_processer = processer
            return
        self.next_processer.append_processer(processer)
