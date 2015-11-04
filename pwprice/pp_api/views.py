# -*- coding: utf-8 -*-
import urllib
#from django.conf import settings
import settings
import json

from django.http.response import JsonResponse
from django.views.generic import View
from pwprice.api import ApiUtill


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context

class ReviewView(JSONResponseMixin, View):

    def get(self, *args, **kwargs):
        jan = kwargs['jan']
#        return self.render_to_json_response({"p":datas})
        return self.render_to_json_response(_get_yahoo_reiew(jan))



def _get_yahoo_reiew(jan, hits=20):

    if not jan:
        return ""

    url = "http://shopping.yahooapis.jp/ShoppingWebService/V1/json/reviewSearch?"

    param_dict = {
        'jan': jan,
#        'appid': settings.YAHOO_S_ID,
        'appid': 'dj0zaiZpPXQ4MjlYTUdRZzBOSyZzPWNvbnN1bWVyc2VjcmV0Jng9ZWM-',
        'hits':hits,
    }
    param = urllib.urlencode(param_dict)

    datas = ApiUtill.callAPI(url, param)

    return json.loads(datas)

def _get_yahoo_keyword_ranking(hits=10):
    url = "http://shopping.yahooapis.jp/ShoppingWebService/V1/json/queryRanking?"

    param_dict = {
        'appid': 'dj0zaiZpPXQ4MjlYTUdRZzBOSyZzPWNvbnN1bWVyc2VjcmV0Jng9ZWM-',
        'hits': hits,
    }
    param = urllib.urlencode(param_dict)

    datas = ApiUtill.callAPI(url, param)

    return json.loads(datas)

class KeywordView(JSONResponseMixin, View):

    def get(self, *args, **kwargs):
        return self.render_to_json_response(_get_yahoo_keyword_ranking())

