# encoding:utf-8

import settings
import hashlib
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import QueryDict

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from api import BridgeApi, Cache
import urllib


@csrf_protect
def home(request):

    ctxt = {}
    ctxt.update(csrf(request))

    if not "kwd" in request.GET:
        request.GET = QueryDict("kwd=アウトレット&i=1")

    # 検索処理
    if "kwd" in request.GET and request.GET[u"kwd"]:
        kwds = request.GET[u"kwd"].split()

        # キャッシュ用の処理
        cache_keys = []
        for kwd in kwds:
            cache_keys.append(hashlib.sha224(kwd.encode('utf-8')).hexdigest())

        if "minPrice" in request.GET:
            ctxt.update({'minPrice': request.GET[u"minPrice"]})
            cache_keys.append(hashlib.sha224("minPrice_%s" % request.GET[u"minPrice"]).hexdigest())
        if "maxPrice" in request.GET:
            ctxt.update({'maxPrice': request.GET[u"maxPrice"]})
            cache_keys.append(hashlib.sha224("maxPrice_%s" % request.GET[u"maxPrice"]).hexdigest())
        # 価格(jan)検索の何番目かの番号
        if "rec" in request.GET:
            ctxt.update({'rec': request.GET[u"rec"]})
        # 価格順かおすすめか
        if "sort" in request.GET and request.GET["sort"]:
            cache_keys.append(hashlib.sha224("sort_1").hexdigest())

        """
        if "item_status" in request.GET and request.GET["item_status"]:
            cache_keys.append(hashlib.sha224("item_status").hexdigest())

        if "store" in request.GET and request.GET["store"]:
            cache_keys.append(hashlib.sha224("store").hexdigest())

        if "buynow" in request.GET and request.GET["buynow"]:
            cache_keys.append(hashlib.sha224("buynow").hexdigest())
        """

        cache_keys.sort()

        ctxt.update({'kwd': request.GET[u"kwd"].encode('utf-8'),
                     'cache_keys':cache_keys,
                     'sort': 1 if "sort" in request.GET and request.GET["sort"] else 0,
                     'jan': '' if not "rec" in request.GET else request.GET[u"rec"].encode('utf-8'),
                     'item_status': 1 if "item_status" in request.GET and request.GET["item_status"]  == u'1' else 0,
                     'store': 1 if "store" in request.GET and request.GET["store"]  == u'1'else 0,
                     'buynow': 1 if "buynow" in request.GET and request.GET["buynow"]  == u'1'else 0,
                     'shipping': 1 if "shipping" in request.GET and request.GET["shipping"] else 0,
                     'init': 1 if "i" in request.GET and request.GET["i"] else 0,
                    })
        
        ctxt.update({"results": BridgeApi.getAll(ctxt)})

        print "cache_keysであるなしチェックや登録などの処理入れるよ", cache_keys

    if "rec" in request.GET and request.GET[u"rec"]:
        price_data, lowestPrice= BridgeApi.getPriceCheckData(ctxt)
        ctxt.update({"praice_results": price_data,
                     "lowestPrice":lowestPrice})

    ctxt = RequestContext(request, ctxt)

    return render_to_response("index.html",ctxt)

