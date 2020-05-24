from django.db import models

# Create your models here.

class Client(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    cares_id = models.IntegerField(blank=True, null=True)
    room_num = models.IntegerField(blank=True, null=True)
    bed = models.CharField(blank=True, null=True, max_length =1)
    signature = models.FileField(upload_to='images/', blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
