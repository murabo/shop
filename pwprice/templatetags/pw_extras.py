# encoding:utf-8
from django.utils.safestring import mark_safe

from pwprice.api import BridgeApi
from django import template
register = template.Library()
import urllib

@register.filter
def getMatrix(num, args):
    amazon = args['amazon']
    rakuten = args['rakuten']
    yahoo_s = args['yahoo_s']
    ponpare = args['ponpare']
    yahoo_a = args['yahoo_a']
    if not len(amazon) and not len(rakuten) and not len(yahoo_a) and not len(yahoo_s) and not len(ponpare):
        return
    # Amazon 商品画像、商品名
    name_image_tag = u'''
    <td class="item">
    <div class="img">
    <img src="%s" alt="画像" height='76' width='76'/>
    </div>
    <a href='%s'><div class="body">%s</div></a>
    </td>'''
    tag = u'''<table class="resultItems">
              <tr>'''
    if  int(num) < len(amazon) and 'imageUrl' in amazon[int(num)]:
        tag += name_image_tag % (amazon[int(num)]['imageUrl'], amazon[int(num)]['itemUrl'], amazon[int(num)]['itemName'])
    else:
        tag += u'<td class="item"></td>'

    if  int(num) < len(rakuten) and 'imageUrl' in rakuten[int(num)]:
            tag += name_image_tag % (rakuten[int(num)]['imageUrl'], rakuten[int(num)]['itemUrl'], rakuten[int(num)]['itemName'])
    else:
        tag += u'<td class="item"></td>'
    if  int(num) < len(yahoo_s):
        tag += name_image_tag % (yahoo_s[int(num)]['imageUrl'], yahoo_s[int(num)]['itemUrl'], yahoo_s[int(num)]['itemName'])
    else:
        tag += u'<td class="item"></td>'
    if  int(num) < len(ponpare):
        tag += name_image_tag % (ponpare[int(num)]['imageUrl'], ponpare[int(num)]['itemUrl'], ponpare[int(num)]['itemName'])
    else:
        tag += u'<td class="item"></td>'
    if  int(num) < len(yahoo_a):
        tag += name_image_tag % (yahoo_a[int(num)]['imageUrl'], yahoo_a[int(num)]['itemUrl'], yahoo_a[int(num)]['itemName'])
    else:
        tag += u'<td class="item"></td>'
    tag += u'</tr>'

    price_tag = u'''
    <td>
    <p class="priceText">販売価格<span>%s円</span></p>
    </td>
    '''
    tag += u'<tr>'

    if amazon and int(num) < len(amazon):
        tag += price_tag % (amazon[int(num)]['itemPrice'])
    else:
        tag += u'<td></td>'
    if rakuten and int(num) < len(rakuten):
        tag += price_tag % (rakuten[int(num)]['itemPrice'])
    else:
        tag += u'<td></td>'
    if yahoo_s and int(num) < len(yahoo_s):
        tag += price_tag % (yahoo_s[int(num)]['itemPrice'])
    else:
        tag += u'<td></td>'
    if ponpare and int(num) < len(ponpare):
        tag += price_tag % (ponpare[int(num)]['itemPrice'])
    else:
        tag += u'<td></td>'
    if yahoo_a and int(num) < len(yahoo_a):
        tag += u'<td></td>'
    else:
        tag += u'<td></td>'
    tag += u'</tr>'
    tag += u'<tr>'
    if int(num) < len(amazon) and amazon :
        tag += u'<td><a href="%s" class="link">最新価格のチェックはこちら</a></td>' % (amazon[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(rakuten) and rakuten :
        tag += u'<td><a href="%s" class="link">最新価格のチェックはこちら</a></td>' % (rakuten[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_s) and yahoo_s:
        tag += u'<td><a href="%s" class="link">最新価格のチェックはこちら</a></td>' % (yahoo_s[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(ponpare) and ponpare:
        tag += u'<td><a href="%s" class="link">最新価格のチェックはこちら</a></td>' % (ponpare[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_a) and yahoo_a:
        tag += u'<td><a href="%s" class="link">最新価格のチェックはこちら</a></td>' % (yahoo_a[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    tag += u'</tr>'

    tag += u'<tr>'
    if int(num) < len(amazon) and amazon :
        tag += u'<td><a href="/" ><img src="/static/images/banner/amazon_p193x40.gif" /></a></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(rakuten) and rakuten :
        tag += u'<td><a href="/" ><img src="/static/images/banner/rakuten_p193x40.gif" /></a></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_s) and yahoo_s:
        tag += u'<td><a href="/" ><img src="/static/images/banner/yahoo_p193x40.gif" /></a></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(ponpare) and ponpare:
        tag += u'<td><a href="/" ><img src="/static/images/banner/ponpare_p193x40.gif" /></a></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_a) and yahoo_a:
        tag += u'<td><a href="/" ><img src="/static/images/banner/yauc_p193x40.gif" /></a></td>'
    else:
        tag += u'<td></td>'
    tag += u'</tr>'

    tag += u'<tr>'
    if int(num) < len(amazon) and amazon :
        tag += u'<td class="prBx"></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(rakuten) and rakuten :
        tag += u'<td class="prBx"><p class="pr"><span>楽天カードの無料登録</span></br>で実質<em>5000円</em>の値引き</p></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_s) and yahoo_s:
        tag += u'<td class="prBx"></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(ponpare) and ponpare:
        tag += u'<td class="prBx"><p class="pr"><span>リクルートカードの無料登録</span></br>で実質<em>5000円</em>の値引き</p></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_a) and yahoo_a:
        tag += u'<td class="prBx"></td>'
    else:
        tag += u'<td></td>'
    tag += u'</tr>'

    tag += u'<tr>'
    if int(num) < len(amazon) and amazon :
        tag += u'<td><a href="%s" class="link">送料・支払い方法</a></td>' % (amazon[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(rakuten) and rakuten :
        tag += u'<td><a href="%s" class="link">送料・支払い方法</a></td>' % (rakuten[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_s) and yahoo_s:
        tag += u'<td><a href="%s" class="link">送料・支払い方法</a></td>' % (yahoo_s[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(ponpare) and ponpare:
        tag += u'<td><a href="%s" class="link">送料・支払い方法</a></td>' % (ponpare[int(num)]['itemUrl'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_a) and yahoo_a:
        tag += u'<td></td>'
    else:
        tag += u'<td></td>'
    tag += u'</tr>'

    tag += u'<tr>'
    if int(num) < len(amazon) and amazon :
        tag += u'<td></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(rakuten) and rakuten :
        tag += u'<td> <img src="/static/images/star/%s.gif" /> <a href="%s" class="link">(%s件)</a></td>' % (rakuten[int(num)]['reviewAvg'],rakuten[int(num)]['itemUrl'],rakuten[int(num)]['reviewCnt'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_s) and yahoo_s:
        tag += u'<td><img src="/static/images/star/%s.gif" /><a href="%s" class="link">(%s件)</a></td>' % (yahoo_s[int(num)]['reviewAvg'], yahoo_s[int(num)]['reviewUrl'], yahoo_s[int(num)]['reviewCnt'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(ponpare) and ponpare:
        tag += u'<td></td>'
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_a) and yahoo_a:
        tag += u'<td>入札&nbsp;%s件</td>' % yahoo_a[int(num)]['bids']
    else:
        tag += u'<td></td>'
    tag += u'</tr>'

    tag += u'<tr>'
    if int(num) < len(amazon) and amazon :
        tag += u'<td>%s</td>' % (amazon[int(num)]['shopName'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(rakuten) and rakuten :
        tag += u'<td>%s</td>' % (rakuten[int(num)]['shopName'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_s) and yahoo_s:
        tag += u'<td>%s</td>' % (yahoo_s[int(num)]['shopName'])
    else:
        tag += u'<td></td>'
    if int(num) < len(ponpare) and ponpare:
        tag += u'<td>%s</td>' % (ponpare[int(num)]['shopName'])
    else:
        tag += u'<td></td>'
    if  int(num) < len(yahoo_a) and yahoo_a:
        tag += u'<td>%s</td>' % (yahoo_a[int(num)]['seller'])
    else:
        tag += u'<td></td>'
    tag += u'</tr>'


    last_tag = u'</table><!-- /.resultItems -->'
    tag += last_tag

    return mark_safe(tag)

    '''
    <tr>
    <td>
    <p class="point">ポイント1%</p>
    </td>
    <td>
    <p class="point">ポイント1%</p>
    </td>
    <td>
    <p class="point">ポイント1%</p>
    </td>
    <td>
    <p class="point">ポイント1%</p>
    </td>
    <td>
    <p class="point">ポイント1%</p>
    </td>
    </tr>
    <tr>
    <td>
    <p>獲得ポイント178</p>
    </td>
    <td>
    <p>獲得ポイント178</p>
    </td>
    <td>
    <p>獲得ポイント178</p>
    </td>
    <td>
    <p>獲得ポイント178</p>
    </td>
    <td>
    <p>獲得ポイント178</p>
    </td>
    </tr>
    <tr>
    <td class="prBx">
    <p class="pr"><span>楽天カードの無料登録</span></br>で実質<em>5000円</em>の値引き</p>
    </td>
    <td class="prBx">
    <p class="pr"><span>楽天カードの無料登録</span></br>で実質<em>5000円</em>の値引き</p>
    </td>
    <td class="prBx">
    <p class="pr"><span>楽天カードの無料登録</span></br>で実質<em>5000円</em>の値引き</p>
    </td>
    <td class="prBx">
    <p class="pr"><span>楽天カードの無料登録</span></br>で実質<em>5000円</em>の値引き</p>
    </td>
    <td class="prBx">
    <p class="pr"><span>楽天カードの無料登録</span></br>で実質<em>5000円</em>の値引き</p>
    </td>
    </tr>
    <tr>
    <td class="option">
    <span class="tag card">カード</span>
    <span class="tag point">翌日は移送</span>
    <span class="tag postage">送料無料</span>
    </td>
    <td class="option">
    <span class="tag card">カード</span>
    <span class="tag point">翌日は移送</span>
    <span class="tag postage">送料無料</span>
    </td>
    <td class="option">
    <span class="tag card">カード</span>
    <span class="tag point">翌日は移送</span>
    <span class="tag postage">送料無料</span>
    </td>
    <td class="option">
    <span class="tag card">カード</span>
    <span class="tag point">翌日は移送</span>
    <span class="tag postage">送料無料</span>
    </td>
    <td class="option">
    <span class="tag card">カード</span>
    <span class="tag point">翌日は移送</span>
    <span class="tag postage">送料無料</span>
    </td>
    </tr>
    <tr>
    <td>
    <p class="linkCol">送料・支払い方法</p>
    <p class="star">★★★★★★(14件)</p>
    <p>パナソニック</p>
    </td>
    <td>
    <p class="linkCol">送料・支払い方法</p>
    <p class="star">★★★★★★(14件)</p>
    <p>パナソニック</p>
    </td>
    <td>
    <p class="linkCol">送料・支払い方法</p>
    <p class="star">★★★★★★(14件)</p>
    <p>パナソニック</p>
    </td>
    <td>
    <p class="linkCol">送料・支払い方法</p>
    <p class="star">★★★★★★(14件)</p>
    <p>パナソニック</p>
    </td>
    <td>
    <p class="linkCol">送料・支払い方法</p>
    <p class="star">★★★★★★(14件)</p>
    <p>パナソニック</p>
    </td>
    </tr>
        </table><!-- /.resultItems -->'''

    return mark_safe(s)


@register.filter
def urlEncode(param,key=""):

    key = urllib.quote(key)
    return mark_safe(urllib.quote(param+key))

@register.filter
def urlEncodeRA(param,key=""):
    print "エンコード楽天"
    print key
    print type(unicode(key, "utf-8"))
    print urllib.quote(param+urllib.quote(unicode(key, "utf-8").encode('euc-jp')))
    key = urllib.quote(unicode(key, "utf-8").encode('euc-jp'))
    return mark_safe(urllib.quote(param+key))

@register.filter
def getEcImg(ec):
    if ec == 'yahoo':
        return "/static/images/block2/yahoo135x32.gif"
    if ec == 'rakuten':
        return "/static/images/block2/rakuten135x32.gif"
    if ec == 'amazon':
        return "/static/images/block2/amazon135x32.gif"
    if ec == 'yahoo_a':
        return "/static/images/block2/yahooauc135x32.gif"
    if ec == 'ponpare':
        return "/static/images/block2/ponpar135x32.gif"