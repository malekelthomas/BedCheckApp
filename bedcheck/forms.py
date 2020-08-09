from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User
from .models import Client

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False) #super looks into MRO of class for next class, returns a super object which acts as proxy
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

class ClientSignatureForm(ModelForm):
    class Meta:
        model = Client
        fields = ('signature',)
        widgets = {'signature': forms.FileInput(),}
    
    def save(self, commit=True):
        client = super(ClientSignatureForm, self).save(commit=False)
        client.signature = self.cleaned_data['signature']
        print(client.signature)
        if commit:
            client.save()
            print(client)
        return client

