from django.contrib import admin
from django.contrib import messages
# Register your models here.
from .models import Client
from .forms import CustomUserChangeForm
from .models import User, Room

admin.site.register(User)
admin.site.register(Client)

class RoomAdmin(admin.ModelAdmin):
	       def message_user(self, *args):
	       	pass
	       def save_model(self, request, obj, form, change):
	       	super(RoomAdmin, self).save_model(request, obj, form, change)
	       	if type(obj.save()) != str:
	       		messages.success(request, "Room successfully added")
	       	else:
	       		messages.error(request, obj.save())
	       		
admin.site.register(Room, RoomAdmin)