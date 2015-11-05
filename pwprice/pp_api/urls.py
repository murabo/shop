# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from pwprice.pp_api.views import ReviewView, KeywordView, RankingView

urlpatterns = patterns('',
    # レビュー
    url(r'review/(?P<jan>[0-9]+)/$', ReviewView.as_view()),
    # キーワード
    url(r'kwd/$',KeywordView.as_view()),
    # 売り上げランキング
    url(r'ranking/(?P<category>[0-9]+)/$', RankingView.as_view()),
    url(r'ranking/$', RankingView.as_view()),
)
