# encoding:utf-8

import settings
import hashlib
import urllib
import json

import redis
import time
import msgpack
import locale
import csv


class ApiUtill(object):

    @staticmethod
    def imageFilter(str):
        f = open('%s/ng_url.csv' % settings.STATIC_ROOT, 'rb')
        dataReader = csv.reader(f)
        for row in dataReader:
            if row[0] in str:
                return ""
            else:
                return str


    @staticmethod
    def callAPI(url, param):
        try:
            datas = urllib.urlopen(url + param)
            datas = datas.read()
            return datas
        except:
            return []

    @classmethod
    def makeStar(cls, num):
        str = ""
        for i in xrange(1,6):
            if i <= num:
                str += "★"
            else:
                str += "☆"
        return str
    @staticmethod
    def exchangeRakuten(datas):
        results = []
        locale.setlocale(locale.LC_NUMERIC, 'ja_JP')
        af_url = "http://c.af.moshimo.com/af/c/click?a_id=563064&p_id=54&pc_id=54&pl_id=616&url="
        for data in datas:
            data = data['Item']
            res = {"itemName":data['itemName'][:30],
                "itemPrice":locale.format('%d', data['itemPrice'], True),
                "itemPriceP":data['itemPrice'],
                "pointRate":data['pointRate'],
                "postageFlag":data['postageFlag'],
                "asurakuFlag":data['asurakuFlag'],
                "reviewAverage":data['reviewAverage'],
                "reviewCount":data['reviewCount'],
                "itemUrl":af_url+urllib.quote(data['itemUrl']),
                "shopName":data['shopName'],
                "ec":"rakuten",
                "reviewCnt":data['reviewCount'],
                "reviewAvg":int(round(data['reviewAverage'],0))}
            if data['mediumImageUrls']:
                res["imageUrl"] = data['mediumImageUrls'][0]['imageUrl']

            results.append(res)

        return results

    @classmethod
    def exchangePonpare(cls, datas):
        locale.setlocale(locale.LC_NUMERIC, 'ja_JP')
        results = []
        for data in datas:
            results.append({"itemName":data['title'][:30],
                           "itemPrice":locale.format('%d', data['price'], True),
                           "itemPriceP":data['price'],
                           "itemUrl":data['link'],
                           "imageUrl":data['imageFree']['url'],
                           "ec":"ponpare",
                           "shopName":data['subStoreName']}
                           )
        return results


    @classmethod
    def exchangeAmazon(cls, datas):
        locale.setlocale(locale.LC_NUMERIC, 'ja_JP')
        results = []
        for data in datas:

            results.append({"itemName":data['title'][:30],
                           "itemPrice":locale.format('%d', data['price'], True),
                           "itemPriceP":data['price'],
                           "itemUrl":data['link'],
                           "imageUrl":data['imageFree']['url'],
                           "ec":"amazon",
                           "shopName":data['subStoreName']}
                       )
        return results

    @classmethod
    def exchangeYahooS(cls, datas):

        locale.setlocale(locale.LC_NUMERIC, 'ja_JP')
        results = []
        for data in datas:
            category = ''
            for i in data['CategoryIdPath'].keys():
                if category:
                    continue
                if i == '_container':
                    continue
                if not category and 'CategoryIdPath' in data and data['CategoryIdPath'][i]['Id'] != '1':
                    category = data['CategoryIdPath'][i]['Id']


            results.append({"itemName":data['Name'][:30],
                           "itemPrice":locale.format('%d', int(data['Price']['_value']), True),
                           "itemPriceP":int(data['Price']['_value']),
                           "itemUrl":data['Url'],
                           "imageUrl":cls.imageFilter(data['ExImage']['Url']),
                           "jan": data['JanCode'],
                           "shopName": data['Store']['Name'],
                           "ec":"yahoo",
                           "reviewAvg":int(round(float(data['Review']['Rate']),0)),
                           "reviewCnt":data['Review']['Count'],
                           "reviewUrl":data['Review']['Url'],
                           "category":category
                           })
        return results

    @classmethod
    def exchangeYahooA(cls, datas):
        locale.setlocale(locale.LC_NUMERIC, 'ja_JP')
        results = []

        for data in datas:
            param = urllib.urlencode({
                                     'vc_url': data['AuctionItemUrl'],
                                     })

            results.append({"itemName":data['Title'][:30],
                            "itemUrl": settings.VC_Y_A_URL + param,
                            "imageUrl":data['Image'],
                            "shopName":"",
                            "ec":"yahoo_a",
                            "bids":data['Bids'],
                            "seller":data['Seller']['Id']
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
                    cls.JAN_DATA.append({
                        "jan":[data['jan']],
                        "imageUrl": data['imageUrl'],
                        "itemName": data['itemName'][:30],
                        "category": data['category']})


    @classmethod
    def getLowPrice(cls):
        for data in cls.amazon_data:
            continue


    @classmethod
    def getRakten(cls, ctxt, nocache=0, sort='standard', hits=20):
        api_name = 'rakuten'
        param = urllib.urlencode(
                        {'format': 'json',
                         'keyword': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                         'applicationId': settings.RAKUTEN_APP_ID,
                         'minPrice': ctxt['minPrice'] if 'minPrice' in ctxt else "",
                         'maxPrice': ctxt['maxPrice'] if 'maxPrice' in ctxt else "",
                         'imageFlag': '1',
                         'hits':hits,
                         'sort': sort if nocache or not ctxt['sort'] else "+itemPrice",
                         'postageFlag': ctxt['shipping']}
        )

        keys = ctxt['cache_keys']
        if ctxt['shipping']:
            keys.append(hashlib.sha224("shipping").hexdigest())
        keys.sort()
        datas = Cache.getCacheData(api_name, keys)
        if not datas or nocache:
            datas = ApiUtill.callAPI(settings.RAKUTEN_API_URL, param)
            datas = json.loads(datas)
            if not nocache:
                Cache.setCacheData(api_name, ctxt['cache_keys'], datas)

        # 必要なデータだけに生成
        if "Items" in datas:
            return ApiUtill.exchangeRakuten(datas['Items'])
        return []


    @classmethod
    def getYahooS(cls, ctxt, nocache=0, sort='', hits=30):
        api_name = 'yahoo_shopping'

        param_dict = {
                         'query': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                         'appid': settings.YAHOO_S_ID,
                         'affiliate_type':'vc',
                         'affiliate_id': settings.YAHOO_S_AF_ID,
                         'image_size':146,
                         'hits':hits,
                      }
        if ctxt['sort'] or sort == '+price':
            param_dict.update({'sort':'+price'})
        if ctxt['jan']:
            param_dict.update({'jan':ctxt['jan']})
        if 'minPrice' in ctxt and ctxt['minPrice']:
            param_dict.update({'price_from':ctxt['minPrice']})
        if 'maxPrice' in ctxt and ctxt['maxPrice']:
            param_dict.update({'price_to':ctxt['maxPrice']})
        if ctxt['shipping']:
            param_dict.update({'shipping':ctxt['shipping']})
        param = urllib.urlencode(param_dict)

        keys = ctxt['cache_keys']
        if ctxt['shipping']:
            keys.append(hashlib.sha224("shipping").hexdigest())
        keys.sort()
        datas = Cache.getCacheData(api_name, keys)

        result_datas = []

        if not datas or nocache:

            datas = ApiUtill.callAPI(settings.YAHOO_S_URL, param)

            j = json.loads(datas)

            if not u'Error' in json.loads(datas):
                datas = json.loads(datas)['ResultSet']
                if 0 < datas['totalResultsReturned'] and 'totalResultsReturned' in datas:
                    for i in xrange(0, int(datas['totalResultsReturned'])):
                        result_datas.append(datas[u'0']['Result'][u'%s' % i])

            # jan検索はキャッシュしない。
            if not nocache:
                Cache.setCacheData(api_name, ctxt['cache_keys'], result_datas)
            datas = result_datas

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
                             'aucminprice': ctxt['minPrice'] if 'minPrice' in ctxt else "",
                             'aucmaxprice': ctxt['maxPrice'] if 'maxPrice' in ctxt else "",
                             'sort': sort if nocache or not ctxt['sort'] else "cbids",
                             'buynow': ctxt['buynow'],
                             'item_status': ctxt['item_status'],
                             'store': ctxt['store']
                             # 'shipping': ctxt['shipping'], # 1：送料無料 デフォルトはなし
                             })
        keys = ctxt['cache_keys']
        if ctxt['buynow']:
            keys.append(hashlib.sha224("buynow").hexdigest())
        if ctxt['item_status']:
            keys.append(hashlib.sha224("item_status").hexdigest())
        if ctxt['store']:
            keys.append(hashlib.sha224("store").hexdigest())
        keys.sort()
        data = Cache.getCacheData(api_name, keys)

        datas = []

        if not data or nocache:
            data = ApiUtill.callAPI(settings.YAHOO_A_URL, param)
            data = json.loads(data.replace('loaded(',"")[:-1])['ResultSet']

            if not nocache:
                Cache.setCacheData(api_name, ctxt['cache_keys'], data)

        if 'UnitsWord' in data[u'Result'] and type(data['Result']['UnitsWord']) == list:
            ctxt.update({"suggest": data['Result']['UnitsWord']})
        else:
            if not nocache:
                ctxt.update({"suggest": [ctxt['kwd'],]})


        for i in xrange(0, int(data['@attributes']['totalResultsReturned'])):
            if int(data['@attributes']['totalResultsReturned']) == 1:
                datas.append(data['Result']['Item'])
            else:
                datas.append(data['Result']['Item'][i])

        # 必要なデータだけに生成
        return ApiUtill.exchangeYahooA(datas)



    @classmethod
    def createVC(cls, ctxt, nocache=0, sort='', sort_order='', hits=30):
        api_name = 'vc'
        amazon_data = []
        ponpare_data = []

        keyword = urllib.quote(ctxt['kwd'])
        param = urllib.urlencode({
                                 'token': settings.VALUE_TOKEN_ID,
                                 'keyword': ctxt['kwd'] if not ctxt['jan'] else ctxt['jan'],
                                 'category':'',
                                 'ec_code': cls.EC_CODE,

                                 'sort': sort if nocache or not ctxt['sort'] else "price",
                                 'sort_order':sort_order if nocache or not ctxt['sort'] else "asc",
                                 'format':'json',
                                 'results_per_page':hits})


        datas = Cache.getCacheData(api_name, ctxt['cache_keys'])
        if not datas or nocache:
            datas = ApiUtill.callAPI(settings.VALUE_API_URL, param)
            if datas:
                datas = json.loads(datas)
                if not nocache:
                    Cache.setCacheData(api_name, ctxt['cache_keys'], datas)

        if datas and datas['resultCount']:
            for data in datas['items']:

                if cls.EC_CODE_A == data['ecCode']:
                    amazon_data.append(data)
                elif cls.EC_CODE_P == data['ecCode']:
                    ponpare_data.append(data)
        #print "A&P",len(amazon_data), len(ponpare_data)
        return amazon_data, ponpare_data


    @classmethod
    def getPonpare(cls, datas):
        return ApiUtill.exchangePonpare(datas)

    @classmethod
    def getAmazon(cls, datas):
        return ApiUtill.exchangeAmazon(datas)


    @classmethod
    def getAll(cls, ctxt):
        #amazon_data, ponpare_data = cls.createVC(ctxt)

        return {'rakuten': cls.getRakten(ctxt),
                'yahoo_s': cls.getYahooS(ctxt),
#                'yahoo_a': cls.getYahooA(ctxt),
#                'amazon' : cls.getAmazon(amazon_data),
#                'ponpare': cls.getPonpare(ponpare_data),
                'jandata': cls.JAN_DATA
                }

    @classmethod
    def getPriceCheckData(cls, ctxt):
        #print "JANだよ！",ctxt["jan"]
        #amazon_data, ponpare_data = cls.createVC(ctxt, sort='price', nocache=1, sort_order='asc', hits=10)
        rakuten = cls.getRakten(ctxt, nocache=1, sort='+itemPrice', hits=10)
        yahoo_s = cls.getYahooS(ctxt, nocache=1, sort='+price', hits=10)
        #yahoo_a = cls.getYahooA(ctxt, nocache=1, sort='cbids')
        #amazon = cls.getAmazon(amazon_data)
        #ponpare = cls.getPonpare(ponpare_data)

        datas = {'rakuten_p': rakuten,
                'yahoo_s_p': yahoo_s,
                #'yahoo_a_p': yahoo_a,
        #        'amazon_p' : amazon,
        #        'ponpare_p': ponpare,
        }
        lowestPrice = {'1st_rakuten_p':rakuten[0] if rakuten and rakuten[0] else "",
                       '1st_yahoo_s_p':yahoo_s[0] if yahoo_s and yahoo_s[0] else "",
                       #'1st_yahoo_a_p':yahoo_a[0] if yahoo_a and yahoo_a[0] else "",
        #               '1st_amazon_p':amazon[0] if amazon and amazon[0] else "",
        #               '1st_ponpare_p':ponpare[0] if ponpare and ponpare[0] else "",
        }
        return cls.price_ranking(datas), lowestPrice


    @classmethod
    def price_ranking(cls, datas):
        list = []
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
        return int(x["itemPriceP"]) - int(y["itemPriceP"])

    @classmethod
    def imgUrlFilter(cls, url):
        # ドメインでチェック
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
        result = r.get('%s:%s' % (name, str))

        if result:
            return msgpack.unpackb(result, encoding='utf-8')
