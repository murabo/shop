# -*- coding: utf-8 -*-
from django.contrib import admin

from pwprice.forms import NgFilterForm
from pwprice.models import NgFilter


class NgFilterAdmin(admin.ModelAdmin):
    form = NgFilterForm

admin.site.register(NgFilter, NgFilterAdmin)