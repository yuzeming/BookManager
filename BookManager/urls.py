# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from view import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BookManager.views.home', name='home'),
    # url(r'^BookManager/', include('BookManager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #主页
    url(r'^$',"BookManager.view.Index"),
    #我的主页
    url(r'^mybook$',"BookManager.view.MyBook"),
    #搜索
    url(r'^search',"BookManager.view.Search"),
    #登陆登出用户注册
    url(r'^login',"django.contrib.auth.views.login",{"template_name":"login.html"}),
    url(r'^logout', 'django.contrib.auth.views.logout',{"template_name":"logout.html"}),
    url(r"^admin$","BookManager.view.admin"),
    url(r"^reg$","BookManager.view.reg"),
    #图书类型管理
    url(r'^img/(?P<bkid>\d+)/$',"BookManager.view.ShowImg"),

    url(r'^book/(?P<bkid>\d+)/edit$',"BookManager.view.Edit"),
    url(r'^book/(?P<bkid>\d+)/$',"BookManager.view.Book"),
    #图书实例管理
    url(r'^book/(?P<bkid>\d+)/(?P<bid>\d+)/delete$',"BookManager.view.BookIns",{"action":"delete"}),
    url(r'^book/(?P<bkid>\d+)/(?P<bid>\d+)/$',"BookManager.view.BookIns"),
    #图书借阅管理
    url(r'^book/(?P<bkid>\d+)/ask$',"BookManager.view.Ask"),
    url(r"^need/(?P<nid>\d+)/delete$","BookManager.view.BookLend",{"action":"delete"}),
    url(r'^need/(?P<nid>\d+)/return$',"BookManager.view.BookLend",{"action":"return"}),
    url(r"^need/(?P<nid>\d+)/$","BookManager.view.BookLend"),


)
