from django.shortcuts import render
from api.src import APIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.src.APICenter import APICenter

# Create your views here.
@csrf_exempt
def index(request):
    return APICenter().process_request(request)
