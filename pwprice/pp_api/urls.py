# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from pwprice.pp_api.views import ReviewView, KeywordView

urlpatterns = patterns('',
    # レビュー
    url(r'review/(?P<jan>[0-9]+)/$', ReviewView.as_view()),     # 一覧
    url(r'kwd/$',KeywordView.as_view()),
)
