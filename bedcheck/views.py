from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import Context, loader
from .models import Client, Room
from .forms import NewUserForm, ClientSignatureForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
import datetime
import base64
import os
from pathlib import Path
import re
# Create your views here.


def home_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {"user":request.user, "user_name":request.user.get_full_name()}
            return render(request, "pages/home.html", context, status=200)
        else:
            return render(request, "pages/home.html", context={}, status=200)

def profile_view(request, *args, **kwargs):
    pass

def roster_view(request, *args, **kwargs):
    time_client_signed = request.session.get('time_submitted')
    return render(request, "pages/rosterpage.html", context ={"time_client_signed": time_client_signed}, status=200)


def roster_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JS or Java/Swift/Android/iOS
    returns json data
    """
    qs = Client.objects.all()
    client_list = [{"id": x.id, "firstname": x.first_name, "lastname": x.last_name, "caresID": x.cares_id, "roomNumber": x.room_num, "bed": x.bed, "lpOn": x.lp_on, "image": x.getImgUrl(), "signature": x.getSigUrl()} for x in qs]
    data = {
        "response": client_list
    }
    return JsonResponse(data)

def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request,user)
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "pages/register.html", context={"form":form})

    form = NewUserForm
    return render(request, "pages/register.html", context={"form":form})

def login_view(request, *args, **kwargs):
    if request.method == 'POST': #if user is logging in not creating an acc
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username") #normalizes data
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/")
            else:
                print("Unsuccessful")
                messages.error(request, "Invalid username or password")
    else:
        print("Unsuccessful")
        messages.error(request, "Invalid username or password") 
    form = AuthenticationForm()
    return render(request, "pages/login.html", context={"form":form})
    	
    	
def logout_view(request, *args, **kwargs):
	logout(request)
	return redirect("/")

def single_client_data_view(request, *args, **kwargs):
    this_client_cares_id = request.session.get('this_client_cares_id')
    obj = Client.objects.get(cares_id=this_client_cares_id)
    data = {
        "response": [obj.id, obj.first_name, obj.last_name, obj.cares_id, obj.room_num, obj.bed, obj.lp_on, obj.getImgUrl()]
    }
    return JsonResponse(data)

def bedcheck_time():
    time = str(datetime.datetime.now().strftime("%I:%M %p"))
    split_time = re.split(":| ",time) #splits time string by : and " "
    if split_time[2] == "AM":
        if split_time[0] == 12 and split_time[1] <= 45:
            return True
        elif split_time[0] == 2 and split_time[1] <= 30:
            return True
        else:
            return False
    elif split_time[2] == "PM":
        if split_time[0] == 9:
            if split_time[1] >= 55:
                return True
        elif split_time[0] == 10:
            if split_time[1] <= 45:
                return True
        else:
            return False


def single_client_view(request, caresID, *args, **kwargs):
    this_client_cares_id = caresID
    this_client = Client.objects.get(cares_id=caresID)
    request.session['this_client_cares_id'] = this_client_cares_id
    context = {"user_is_supervisor":request.user.is_supervisor, "cares_id": this_client_cares_id, "bedcheck_time": bedcheck_time(), "time_now": str(datetime.datetime.now().strftime("%I:%M %p"))}
    if request.method == 'POST':
        form = ClientSignatureForm(request.POST, request.FILES, instance=this_client)
        context["form"] = form
        if form.is_valid():
            client = form.save()
            signature = request.POST.get('signature', False)
            time_submitted = request.POST.get('date', False)
            request.session['time_submitted'] = time_submitted
            print(time_submitted)
            path_parent = Path(settings.MEDIA_ROOT)
            this_client_signatures_path = path_parent/"signatures"/str(caresID)/str(datetime.date.today()) 
            this_client_signatures_log_path = path_parent/"signatures"/str(caresID)/"log"
            if not os.path.exists(this_client_signatures_path):
                print("creating path", this_client_signatures_path)
                os.makedirs(this_client_signatures_path)
                with open(this_client_signatures_path/"sig.png","wb") as f:
                    str_as_bytes = str.encode(signature.split(",")[1])
                    f.write(base64.decodebytes(str_as_bytes))
                    f.close()
            else:
                print("saving file", this_client_signatures_path, "\n")
                with open(this_client_signatures_path/"sig.png","wb") as f:
                    str_as_bytes = str.encode(signature.split(",")[1])
                    f.write(base64.decodebytes(str_as_bytes))
                    f.close()
                    
            if not os.path.exists(this_client_signatures_log_path):
            	   print("creating path",this_client_signatures_log_path)
            	   os.makedirs(this_client_signatures_log_path)
            	   with open(this_client_signatures_log_path/"log.txt", "a") as f:
            	   	f.write("Last time signed: "+time_submitted+"\n")
            	   	f.close()
            else:
            	   	print("updating log")
            	   	with open(this_client_signatures_log_path/"log.txt", "a") as f:
            	   		f.write("Last time signed: "+time_submitted+"\n")
            	   		f.close()
            	   	
            	   	
            	   
            client.signature = str(this_client_signatures_path)[str(this_client_signatures_path).index("media/")+len("media/"):]+"/sig.png" #have to handle slashes on different platforms
            print(client.signature)
            client.save()
            return redirect("/roster")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "pages/client_view.html", context, status=200)

    form = ClientSignatureForm
    return render(request, "pages/client_view.html", context, status=200)


def client_delete_view(request, caresID, *args, **kwargs):
	client = Client.objects.get(cares_id=caresID)
	client.delete()
	return  redirect("/roster")


        
        
