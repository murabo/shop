# -*- coding:utf-8 -*-
import os
import redis
from django import forms

from pwprice.models import NgFilter


class NgFilterForm(forms.ModelForm):
    class Meta:
        model = NgFilter
        fields = '__all__'


    def is_valid(self):

        path = 'pwprice/template/ad'

        self._set_redis("ng_1", self.data["ng_1"])
        self._set_redis("ng_2", self.data["ng_2"])

        if not os.path.exists(path):
            os.mkdir(path)
        for i in xrange(1,9):
            file_path = os.path.join(path, 'ad_ng_{}.html'.format(i))
            f = open(file_path, 'w')
            f.write(self.data["ad_ng_{}".format(i)])
            f.close() # ファイルを閉じる
            file_path = os.path.join(path, 'ad_ok_{}.html'.format(i))
            f = open(file_path, 'w')
            f.write(self.data["ad_ok_{}".format(i)])
            f.close() # ファイルを閉じる

        print u"Success!!"
        return super(NgFilterForm, self).is_valid()

    def _set_redis(self, key, value):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.setex(key, 36000, value)
