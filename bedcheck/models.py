from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Client(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    cares_id = models.IntegerField(blank=True, null=True)
    room_num = models.IntegerField(blank=True, null=True)
    bed = models.CharField(blank=True, null=True, max_length =1)
    lp_on = models.TextField(blank=True, null=True)
    signature = models.FileField(upload_to='signatures/', blank=True, default="")
    image = models.ImageField(upload_to='images/', blank=True, default="")

    def getImgUrl(self):
        if self.image != None:
            img_url = self.image.url
            return img_url
        else:
            return ""

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
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with supplied parameters
        """

        user = self.create_user(email,password=password, first_name=first_name, last_name=last_name, commit=False,)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
    #password and last login supplied by AbstractBaseUser
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)

    is_active = models.BooleanField(_('Active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),)

    is_staff = models.BooleanField(_('Staff Status'), default=False, help_text=('Designates whether the user can log into this admin site.'),)

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