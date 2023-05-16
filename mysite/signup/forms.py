from django import forms
from django.contrib.auth.models import User
#from .models import Registration

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'username','password')

'''
class UserForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('',)
'''