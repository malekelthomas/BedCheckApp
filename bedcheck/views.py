from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.template import Context, loader
from .models import Client
# Create your views here.

def roster_view(request, *args, **kwargs):
    return render(request, "pages/rosterpage.html", context ={}, status=200)


def roster_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JS or Java/Swift/Android/iOS
    returns json data
    """
    qs = Client.objects.all()
    client_list = [{"id": x.id, "firstname": x.first_name, "lastname": x.last_name, "caresID": x.cares_id, "roomNumber": x.room_num, "bed": x.bed, "lpOn": x.lp_on, "image": x.getImgUrl()} for x in qs] #does not have signature
    data = {
        "response": client_list
    }
    return JsonResponse(data)

def login_view(request, *args, **kwargs):
    return render(request, "pages/login.html", context ={}, status=200)


def single_client_data_view(request, caresID, *args, **kwargs):
    obj = Client.objects.get(cares_id=caresID)
    data = {
        "response": [obj.id, obj.first_name, obj.last_name, obj.cares_id, obj.room_num, obj.bed, obj.lp_on, obj.getImgUrl()]
    }
    return JsonResponse(data)