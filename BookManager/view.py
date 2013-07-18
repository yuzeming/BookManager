# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from models import *
from forms import *
import base64
import urllib2
import json
import string
from settings import PASSWORD ,noimg
import datetime
import random

def NeedAdmin(func):
    def _NeedAdmin(*args, **kwargs):
        request = args[0]
        if not request.session.get("admin", False):
            messages.error(request,"只有可爱的管理员姐姐才能访问这个页面")
            return redirect("/login?go="+request.path)
        return func(*args,**kwargs)
    return _NeedAdmin

@NeedAdmin
def Edit(request, bkid):
    c = None
    i = None
    if int(bkid) != 0:
        c = get_object_or_404(BookClass, pk=bkid)
        i = BookInstance.objects.filter(Type=c)
    if request.REQUEST.get("delete",None) and c is not None:
        c.delete()
        messages.success(request,"成功删除")
        return redirect("/")

    if request.REQUEST.get("isbn", None) and request.REQUEST.get("AutoCompletion", False):
        isbn = request.REQUEST.get("isbn", None)
        try:
            j = dict(json.loads(urllib2.urlopen('http://api.douban.com/v2/book/isbn/' + isbn).read()))
        except:
            j = None
            messages.error(request, u"获取信息失败")
        if j:
            if c is None:
                c = BookClass()
            c.author = j.get("author", None)
            c.isbn = j.get("isbn13", None)
            c.title = j.get("title", None)
            c.subtitle = j.get("subtitle", None)
            c.pages = j.get("pages", None)
            c.author = string.join(j.get("author", None), " / ")
            c.translator = string.join(j.get("translator", None), "/ ")
            c.price = j.get("price", None)
            c.publisher = j.get("publisher", None)
            c.pubdate = j.get("pubdate", None)
            c.summary = j.get("summary", None)
            c.author_intro = j.get("author_intro", None)
            img_url = j.get("images", {}).get("large", "")
            try:
                tmp = urllib2.urlopen(img_url).read()
                c.cover_img = base64.encodestring(tmp)
            except:
                messages.error(request, u"获取图片失败")
            c.save()
            return HttpResponseRedirect("/book/%d/" % (c.pk,))
    book = None
    if request.method == "POST":
        book = BookForm(request.POST, request.FILES, instance=c)
        book.img = None
        if book.is_valid():
            img = request.FILES.get("img", None)
            if img:
                bimg = ''
                if img.multiple_chunks():
                    for chunk in img.chunk():
                        bimg += chunk
                else:
                    bimg = img.read()
                book.img = base64.encodestring(bimg)
            bookc = book.save(commit=False)
            if book.img or book.cleaned_data["clean"]:
                bookc.cover_img = book.img
            bookc.save()
            return HttpResponseRedirect("/book/%d/" % (book.instance.pk,))
    else:
        book = BookForm(instance=c)
    return render_to_response("edit.html", {"form": book, "book": c, "list": i, "bkid": bkid},
                              context_instance=RequestContext(request))


def ShowImg(request, bkid):
    c = get_object_or_404(BookClass, pk=bkid)
    if c.cover_img:
        return HttpResponse(base64.decodestring(c.cover_img), mimetype="image/jpg")
    else:
        return HttpResponse(base64.decodestring(noimg), mimetype="image/jpg")


def Book(request, bkid ):
    c = get_object_or_404(BookClass, pk=bkid)
    i = BookInstance.objects.filter(Type=c)
    need = BookUse.objects.filter(BookC=c,BookI=None).all()
    if request.method == "POST":
        try:
            num = int(request.REQUEST.get("addnum", 0))
        except ValueError:
            num = 0
        qs = BookInstance.objects.filter(Type=c).order_by("-BookID")
        last = 0
        if qs.count() != 0:
            last = qs[0].BookID

        for x in xrange(last + 1, last + num +1):
            bi = BookInstance()
            bi.Type = c
            bi.Buy = datetime.date.today()
            bi.BookID = x
            bi.save()
        messages.success(request, "已经添加")
    return render_to_response("book.html", {"book": c, "list": i ,"need":need}, context_instance=RequestContext(request))

