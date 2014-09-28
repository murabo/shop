# encoding:utf-8
from django.utils.safestring import mark_safe

from pwprice.api import BridgeApi
from django import template
register = template.Library()

@register.filter
def getTest(num, args):
    amazon = args['amazon']
    rakuten = args['rakuten']
    yahoo_s = args['yahoo_s']
    ponpare = args['ponpare']
    yahoo_a = args['yahoo_a']
    if not len(amazon) and not len(rakuten) and not len(yahoo_a) and not len(yahoo_s) and not len(ponpare):
        return
    print len(amazon), len(rakuten), len(yahoo_s), len(ponpare), len(yahoo_a)
    # Amazon 商品画像、商品名
    name_image_tag = u'''
    <td class="item">
    <div class="img">
    <img src="%s" alt="画像" height='45' width='45'/>
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
    #print tag

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

    print s
    return mark_safe(s)
