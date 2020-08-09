from django.urls import path

from . import views

app_name = 'bedcheck'

urlpatterns =[
    path("", views.home_view, name="home"),
    path("roster/", views.roster_view, name="roster"),
    path("this_client/<int:caresID>", views.single_client_view, name="single-client"),
]