@NeedAdmin
def BookIns(request,bkid,bid,action="show"):
    c = get_object_or_404(BookClass, pk=bkid)
    i = get_object_or_404(BookInstance ,Type = c , BookID =bid)
    used = BookUse.objects.filter(BookI=i).all()

    if action=="delete":
        i.delete()
        messages.success(request,u"成功删除图书")
        return redirect("/book/"+str(c.pk))

    return render_to_response("booki.html",{"book": c, "booki": i,"used": used})

def Search(request):
    kw = request.REQUEST.get("kw", None)
    if kw is None or len(kw) == 0:
        messages.info(request, u"没有输入关键字，到首页逛逛吧.")
        return redirect("/")
    book = []
    book.extend(BookClass.objects.filter(title__icontains=kw).all())
    book.extend(BookClass.objects.filter(isbn__icontains=kw).all())
    book.extend(BookClass.objects.filter(author__icontains=kw).all())
    return render_to_response("search.html", {"list": book, "kw": kw}, context_instance=RequestContext(request))


def Ask(request, bkid):
    c = get_object_or_404(BookClass, pk=bkid)
    if request.method == "POST":
        askf = AskForm(request.POST)
        if askf.is_valid():
            askm = askf.save(commit=False)
            askm.BookC = c
            askm.save()
            messages.success(request, u"成功预订，管理员会人工联系你！")
            return redirect("/book/" + str(c.pk))
    else:
        askf = AskForm()
    return render_to_response("ask.html", {"ask": askf, "book": c}, context_instance=RequestContext(request))

@NeedAdmin
def BookLend(request,nid,action="lend"):
    u = get_object_or_404(BookUse, pk =nid)
    i = BookInstance.objects.filter(Type=u.BookC ,Use=None)
    go = request.REQUEST.get("go","/book/"+str(u.BookC.pk))
    if action=="return":
        if u.Rent is None:
            u.Rent = datetime.date.today()
            u.save()
            u.BookI.Use = None
            u.BookI.save()
        else:
            messages.error(request,u"我觉得这本书已经归还了")

    if action=="delete":
        u.delete()
        messages.success(request,u"成功删除")
        return redirect("/book/"+str(u.BookC.pk))
    if action=="lend":
        if (i.count()==0):
            messages.error(request,u"没有可用的图书了")
        else:
            i=i[random.randint(0,i.count()-1)]
            u.BookI=i
            u.Lend=datetime.date.today()
            u.save()
            i.Use=u
            i.Type.Lend += 1
            i.Type.save()
            i.save()
            messages.success(request,u"将"+str(i.BookID)+u"借阅给"+u.Name)
    return redirect(go)

def Login(request):
    if request.method == "POST":
        password = request.POST.get("PWD")
        if password == PASSWORD:
            request.session["admin"] = True
            messages.success(request, u"登陆成功")
        else:
            messages.error(request, u"密码不正确")
    go = request.REQUEST.get("go", "/")
    if request.session.get("admin", False):
        return redirect(go)
    return render_to_response("login.html", {"go": go}, context_instance=RequestContext(request))


def Logout(request):
    request.session["admin"] = False
    messages.success(request, u"退出")
    return redirect("/")

def Index(request):
    totc = BookClass.objects.count()
    toti = BookInstance.objects.count()
    mostuse = BookClass.objects.order_by("-Lend")[0:6]
    recadd = BookClass.objects.order_by("-Add")[0:6]
    return render_to_response("index.html",{"totc":totc,"toti":toti,"mostusd":mostuse,"recadd":recadd},
                              context_instance=RequestContext(request) )
@NeedAdmin
def admin(request):
    ask = BookUse.objects.filter(BookI = None)
    ret = BookUse.objects.filter(Rent__isnull = True , Lend__isnull=False)
    return render_to_response("admin.html" ,{"ask":ask,"ret":ret},context_instance=RequestContext(request))