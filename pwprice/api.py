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

class ApiUtill(object):
    @staticmethod
    def callAPI(url, param):
        
        print "callAPI:",url + param
        datas = urllib.urlopen(url + param)
        
        datas = datas.read()
        return datas

    @staticmethod
    def exchangeRakuten(datas):
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
                "itemUrl":data['itemUrl'],
                "shopName":data['shopName'],
                "ec":"rakuten"}
            if data['mediumImageUrls']:
                res["imageUrl"] = data['mediumImageUrls'][0]['imageUrl']
            
            results.append(res)
        
        return results

    @classmethod
    def exchangePonpare(cls, datas):
        results = []
        for data in datas:
            results.append({"itemName":data['title'],
                           "itemPrice":data['price'],
                           "itemUrl":data['link'],
                           "imageUrl":data['imageFree']['url'],
                           "ec":"ponpare"}
                           )
        return results


    @classmethod
    def exchangeAmazon(cls, datas):
        results = []
        for data in datas:
            
            results.append({"itemName":data['title'],
                           "itemPrice":data['price'],
                           "itemUrl":data['link'],
                           "imageUrl":data['imageFree']['url'],
                           "ec":"amazon"}
                       )
        return results

    @classmethod
    def exchangeYahooS(cls, datas):
        results = []
        for data in datas:

            results.append({"itemName":data['Name'],
                           "itemPrice":data['Price']['_value'],
                           "itemUrl":data['Url'],
                           "imageUrl":data['ExImage']['Url'],
                           "jan": data['JanCode'],
                           "shopName": data['Store']['Name'],
                           "ec":"yahoo"
                           })
        return results

    @classmethod
    def exchangeYahooA(cls, datas):
        results = []
    
        for data in datas:
            param = urllib.urlencode({
                                     'vc_url': data['AuctionItemUrl'],
                                     })

            results.append({"itemName":data['Title'],
                            "itemUrl": settings.VC_Y_A_URL + param,
                            "imageUrl":data['Image'],
                            "shopName":"",
                            "ec":"yahoo_a"
                            })
        return results



