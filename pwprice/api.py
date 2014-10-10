# encoding:utf-8

import settings
import hashlib
from django.template import RequestContext
from django.shortcuts import render_to_response
import urllib
import json
import unicodedata
import redis
import time
import msgpack

class BridgeApi(object):
    RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20140222?"
    VALUE_API_URL   = "http://webservice.valuecommerce.ne.jp/productdb/search?"

    MOSHIMO_A_ID = 431508
    MOSHIMO_URL = "http://c.af.moshimo.com/af/c/click?a_id=%s&p_id=54&pc_id=54&pl_id=616" % MOSHIMO_A_ID

    YAHOO_S_URL = "http://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?"
    YAHOO_A_URL = "http://auctions.yahooapis.jp/AuctionWebService/V2/search?"
    
    VC_Y_A_URL = "http://ck.jp.ap.valuecommerce.com/servlet/referral?sid=3161331&pid=882992162&"

    EC_CODE_A = '038p6'
    EC_CODE_P = '0vbnk'
    EC_CODE = '%s,%s' % (EC_CODE_A, EC_CODE_P)
    SUGGEST = []

    YAHOO_DATA = []
    JAN_DATA = []
    JANCODE_LIST = []
    ponpare_data = []
    amazon_data = []

    @classmethod
    def exchangeRakuten(cls, datas):
        results = []
        for data in datas:

            data = data['Item']
            res = {"itemName":data['itemName'],
                  "itemPrice":data['itemPrice'],
                  "pointRate":data['pointRate'],
                  "postageFlag":data['postageFlag'],
                  "asurakuFlag":data['asurakuFlag'],
                  "reviewAverage":data['reviewAverage'],
                  "reviewCount":data['reviewCount'],
                  "itemUrl":data['itemUrl'],}
            if data['mediumImageUrls']:
                res["imageUrl"] = data['mediumImageUrls'][0]['imageUrl']

            results.append(res)

        return results


    @classmethod
    def createJanImgMap(cls):
        tmp = []
        cls.JAN_DATA = []
        cls.getLowPrice()
        if cls.YAHOO_DATA:
            for data in cls.YAHOO_DATA:
                if data['jan'] and len(cls.JAN_DATA) < 5 and not data['jan'] in tmp:
                    tmp.append(data['jan'])
                    cls.JAN_DATA.append({"jan":[data['jan']],
                                         "imageUrl": data['imageUrl'],
                                        "itemName": data['itemName']})
        print cls.JAN_DATA

        
    @classmethod
    def getLowPrice(cls):
        print "AMA",len(cls.amazon_data)
        for data in cls.amazon_data:
            # print data['janCode']
            continue



    @classmethod
    def exchangeVC(cls, datas):
        results = []
        for data in datas:
            print data['merchantName'],data['janCode']
            results.append({"itemName":data['title'],
                       "itemPrice":data['price'],
                       "itemUrl":data['link'],
                       "imageUrl":data['imageFree']['url']})
        return results

    @classmethod
    def exchangeYahooS(cls, datas):
        results = []
        for data in datas:
            #print data
            results.append({"itemName":data['Name'],
                           "itemPrice":data['Price']['_value'],
                           "itemUrl":data['Url'],
                           "imageUrl":data['ExImage']['Url'],
                           "jan": data['JanCode']
                           })
        return results



    @classmethod
    def exchangeYahooA(cls, datas):
        results = []
        

        for data in datas:
            param = urllib.urlencode(
                                     {
                                     'vc_url': data['AuctionItemUrl'],
                                     })
            print "YA:",
            results.append({"itemName":data['Title'],
                           "itemUrl":cls.VC_Y_A_URL + param,
                           "imageUrl":data['Image'],
                       })
        return results

    @classmethod
    def getRakten(cls, ctxt, sort=0):
        api_name = 'rakuten'
        param = urllib.urlencode(
                        {'format': 'json',
                         'keyword': ctxt['kwd'],
                         'applicationId': settings.RAKUTEN_APP_ID,
                         'minPrice': ctxt['minPrice'],
                         'maxPrice': ctxt['maxPrice'],
                         'imageFlag': '1'}
        )

        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        if not datas:
            print "キャッシュなし"
            datas = urllib.urlopen(cls.RAKUTEN_API_URL + param)
            datas = datas.read()
            datas = json.loads(datas)
            Cache.setCacheData(api_name, ctxt['cache_keys'], datas)
        else:
            print "キャッシュあり"

        # 必要なデータだけに生成
        return cls.exchangeRakuten(datas['Items'])


    @classmethod
    def getYahooS(cls, ctxt, sort=0):
        api_name = 'yahoo_shopping'
        param = urllib.urlencode(
                             {
                                 'query': ctxt['kwd'],
                                 'appid': settings.YAHOO_S_ID,
                                 'affiliate_type':'vc',
                                 'affiliate_id': settings.YAHOO_S_AF_ID,
                                 'jan':'',
                                 'image_size':76,
                                 'category_id':'',
                                 'price_from': ctxt['minPrice'],
                                 'price_to': ctxt['maxPrice'],
                                 'hits':50
                                  #'sort':'',
                                  # 'shipping': ctxt['shipping'], # 1：送料無料 デフォルトはなし
                             })
        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        result_datas = []

        if not datas:
            print "キャッシュなし"
            datas = urllib.urlopen(cls.YAHOO_S_URL + param)

            datas = datas.read()
            datas = json.loads(datas)['ResultSet']
            if 0 < datas['totalResultsReturned'] and 'totalResultsReturned' in datas:
                for i in xrange(0, int(datas['totalResultsReturned'])):
                    result_datas.append(datas[u'0']['Result'][u'%s' % i])

            Cache.setCacheData(api_name, ctxt['cache_keys'], result_datas)
            datas = result_datas

        else:
            print "キャッシュありS",datas[0]

        for data, index in enumerate(datas):
            if index == 0:
                print "data 1",data
