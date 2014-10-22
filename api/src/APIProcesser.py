from api.src.APIParser import BaseAPIParser
from api.src.APIResponse import BaseAPIResponse
from django.http import HttpResponse
from common.ClassUtil import *
from api.APISettings import *

import traceback

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
        self.__init_responser(self.request_processer_data)

    def __init_processer(self, request_processer_data):
        self.__init_parser(request_processer_data)

    def __init_parser(self, request_processer_data):
        try:
            if not request_processer_data:
                return
            parser_name = request_processer_data[REQUEST_PARSER_CONFIG_NAME]
            print parser_name
            if not parser_name:
                return
            parser_clz = get_class_for_full_name(parser_name)
            if issubclass(parser_clz, BaseAPIParser):
                self.parser = parser_clz()
        except Exception, e:
            print 'this processer not parser'
            traceback.print_exc()

    def __init_responser(self, request_processer_data):
        try:
            if not request_processer_data:
                return
            responser_name = request_processer_data[REQUEST_RESPONSER_CONFIG_NAME]
            print responser_name
            if not responser_name:
                return
            responser_clz = get_class_for_full_name(responser_name)
            if issubclass(responser_clz, BaseAPIResponse):
                self.responser = responser_clz()
        except Exception, e:
            print 'this processer not responser'
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
        return

    def append_processer(self, processer):
        if not self.next_processer:
            self.next_processer = processer
            return
        self.next_processer.append_processer(processer)