class BridgeApi(object):

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


    @classmethod
    def getLowPrice(cls):
        print "AMA",len(cls.amazon_data)
        for data in cls.amazon_data:
            # print data['janCode']
            continue


    @classmethod
    def getRakten(cls, ctxt, nocache=0, sort='', hits=30):
        api_name = 'rakuten'
        param = urllib.urlencode(
                        {'format': 'json',
                         'keyword': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                         'applicationId': settings.RAKUTEN_APP_ID,
                         'minPrice': ctxt['minPrice'],
                         'maxPrice': ctxt['maxPrice'],
                         'imageFlag': '1',
                         'hits':hits,
                         'sort': sort}
        )

        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        if not datas or nocache:
            print "キャッシュなしR"
            datas = ApiUtill.callAPI(settings.RAKUTEN_API_URL, param)
            datas = json.loads(datas)
            Cache.setCacheData(api_name, ctxt['cache_keys'], datas)
        else:
            print "キャッシュありR"

        # 必要なデータだけに生成
        return ApiUtill.exchangeRakuten(datas['Items'])




    @classmethod
    def getYahooS(cls, ctxt, nocache=0, sort='', hits=50):
        api_name = 'yahoo_shopping'
        param = urllib.urlencode(
                             {
                                 'query': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                                 'appid': settings.YAHOO_S_ID,
                                 'affiliate_type':'vc',
                                 'affiliate_id': settings.YAHOO_S_AF_ID,
                                 'jan': ctxt['jan'] if ctxt['jan'] else '',
                                 'image_size':76,
                                 'category_id':'',
                                 'price_from': ctxt['minPrice'],
                                 'price_to': ctxt['maxPrice'],
                                 'hits':hits,
                                 'sort':sort,
                                  # 'shipping': ctxt['shipping'], # 1：送料無料 デフォルトはなし
                             })

        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        result_datas = []

        print "getYAHOO!S!",ctxt["jan"]
        if ctxt["jan"]:
            print "JAN!!YAHOO"

        if not datas or nocache:
            print "キャッシュなしorJAN検索"

            datas = ApiUtill.callAPI(settings.YAHOO_S_URL, param)
            datas = json.loads(datas)['ResultSet']
            if 0 < datas['totalResultsReturned'] and 'totalResultsReturned' in datas:
                for i in xrange(0, int(datas['totalResultsReturned'])):
                    result_datas.append(datas[u'0']['Result'][u'%s' % i])

            # jan検索はキャッシュしない。
            if not ctxt['jan']:
                Cache.setCacheData(api_name, ctxt['cache_keys'], result_datas)
            datas = result_datas
            for d in datas:
                print "@@@@@@@@@@@@@@@", d

        else:
            print "キャッシュありS",

        cls.YAHOO_DATA = ApiUtill.exchangeYahooS(datas)
        cls.createJanImgMap()
        # 必要なデータだけに生成
        return ApiUtill.exchangeYahooS(datas)


    @classmethod
    def getYahooA(cls, ctxt, nocache=0, sort=''):
        api_name = 'yahoo_auctions'
        param = urllib.urlencode(
                             {
                             'query': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                             'appid': settings.YAHOO_A_ID,
                             'output':'json',
                             'category_id':'',
                             'aucminprice': ctxt['minPrice'],
                             'aucmaxprice': ctxt['maxPrice'],
                             'item_status':0, #0 ：指定なし,1 ：新品
                             'sort':sort,
                             # 'shipping': ctxt['shipping'], # 1：送料無料 デフォルトはなし
                             })


        data = Cache.getCacheData(api_name, ctxt['cache_keys'])
        
        datas = []
        if not data or nocache:
            print "キャッシュなしYA!"
            data = ApiUtill.callAPI(settings.YAHOO_A_URL, param)
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
        return ApiUtill.exchangeYahooA(datas)



    @classmethod
    def createVC(cls, ctxt, nocache=0, sort='', sort_order='', hits=50):
        api_name = 'vc'
        amazon_data = []
        ponpare_data = []
        
        keyword = urllib.quote(ctxt['kwd'])
        param = urllib.urlencode({
                                 'token': settings.VALUE_TOKEN_ID,
                                 'keyword': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                                 'category':'',
                                 'ec_code': cls.EC_CODE,
                                 'sort_by':sort,
                                 'sort_order':sort_order,
                                 'format':'json',
                                 'results_per_page':hits})
        
        
        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        if not datas or nocache:
            print "キャッシュなしVC"
            datas = ApiUtill.callAPI(settings.VALUE_API_URL, param)
            datas = json.loads(datas)
            Cache.setCacheData(api_name, ctxt['cache_keys'], datas)
        else:
            print "キャッシュありVC"

        if datas['resultCount']:
            for data in datas['items']:

                if cls.EC_CODE_A == data['ecCode']:
                    amazon_data.append(data)
                elif cls.EC_CODE_P == data['ecCode']:
                    ponpare_data.append(data)
        print "A&P",len(amazon_data), len(ponpare_data)
        return amazon_data, ponpare_data


    @classmethod
    def getPonpare(cls, datas):
        return ApiUtill.exchangePonpare(datas)
    
    @classmethod
    def getAmazon(cls, datas):
        return ApiUtill.exchangeAmazon(datas)


    @classmethod
    def getAll(cls, ctxt):

        amazon_data, ponpare_data = cls.createVC(ctxt)

        return {'rakuten': cls.getRakten(ctxt, sort='standard'),
                'yahoo_s': cls.getYahooS(ctxt),
                'yahoo_a': cls.getYahooA(ctxt),
                'amazon' : cls.getAmazon(amazon_data),
                'ponpare': cls.getPonpare(ponpare_data),
                'jandata': cls.JAN_DATA
                }

    @classmethod
    def getPriceCheckData(cls, ctxt):
        amazon_data, ponpare_data = cls.createVC(ctxt, sort='price', nocache=1, sort_order='asc', hits=10)
        rakuten = cls.getRakten(ctxt, nocache=1, sort='+itemPrice', hits=10)
        yahoo_s = cls.getYahooS(ctxt, nocache=1, sort='+price', hits=10)
        yahoo_a = cls.getYahooA(ctxt, nocache=1, sort='cbids')
        amazon = cls.getAmazon(amazon_data)
        ponpare = cls.getPonpare(ponpare_data)
        
        datas = {'rakuten_p': rakuten,
                'yahoo_s_p': yahoo_s,
                'yahoo_a_p': yahoo_a,
                'amazon_p' : amazon,
                'ponpare_p': ponpare,
#                'jandata_p': cls.JAN_DATA,

        }
        lowestPrice = {'1st_rakuten_p':rakuten[0] if rakuten and rakuten[0] else "",
                       '1st_yahoo_s_p':yahoo_s[0] if yahoo_s and yahoo_s[0] else "",
                       '1st_yahoo_a_p':yahoo_a[0] if yahoo_a and yahoo_a[0] else "",
                       '1st_amazon_p':amazon[0] if amazon and amazon[0] else "",
                       '1st_ponpare_p':ponpare[0] if ponpare and ponpare[0] else "",}
        return cls.price_ranking(datas), lowestPrice
    

    @classmethod
    def price_ranking(cls, datas):
        list = []
        del_list=[]
        for k, v in datas.items():
            list.extend(v)

        for i, d in enumerate(list):
            if not "itemPrice" in d:
                list.pop(i)

        list.sort(cls.price_sort)
        if len(list) > 10:
            list = list[:10]
        return list


    @classmethod
    def price_sort(cls, x, y):
        return int(x["itemPrice"]) - int(y["itemPrice"])

    @classmethod
    def imgUrlFilter(cls, url):
        # ドメインでチェック
        return










class PriceCheck(object):
    @classmethod
    def test(cls,ctxt):
        #print "jan ys 検索：", BridgeApi.getYahooS(ctxt, sort='+price',hits=10)
        return

    @classmethod
    def getAll(cls, ctxt):
        # 全APIから価格順で10件ずつ取得
        # YAHOOS 10件取得
        # YAHOOA 10件取得
        # 楽天    10件取得
        # VC(ama&pon)10件取得
        # 上記の各サービス毎の1件目を最安値とする。
        # 上記を一つにし、価格でソートして10件をランキングとする。
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

        result = r.setex('%s:%s' % (name, str), 36000, msgpack.packb(data))


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
