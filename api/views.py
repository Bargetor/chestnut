from django.shortcuts import render
from api.src import APIResponse

# Create your views here.

def index(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    if APIResponse.signature('bargetor_chestnut', signature, timestamp, nonce, echostr):
        return render(request, 'api/index.html', {'signature' : signature})
    else:
        return render(request, 'api/index.html', {'signature' : 'Flash'})
