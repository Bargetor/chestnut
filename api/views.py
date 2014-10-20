from django.shortcuts import render
from api.src import APIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        if APIRequest.signature('bargetor_chestnut', signature, timestamp, nonce, echostr):
            return render(request, 'api/index.html', {'signature' : signature})
        else:
            return render(request, 'api/index.html', {'signature' : signature})
    if request.method == 'POST':
        return HttpResponse(request.POST['HTTP_RAW_POST_DATA'])
