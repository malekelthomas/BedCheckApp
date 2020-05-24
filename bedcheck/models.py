from django.db import models

# Create your models here.

class Client(models.Model):
    firstName = models.TextField(blank=True, null=True)
    lastName = models.TextField(blank=True, null=True)
    caresID = models.IntegerField(blank=True, null=True)
    roomNumber = models.IntegerField(blank=True, null=True)
    bed = models.CharField(blank=True, null=True, max_length =1)
    signature = models.FileField(upload_to='images/', blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
