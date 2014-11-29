import random
# *************************public method ********************************* #

def build_wechat_base_request_headers():
    headers = dict()

    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Host'] = 'mp.weixin.qq.com'
    headers['Origin'] = 'https://mp.weixin.qq.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    return headers


def build_wechat_base_request_params():
    params = dict()

    params['lang'] = 'zh_CN'
    params['f'] = 'json'
    params['random'] = str(random.random())

    return params
