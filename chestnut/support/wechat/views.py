from django.http import HttpResponse
from chestnut.src.wechat.WechatCenter import WechatCenter


def user_info(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    wechat = WechatCenter().build_wechat(username, password)

    response_json = None
    if wechat is not None : response_json =  wechat.setting_page.account_info.get_json_str()


    return HttpResponse(response_json)
