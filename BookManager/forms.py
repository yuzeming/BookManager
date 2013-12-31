# -*- coding: UTF-8 -*-
__author__ = 'Zeming'
from django import forms
from models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = BookClass
        fields = ("isbn", "AutoCompletion", "title", "subtitle", "pages", "author", "translator", "price",
                  "publisher", "pubdate", "summary", "author_intro","delete","img","clean")

    img = forms.FileField(label=u"封面图", required=False)
    clean = forms.BooleanField(label=u"清除当前封面数据",required=False)
    AutoCompletion = forms.BooleanField(label=u"根据ISBN自动补全",required=False)
    delete = forms.BooleanField(label=u"删除图书",required=False)


class AskForm(forms.ModelForm):
    class Meta:
        model = BookUse
        fields = ("Note",)


class UserRegForm(forms.Form):
    ID = forms.CharField(label="Username")
    Email = forms.EmailField(label="Email")
    Password = forms.CharField(widget=forms.PasswordInput,label="Password")
    Password2 = forms.CharField(widget=forms.PasswordInput,label="Again")

    def clean_Password2(self):
        if len(self.cleaned_data.get("Password")) < 6:
            raise forms.ValidationError("Password too short!")
        if self.cleaned_data.get("Password")!=self.cleaned_data.get("Password2"):
            raise forms.ValidationError("not match!")
        if (User.objects.filter(username=self.cleaned_data.get("ID")).count()==1):
             raise forms.ValidationError("UserID exist")
        return self.cleaned_data.get("Password")

class ChangePasswordForm(forms.Form):
    OldPassword = forms.CharField(widget=forms.PasswordInput,label="Old Password")
    Password = forms.CharField(widget=forms.PasswordInput,label="New Password")
    Password2 = forms.CharField(widget=forms.PasswordInput,label="New Password Again")
    def clean_Password2(self):
        if len(self.cleaned_data.get("Password")) < 6:
            raise forms.ValidationError("Password too short!")
        if self.cleaned_data.get("Password")!=self.cleaned_data.get("Password2"):
            raise forms.ValidationError("not match!")
        return self.cleaned_data.get("Password")

