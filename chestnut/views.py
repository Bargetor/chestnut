from django.shortcuts import render
from api.src import APIRequest
from django.http import HttpResponse
from django.contrib import auth

def index(request):
    response_str = None
    if request.user.is_authenticated():
        response_str = request.user.username

    return render(request, 'chestnut/index.html', {'response_str':response_str})

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
    return HttpResponse('')

def signup(request):
    return HttpResponse('')
