# -*- coding: utf-8 -*-
import hashlib
from bargetor.common import ArrayUtil, XMLUtil
from bargetor.api.APISettings import *

class APIRequestData(object):
    """docstring for APIRequestData"""
    def __init__(self, http_request):
        super(APIRequestData, self).__init__()

        self.request_method = http_request.method
        self.request_get_data = http_request.GET
        self.request_post_data_body = http_request.body
        self.request_post_data = http_request.POST
        self.request_post_xml_dic = None

        self.__parse_xml_data()

    def __parse_xml_data(self):
        etree = XMLUtil.parse_from_str(self.request_post_data_body)
        self.request_post_xml_dic = XMLUtil.get_children_text_dic(etree, CHARSET)

    def __str__(self):
        return "%s %s %s" % (self.request_method, self.request_get_data, self.request_post_data_body)

    def __unicode__(self):
        return self.__str__()


class BaseAPIRequest(object):
    """docstring for BaseAPIRequest"""
    def __init__(self, request_data):
        super(BaseAPIRequest, self).__init__()

        self.__load_request_data(request_data)

    def __load_request_data(self, request_data):
        pass


