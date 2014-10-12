# encoding:utf-8

import settings
import hashlib
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from api import BridgeApi, Cache
import urllib


@csrf_protect
def home(request):

    ctxt = {}
    ctxt.update(csrf(request))

    # 検索処理
    if "kwd" in request.GET and request.GET[u"kwd"]:
        kwds = request.GET[u"kwd"].split()

        if "minPrice" in request.GET:
            ctxt.update({'minPrice': request.GET[u"minPrice"]})
        if "maxPrice" in request.GET:
            ctxt.update({'maxPrice': request.GET[u"maxPrice"]})
        # 価格(jan)検索の何番目かの番号
        if "rec" in request.GET:
            ctxt.update({'rec': request.GET[u"rec"]})
        # 価格順かおすすめか
        if "sort" in request.GET:
            sort = request.GET[u"sort"]
        else:
            sort = 0

        # キャッシュ用の処理
        cache_keys = []
        for kwd in kwds:
            cache_keys.append(hashlib.sha224(kwd.encode('utf-8')).hexdigest())

        # 価格順の場合は、キーに追加
        if sort:
            cache_keys.append(hashlib.sha224(sort).hexdigest())

        cache_keys.sort()
        ctxt.update({'kwd': request.GET[u"kwd"].encode('utf-8'),
                     'cache_keys':cache_keys,
                     'sort': sort,
                     'jan': '' if not "jan" in request.GET else request.GET[u"jan"].encode('utf-8')
                    })

        ctxt.update({"results": BridgeApi.getAll(ctxt)})


        print "cache_keysであるなしチェックや登録などの処理入れるよ", cache_keys
    
    return render_to_response("index.html",ctxt)

