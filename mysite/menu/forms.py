from django import forms
from .models import Notice,Rules,Comment,Noticomment

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'contents']

class RulesForm(forms.ModelForm):
    class Meta:
        model = Rules
        fields = ['title', 'contents']

class NoticomForm(forms.ModelForm):
    class Meta:
        model = Noticomment
        fields = ('contents',)