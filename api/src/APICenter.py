from django.http import HttpResponse
from api.src.APIParser import BaseAPIParser
from api.src.APIRequest import APIRequestData
import api.APISettings as settings
from common import ClassUtil


class APICenter(object):
    """docstring for APICenter"""
    _instance = None
    _parser_list = []

    def __new__(clz, *args, **kwargs):
        if not clz._instance:
            clz._instance = super(APICenter, clz).__new__(clz, *args, **kwargs)
        return clz._instance

    def __init__(self):
        super(APICenter, self).__init__()
        self.__parser_init()

    def __parser_init(self):
        for parser_config_item in settings.request_parsers:
            parser_clz = ClassUtil.get_class_for_full_name(parser_config_item["name"])
            if issubclass(parser_clz, BaseAPIParser):
                self._parser_list.append(parser_clz())

    def process_request(self, http_request):
        request = None
        request_data = APIRequestData(http_request)
        for parser in self._parser_list:
            request = parser.parse(request_data)
            if request:
                break
        print request
        return self.response_request(request)

    def response_request(self, request):
        if not request:
            return HttpResponse(None)
        return HttpResponse(request.echostr)

