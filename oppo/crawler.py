# -*- coding: utf-8 -*-
import json
import random
import time

import requests
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(os.path.split(curPath)[0])[0]
if 'app_proxy' not in rootPath:
    sys.path.append(rootPath + '/app_proxy')
sys.path.append(rootPath)
from oppo.uilts import param_sign
from utils import get_html
from oppo.format_data import fmt_data

headers = {
    'ch': '2101',
    'token': '-1',
    'cpu-arch': 'x86_64',
    'enter-id': '1',
    't': '1634181987218',
    'appversion': '8.6.4beta1',
    'id': '008796752816546///',
    # 'sg':'cec64454e8d4db01c246f2a8d6f720fb',
    # 'traceid'	:'fO7gECtn-1632922353215',
    'pkg-ver': '0',
    'accept': 'application/json; charset=UTF-8',
    # 'sign'	:'83600aa630d2583207b5bc6ded027d30',
    'pid': '001',
    'locale': 'zh-CN;CN',
    'appid': 'Android#001#CN',
    'ext-info': 'normal',
    'nw': '1',
    'ocp': '8968',
    'oak': 'cdb09c43063ea6bb',
    'user-agent': 'Android%2FMuMu%2F23%2F6.0.1%2FUNKNOWN%2F2%2F2101%2F86040%2F8.6.4beta1',
    'component': '86040/2',
    'iad': '3714665%2C600265%2C3621605',
    'ouid-limit-status': '0',
    'romver': '-1',
    'ocs': 'Android%2FMuMu%2F23%2F6.0.1%2FUNKNOWN%2F2%2FV417IR+release-keys%2F86040',
    'pr': '1',
    'accept-encoding': 'gzip'
}


def get_all_catagory():
    url = 'https://api-cn.store.heytapmobi.com/card/store/v4/cat/app?size=10&start=0'
    headers['sign'] = param_sign(headers, url)
    r = get_html(url=url, headers=headers, method=requests.get)
    print(r.text)
    return r.text


def get_category_app(card1_id, card2_id, page):
    url = 'https://api-cn.store.heytapmobi.com/card/store/v3/cat/resources/alg/1?cid={}&subId={}&req_id=&cType=1&size=10&start={}'.format(
        card1_id, card2_id, (int(page - 1) * 10))
    headers['sign'] = param_sign(headers, url)
    r = get_html(url=url, headers=headers, method=requests.get)
    print(r.text)
    return r.text


def app_detail(app_id):
    url = 'https://api-cn.store.heytapmobi.com/detail/v4/{}?query=1,2,3,4,5,6,7,8,9,10,12,15,16,17,19,20&source=1'.format(
        app_id)
    headers['sign'] = param_sign(headers, url)
    r = get_html(url=url, headers=headers, method=requests.get)
    print(r.text)
    return r.text


def start():
    cate_info = get_all_catagory()
    if not cate_info:
        print('catagory get error')
        return
    try:
        cata_list = json.loads(cate_info)['cards']
    except Exception as e:
        print(e)
        print('catagory get error')
        return
    for card in cata_list:
        card1_id = card['id']
        card1_name = card['name']
        card1_int = card.get('subCategories', [])
        for card2 in card1_int:
            card2_id = card2['id']
            card2_name = card2['name']
            page = 1
            next_page = True
            while next_page:
                app_info = get_category_app(card1_id, card2_id, page)
                try:
                    app_list = json.loads(app_info)['cards']
                    next_page = True if not json.loads(app_info)['isEnd'] else False
                except Exception as e:
                    print(e)
                    continue
                app_list = app_list if app_list else []
                page += 1
                for detail_card in app_list:
                    for app in detail_card['apps']:
                        app_id = app['appId']
                        app_detail_info = app_detail(app_id)
                        try:
                            app_detail_info = json.loads(app_detail_info)
                        except Exception as e:
                            print(e)
                            continue
                        fmt_data(app_detail_info, card1_name, card2_name)
                        time.sleep(10 * random.random())


if __name__ == '__main__':
    start()
