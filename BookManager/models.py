# -*- coding: UTF-8 -*-
__author__ = 'Zeming'

from django.db import models
import datetime

class BookClass(models.Model):
    class Meta:
        verbose_name = u'图书'
        verbose_name_plural = verbose_name
    isbn = models.CharField(u'ISBN', max_length=13, unique=True, blank=True, null=True)
    title = models.CharField(u'书名', max_length=200)
    subtitle = models.CharField(u'副标题', max_length=200, blank=True, null=True)
    pages = models.CharField(u'页数', max_length=5,blank=True, null=True)
    author = models.CharField(u'作者', max_length=60, blank=True, null=True)
    translator = models.CharField(u'译者', max_length=60, blank=True, null=True)
    price = models.CharField(u'定价', max_length=60, blank=True, null=True)
    publisher = models.CharField(u'出版社', max_length=200, blank=True, null=True)
    pubdate = models.CharField(u'出版日期', max_length=60, blank=True, null=True)
    cover_img = models.TextField(u'封面图', null=True,blank=True )
    summary = models.TextField(u'内容简介', blank=True, max_length=2000, null=True)
    author_intro = models.TextField(u'作者简介', blank=True, max_length=2000, null=True)
    Lend = models.IntegerField(u"借阅次数",default=0)
    Add = models.DateField(u"添加时间",default=datetime.date.today())
    def __unicode__(self):
        return unicode(self.title)

class BookInstance(models.Model):
    class Meta:
        verbose_name = u'图书实例'
        verbose_name_plural = verbose_name
    Type = models.ForeignKey(BookClass)
    Buy = models.DateField(u'购买日期')
    BookID = models.IntegerField(u"编号")
    Use = models.ForeignKey("BookUse", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.Type.title) + unicode(self.BookID)


class BookUse(models.Model):
    class Meta:
        verbose_name=u'借阅记录'
        verbose_name_plural=verbose_name
    BookI = models.ForeignKey(BookInstance,blank=True, null=True)
    BookC = models.ForeignKey(BookClass)
    Lend = models.DateField(u"出借日期",blank=True, null=True)
    Rent = models.DateField(u"归还日期",blank=True, null=True)
    Name = models.CharField(u"借阅人", max_length=30)
    Note = models.CharField(u"备注", max_length=200,blank=True, null=True)
    def __unicode__(self):
        return unicode(self.Book.Type.title) + unicode(self.Name)
