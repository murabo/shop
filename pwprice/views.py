# encoding:utf-8
import redis
import mojimoji
import settings
import hashlib
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import QueryDict

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from api import BridgeApi, Cache
from constants import CRAWLER_USER_AGENT
import urllib
from models import NgFilter


@csrf_protect
def home(request):

    ctxt = {}
    ctxt.update(csrf(request))

    if not "kwd" in request.GET:
        request.GET = QueryDict("kwd=アウトレット&i=1")

    if _check_crawler_ua(request):

        ctxt.update({'kwd': request.GET[u"kwd"].encode('utf-8'),
                     'init': 1 if "i" in request.GET and request.GET["i"] else 0,
                    })
        ctxt = RequestContext(request, ctxt)
        return render_to_response("crawler_index.html",ctxt)

    # 検索処理
    if "kwd" in request.GET and request.GET[u"kwd"]:
        kwds = request.GET[u"kwd"].split()
        ng_list1 = _get_redis("ng_1")
        ng_filter = NgFilter.objects.get(pk=1)
        if ng_list1:
            ng_list1 = ng_list1.split('\r\n')
        else:
            ng_list1 = ng_filter.ng_1.encode('utf-8').split('\r\n')

        if _check_ng(request.GET[u"kwd"].encode('utf-8'), ng_list1):
            request.GET = QueryDict("kwd=アウトレット&i=1")

        ng_list2 = _get_redis("ng_2")
        if ng_list2:
            ng_list2 = _get_redis("ng_2").split('\r\n')
        else:
            ng_list2 = ng_filter.ng_2.encode('utf-8').split('\r\n')

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
                     'ng': _check_ng(request.GET[u"kwd"].encode('utf-8'), ng_list2),
                    })

        ctxt.update({"results": BridgeApi.getAll(ctxt)})

        if not ctxt["jan"]:
            try:
                q = request.GET.urlencode() + "&rec=%s" % ctxt["results"]["jandata"][0]["jan"][0]
                category = ctxt["results"]["jandata"][0]["category"]
            except:
                q = ''
                category = '1'
            request.GET = QueryDict(q.encode('utf-8'))
            ctxt.update(csrf(request))
            ctxt.update({'jan': '' if not "rec" in request.GET else request.GET[u"rec"].encode('utf-8'),
                         'category': category})

    if "rec" in request.GET and request.GET[u"rec"]:
        price_data, lowestPrice= BridgeApi.getPriceCheckData(ctxt)
        ctxt.update({"praice_results": price_data,
                     "lowestPrice":lowestPrice})

    ctxt = RequestContext(request, ctxt)

    return render_to_response("index.html",ctxt)


def _check_crawler_ua(request):
    user_agent=request.META.get('HTTP_USER_AGENT',None)

    for ua in CRAWLER_USER_AGENT:
        if ua in user_agent:
            return True
        return False

def _check_ng(kwd, ng_list):
    for ng in ng_list:
        if (mojimoji.zen_to_han(kwd.decode('utf-8'), kana=False).encode('utf-8').lower().find(ng)
            or mojimoji.zen_to_han(ng.decode('utf-8'), kana=False).lower() in mojimoji.zen_to_han(kwd.lower().decode('utf-8'), kana=False)):
            return True

def _get_redis(key):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r.get(key)