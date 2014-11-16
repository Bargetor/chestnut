from bargetor.api.src import APIRequest
from django.http import HttpResponse
from django.contrib import auth

from chestnut.src.account import Account

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)

    if user is not None and user.is_active:
        auth.login(request, user)

        return HttpResponse('success!')
    else:
        return HttpResponse('faild!')

def logout(request):
    auth.logout(request)
    return HttpResponse('success!')

def signup(request):
    wechat_username = request.POST.get('wechat_username')
    wechat_password = request.POST.get('wechat_password')
    wechat_default_id = request.POST.get('wechat_default_id')

    Account.signup(wechat_username, wechat_password, wechat_default_id)
    return HttpResponse('')
