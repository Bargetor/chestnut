from django.shortcuts import render


def index(request):
    response_str = None
    if request.user.is_authenticated():
        response_str = request.user.username

    return render(request, 'chestnut/index.html', {'response_str':response_str})


