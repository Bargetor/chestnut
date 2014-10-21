from api.src.APIRequest import BaseAPIRequest, SignatureAPIRequest

class BaseAPIParser(object):
    """docstring for BaseAPIParser"""
    def __init__(self):
        super(BaseAPIParser, self).__init__()

    def parse(self, request):
        return None

class SignatureRequestParser(object):
    """docstring for SignatureRequestParser"""
    def __init__(self):
        super(SignatureRequestParser, self).__init__()

    def parse(self, request):
        if request.method == "GET":
            return SignatureAPIRequest(request)
        return super.parse(request)

