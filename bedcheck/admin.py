from django.contrib import admin

# Register your models here.
from .models import Client
from .models import User

admin.site.register(Client)
admin.site.register(User)