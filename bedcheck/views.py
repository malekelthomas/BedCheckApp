from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import Context, loader
from .models import Client
from .forms import NewUserForm, ClientSignatureForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from time import sleep
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
    return render(request, "pages/rosterpage.html", context ={}, status=200)


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
            return redirect("bedcheck:home")
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
                return redirect("bedcheck:home")
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
	return redirect("bedcheck:home")

def single_client_data_view(request, *args, **kwargs):
    this_client_cares_id = request.session.get('this_client_cares_id')
    obj = Client.objects.get(cares_id=this_client_cares_id)
    data = {
        "response": [obj.id, obj.first_name, obj.last_name, obj.cares_id, obj.room_num, obj.bed, obj.lp_on, obj.getImgUrl()]
    }
    return JsonResponse(data)

def single_client_view(request, caresID, *args, **kwargs):
    this_client_cares_id = caresID
    this_client = Client.objects.get(cares_id=caresID)
    request.session['this_client_cares_id'] = this_client_cares_id
    context = {"cares_id": this_client_cares_id}
    if request.method == 'POST':
        form = ClientSignatureForm(request.POST, request.FILES, instance=this_client)
        if form.is_valid():
            print(form)
            client = form.save()
            #return redirect("/roster")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "pages/client_view.html", context, status=200)

    form = ClientSignatureForm
    return render(request, "pages/client_view.html", context, status=200)