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

class UserRegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email","username","password")



