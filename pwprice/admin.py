# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from django.contrib import admin
from django.template.response import TemplateResponse

from pwprice.forms import NgFilterForm
from pwprice.models import NgFilter


class NgFilterAdmin(admin.ModelAdmin):
    form = NgFilterForm

class KwdAdmin(admin.ModelAdmin):
    r = requests.get('http://shopping.yahoo.co.jp/ranking/keyword/?sc_i=shp_pc_ranking-top_dcSideTheme_query')

    soup = BeautifulSoup(r.text)
    kwds = soup.findAll('h4','elTitle')
    for k in kwds:
        print k.text
    return TemplateResponse(request, 'admin/create_csv.html',)

admin.site.register(NgFilter, NgFilterAdmin)