#        if datas[u'0']['Result'][u'%s' % i]['JanCode'] and len(cls.JANCODE_LIST) <= 5:
#            cls.JANCODE_LIST.append(datas[u'0']['Result'][u'%s' % i]['JanCode'])

#        cls.JANCODE_LIST = list(set(cls.JANCODE_LIST))[:5]

        print len(result_datas)
        cls.YAHOO_DATA = cls.exchangeYahooS(datas)
        cls.createJanImgMap()
        # 必要なデータだけに生成
        return cls.exchangeYahooS(datas)


    @classmethod
    def getYahooA(cls, ctxt, sort=0):
        api_name = 'yahoo_auctions'
        param = urllib.urlencode(
                             {
                             'query': ctxt['kwd'],
                             'appid': settings.YAHOO_A_ID,
                             'output':'json',
                             'category_id':'',
                             'aucminprice': ctxt['minPrice'],
                             'aucmaxprice': ctxt['maxPrice'],
                             'item_status':0, #0 ：指定なし,1 ：新品
                             'sort':'affiliate',
                             # 'shipping': ctxt['shipping'], # 1：送料無料 デフォルトはなし
                             })




        data = Cache.getCacheData(api_name, ctxt['cache_keys'])
        
        datas = []
        if not data:
            print "キャッシュなしYA!"
            data = urllib.urlopen(cls.YAHOO_A_URL + param)
            data = data.read()
            data = json.loads(data.replace('loaded(',"")[:-1])['ResultSet']

            Cache.setCacheData(api_name, ctxt['cache_keys'], data)
        else:
            print "キャッシュありYA!"

        if 'UnitsWord' in data[u'Result'] and type(data['Result']['UnitsWord']) == list:
            ctxt.update({"suggest": data['Result']['UnitsWord']})
        else:
            ctxt.update({"suggest": [ctxt['kwd'],]})

        for i in xrange(0, int(data['@attributes']['totalResultsReturned'])):
            print
            datas.append(data['Result']['Item'][i])
                             
        # 必要なデータだけに生成
        return cls.exchangeYahooA(datas)



    @classmethod
    def createVC(cls, ctxt, sort=0):
        api_name = 'vc'
        cls.amazon_data = []
        cls.ponpare_data = []
        keyword = urllib.quote(ctxt['kwd'])
        param = urllib.urlencode({
                                 'token': settings.VALUE_TOKEN_ID,
                                 'keyword': ctxt['kwd'],
                                 'category':'',
                                 'ec_code': cls.EC_CODE,

                                 'sort_by':'',
                                 'sort_order':'',
                                 'format':'json',
                                 'results_per_page':50})
        
        
        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        if not datas:
            print "キャッシュなしVC"
            datas = urllib.urlopen(cls.VALUE_API_URL + param)
            datas = datas.read()
            datas = json.loads(datas)
            Cache.setCacheData(api_name, ctxt['cache_keys'], datas)
        else:
            print "キャッシュありVC"

        if datas['resultCount']:
            for data in datas['items']:

                if cls.EC_CODE_A == data['ecCode']:
                    cls.amazon_data.append(data)
                elif cls.EC_CODE_P == data['ecCode']:
                    cls.ponpare_data.append(data)
        return


    @classmethod
    def getPonpare(cls):
        return cls.exchangeVC(cls.ponpare_data)
    
    @classmethod
    def getAmazon(cls):
        return cls.exchangeVC(cls.amazon_data)


    @classmethod
    def getAll(cls, ctxt):

        cls.createVC(ctxt)

        return {'rakuten': cls.getRakten(ctxt),
                'yahoo_s': cls.getYahooS(ctxt),
                'yahoo_a': cls.getYahooA(ctxt),
                'amazon' : cls.getAmazon(),
                'ponpare': cls.getPonpare(),
                'jandata': cls.JAN_DATA
                }

    @classmethod
    def imgUrlFilter(cls, url):
        # ドメインでチェック
        return










class PriceCheck(object):
    def test():
        return









class Cache(object):
    TMP = 0
    @classmethod
    def setLastTime(cls, name):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set('lasttime:%s' % name, time.time())

    @classmethod
    def getLastTime(cls, name):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        return r.get('lasttime:%s' % name)
    
    @classmethod
    def getCache(cls, name, key):
        if cls.getLastTime(name) and (cls.getLastTime(name) - time.time()) < 1.0:
        # 現在時刻とキャッシュのラストタイム比較して、1秒以内だったらキャッシュ表示
            return cls.getCacheData(name, keys)

    @classmethod
    def setCacheData(cls, name, keys, data):
        # nameとkeyに、データをキャッシュ(24時間で解放)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        str = ''
        for key in keys:
            str += key
        print "キーのはず！",'%s:%s' % (name, str)
        result = r.setex('%s:%s' % (name, str), 36000, msgpack.packb(data))
        print "setしたよ！", result

    @classmethod
    def getCacheData(cls, name, keys):
        # nameとkeyに、キャッシュを読み込む
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        str = ''
        for key in keys:
            str += key
        print "キーのはず！",'%s:%s' % (name, str)
        result = r.get('%s:%s' % (name, key))
        if result:
            return msgpack.unpackb(result, encoding='utf-8')
