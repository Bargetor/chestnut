from django.http import HttpResponse
from bargetor.wechat.WechatCenter import WechatCenter

import traceback


def user_info(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        wechat = WechatCenter().build_wechat(username, password)
    except Exception, e:
        exstr = traceback.format_exc()
        print exstr
    response_json = None
    if wechat is not None : response_json =  wechat.setting_page.account_info.get_json_str()

    return HttpResponse(response_json)
