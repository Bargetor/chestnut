import hashlib
from common import ArrayUtil


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

