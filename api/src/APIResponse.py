import hashlib
from common import ArrayUtil


def signature(token, signature, timestamp, nonce, echostr):
    if token is None or signature is None or timestamp is None or nonce is None or echostr is None:
        return False
    array = [token, timestamp, nonce]
    array.sort()
    sha1_str = hashlib.sha1(ArrayUtil.StrArraySplice(array))
    return sha1_str == signature

