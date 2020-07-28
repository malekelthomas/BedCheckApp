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


def single_client_data_view(request, *args, **kwargs):
    this_client_cares_id = request.session.get('this_client_cares_id')
    obj = Client.objects.get(cares_id=this_client_cares_id)
    data = {
        "response": [obj.id, obj.first_name, obj.last_name, obj.cares_id, obj.room_num, obj.bed, obj.lp_on, obj.getImgUrl()]
    }
    return JsonResponse(data)

def single_client_view(request, caresID, *args, **kwargs):
    this_client_cares_id = caresID
    request.session['this_client_cares_id'] = this_client_cares_id
    context = {"cares_id": this_client_cares_id}
    return render(request, "pages/client_view.html", context, status=200)