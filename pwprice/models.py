# -*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext as _

class NgFilter(models.Model):
    ng_1 = models.TextField(_('NG Wards 1'), blank=True)
    ng_2 = models.TextField(_('NG Wards 2'), blank=True)

    ad_ok_1 = models.TextField(_('OK ad 1'), blank=True)
    ad_ng_1 = models.TextField(_('NG ad 1'), blank=True)
    ad_ok_2 = models.TextField(_('OK ad 2'), blank=True)
    ad_ng_2 = models.TextField(_('NG ad 2'), blank=True)
    ad_ok_3 = models.TextField(_('OK ad 3'), blank=True)
    ad_ng_3 = models.TextField(_('NG ad 3'), blank=True)
    ad_ok_4 = models.TextField(_('OK ad 4'), blank=True)
    ad_ng_4 = models.TextField(_('NG ad 4'), blank=True)

    ad_ok_5 = models.TextField(_('OK ad 5'), blank=True)
    ad_ng_5 = models.TextField(_('NG ad 5'), blank=True)
    ad_ok_6 = models.TextField(_('OK ad 6'), blank=True)
    ad_ng_6 = models.TextField(_('NG ad 6'), blank=True)
    ad_ok_7 = models.TextField(_('OK ad 7'), blank=True)
    ad_ng_7 = models.TextField(_('NG ad 7'), blank=True)
    ad_ok_8 = models.TextField(_('OK ad 8'), blank=True)
    ad_ng_8 = models.TextField(_('NG ad 8'), blank=True)

    class Meta:
        verbose_name = u'NGワード・広告管理'

