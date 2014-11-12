from api.src import APIRequest
from django.http import HttpResponse
from django.contrib import auth

from common import UserUtil
from chestnut.src import ChestnutModelDao

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
    wechat_defualt_id = request.POST.get('wechat_defualt_id')

    ChestnutModelDao.create_chestnut_user(wechat_username, wechat_password, wechat_defualt_id, None)

    django_user = UserUtil.get_django_user_by_username(wechat_username)
    if not django_user:
        UserUtil.create_normal_django_user(wechat_username, wechat_defualt_id)
    return HttpResponse('')
