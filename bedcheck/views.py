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
    client_list = [{"id": x.id, "firstname": x.first_name, "lastname": x.last_name, "caresID": x.cares_id, "roomNumber": x.room_num, "bed": x.bed, "lpOn": x.lp_on, "image": x.getImgUrl()} for x in qs] #does not have signature and image, FileField not JSON serializable
    data = {
        "response": client_list
    }
    return JsonResponse(data)

def login_view(request, *args, **kwargs):
    return render(request, "pages/login.html", context ={}, status=200)
    
def single_client_data_view(request, caresID, *args, **kwargs):
	print(args, kwargs)
	obj = Client.objects.get(cares_id=caresID)
	return HttpResponse(f"Hello {obj.last_name}, {obj.first_name}")