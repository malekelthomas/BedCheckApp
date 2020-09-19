#pylint:disable=E0001
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime
import re
from django.conf import settings
# Create your models here.

class Client(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    cares_id = models.IntegerField(blank=True, null=True)
    room_num = models.IntegerField(blank=True, null=True)
    bed = models.CharField(blank=True, null=True, max_length =1)
    lp_on = models.TextField(blank=True, null=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, default="", null=True)
    image = models.ImageField(upload_to='images/', blank=True, default="", null=True)
    last_signature_time = models.TextField(blank=True,null=True)

    def getImgUrl(self):
        if self.image != "":
            img_url = self.image.url
            return img_url
        else:
            return ""

    def getSigUrl(self):
        if self.signature != "":
            pattern = str(datetime.date.today())
            if re.search(rf"{pattern}", str(self.signature)): #load file from today's date
                sig_url = self.signature.url
                return sig_url
        else:
            return ""
            
    def __str__(self):
    	return "{} {}".format(self.first_name, self.last_name)


class Room(models.Model):
	room_number = models.IntegerField(blank=True, null=True)
	bed_a = models.OneToOneField( 'Client', blank=True,null=True, unique=True,related_name='%(app_label)s_%(class)s_bed_a', on_delete=models.CASCADE)
	bed_b = models.OneToOneField('Client', blank=True, null=True, unique=True,  related_name='%(app_label)s_%(class)s_bed_b', on_delete=models.CASCADE)
	
	def find_client_room(self, bed):
		if bed == None:
			return False
		if Room.objects.filter(bed_a=bed).exists():
			for i in Room.objects.filter(bed_a=bed):
				return i
		elif Room.objects.filter(bed_b=bed).exists():
			for i in Room.objects.filter(bed_b=bed):
				return i
		else:
			return False
	
	def save(self, *args, **kwargs):
		if not self.find_client_room(self.bed_a) and not self.find_client_room(self.bed_b):
			if self.bed_a == None:
				super(Room, self).save(*args,**kwargs)
			super(Room, self).save(*args,**kwargs)
		else:
			if self.room_number != self.find_client_room(self.bed_a) and self.bed_a:
				return "{} is already in {}".format(self.bed_a, self.find_client_room(self.bed_a))
			if self.room_number != self.find_client_room(self.bed_b) and self.bed_b :
				return "{} is already in {}".format(self.bed_b, self.find_client_room(self.bed_b))
			else:
				super(Room,self).save(*args,**kwargs)
			
		
	
	
	def __str__(self):
		return "{}".format(self.room_number)
		
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, commit=True):
        """Creates and saves a User with supplied parameters"""
        if not email:
            raise ValueError(_('Must have an email address'))
        if not first_name:
            raise ValueError(_('Must have first name'))
        if not last_name:
            raise ValueError(_('User must have last name'))

        user = self.model(email=self.normalize_email(email), first_name=first_name,last_name=last_name,)

        user.set_password(password)
        if commit:
            user.is_active = False
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with supplied parameters
        """

        user = self.create_user(email,password=password, first_name=first_name, last_name=last_name, commit=False,)
        user.is_staff = True
        user.is_superuser = True
        user.is_supervisor = False
        user.save(using=self._db)
        return user 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
    #password and last login supplied by AbstractBaseUser
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)

    is_active = models.BooleanField(_('Active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),)
    
    is_supervisor = models.BooleanField(_('Supervisor Status'), default=False, help_text=_('Designates whether user has supervisor status.'),)

    is_staff = models.BooleanField(_('Staff Status'), default=True, help_text=('Designates whether the user can log into this admin site.'),)

    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now,)
    #is_superuser, groups, and user_permissions supplied by PermissionsMixin

    objects = UserManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True #Simplest answer = yes, always
    
    def has_module_perms(self, app_label):
        "Does user have permision to view the app 'app_label'?"
        return True
          