# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from pwprice.pp_api.views import ReviewView

urlpatterns = patterns('',
    # レビュー
    url(r'review/(?P<jan>[0-9]+)/$', ReviewView.as_view(), name='api'),     # 一覧
)
