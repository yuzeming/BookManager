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
from settings import PASSWORD
import datetime
import random
from django.core.files.base import ContentFile
from settings import NOImg
from django.contrib.auth.decorators import login_required

def NeedAdmin(viewfunc):
    def _NeedAdmin(request,*argv,**argc):
        if request.user.is_authenticated() and request.user.is_superuser:
            return viewfunc(request,*argv,**argc)
        else:
            return redirect("/")
    return _NeedAdmin

@NeedAdmin
def Edit(request, bkid):
    '''
    编辑图书
    '''
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
            j = dict(json.loads(urllib2.urlopen('http://api.douban.com/v2/book/isbn/' + isbn,timeout=10).read()))
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
            c.save()
            try:
                tmp = urllib2.urlopen(img_url,timeout=10).read()
                c.cover_img.save(str(c.id)+".jpg",ContentFile(tmp))
            except:
                messages.error(request, u"获取图片失败")
            return HttpResponseRedirect("/book/%d/" % (c.pk,))
    book = None
    if request.method == "POST":
        book = BookForm(request.POST, request.FILES, instance=c)
        book.img = None
        if book.is_valid():
            img = request.FILES.get("img", None)
            if img:
                book.img = ''
                if img.multiple_chunks():
                    for chunk in img.chunk():
                        book.img += chunk
                else:
                    book.img = img.read()
            bookc = book.save()
            if book.cleaned_data["clean"]:
                bookc.cover_img.delete(True)
            if book.img:
                bookc.cover_img.save(str(c.id)+".jpg",ContentFile(book.img))
            return HttpResponseRedirect("/book/%d/" % (book.instance.pk,))
    else:
        book = BookForm(instance=c)
    return render_to_response("edit.html", {"form": book, "book": c, "list": i, "bkid": bkid},
                              context_instance=RequestContext(request))


def ShowImg(request, bkid):
    if bkid=='0':
        return HttpResponse(NOImg,content_type="image/jpeg")
    c = get_object_or_404(BookClass, pk=bkid)
    if c.cover_img:
        return HttpResponse(c.cover_img,content_type="image/jpeg")
    else:
        return HttpResponse(NOImg,content_type="image/jpeg")


def Book(request, bkid ):
    c = get_object_or_404(BookClass, pk=bkid)
    i = BookInstance.objects.filter(Type=c)
    need = BookUse.objects.filter(BookC=c,BookI=None).all()
    if request.method == "POST":
        try:
            num = int(request.REQUEST.get("addnum", 0))
        except ValueError:
            num = 0
        if (num>100):
            messages.error(request, "不能一次添加太多")
        else:
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


@login_required
def Ask(request, bkid):
    c = get_object_or_404(BookClass, pk=bkid)
    if request.method == "POST":
        askf = AskForm(request.POST)
        if askf.is_valid():
            askm = askf.save(commit=False)
            askm.BookC = c
            askm.User = request.user
            askm.save()
            messages.success(request, u"成功预订，管理员将联系你！")
            return redirect("/book/" + str(c.pk))
    else:
        askf = AskForm()
    return render_to_response("ask.html", {"ask": askf, "book": c}, context_instance=RequestContext(request))

@login_required
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
            messages.success(request,u"将"+str(i.BookID)+u"借阅给"+u.User.username)
    return redirect(go)

def Index(request):
    totc = BookClass.objects.count()
    toti = BookInstance.objects.count()
    mostuse = BookClass.objects.order_by("-Lend")[0:6]
    recadd = BookClass.objects.order_by("-Add")[0:6]
    return render_to_response("index.html",{"totc":totc,"toti":toti,"mostusd":mostuse,"recadd":recadd},
                              context_instance=RequestContext(request) )
@login_required()
def admin(request):
    ask = BookUse.objects.filter(BookI = None)
    ret = BookUse.objects.filter(Rent__isnull = True , Lend__isnull=False)
    return render_to_response("admin.html" ,{"ask":ask,"ret":ret},context_instance=RequestContext(request))

@login_required()
def MyBook(request):
    ask = BookUse.objects.filter(User = request.user,BookI = None)
    ret = BookUse.objects.filter(User = request.user,Rent__isnull = True , Lend__isnull=False)
    return render_to_response("mybook.html",{"ask":ask,"ret":ret},context_instance=RequestContext(request))

def UserReg(request):
    pass