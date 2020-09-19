"""BedCheckApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from bedcheck.models import User
from bedcheck.views import report_view
from bedcheck.views import roster_list_view
from bedcheck.views import roster_view
from bedcheck.views import login_view, logout_view, home_view
from bedcheck.views import single_client_data_view
from bedcheck.views import single_client_view, register_view, client_delete_view

app_name = 'bedcheck'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('bedcheck.urls','bedcheck'), namespace="home")),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path("roster/",include(('bedcheck.urls','bedcheck'), namespace="roster")),
    path("rosterlist/", roster_list_view, name="roster_data"),
    path("this_client/<int:caresID>", include(('bedcheck.urls', 'bedcheck'), namespace="single-client")),
    path("this_client_data/", single_client_data_view, name="client_data"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('report/', report_view)
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
