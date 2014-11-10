from django.http import HttpResponse
from chestnut.src.Wechat import Wechat


def user_info(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    wechat = Wechat(username, password)
    wechat.wechat_auto_login()
    wechat.request_user_setting_page()


    return HttpResponse(wechat.setting_page.account_info.name)
