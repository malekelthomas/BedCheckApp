from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
# Create your views here.

def roster_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")

# def login_view(request, *args, **kwargs):
#     template = loader.get_template("/Users/yeehaw/Documents/BedCheckApp/BedCheckApp/web/login.html")
#     return HttpResponse(template.render())