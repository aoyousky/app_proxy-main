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
from format_data import fmt_data
from urllib.parse import urlencode
from utils import get_html

headers = {
    'user-agent':'AndroidAppStore%2F10+%28Linux%3B+U%3B+Android+10%3B+Pixel+2+Build%2FQQ3A.200805.001%29',
    # content-type	application/x-www-form-urlencoded; charset=UTF-8
    # content-length	1840
    'accept-encoding':'gzip'
}

def get_all_catagory():
    url = 'https://main.appstore.vivo.com.cn/categories/info?screensize=1080_1794&plateformVersion=0&apps_per_page=20&app_version=1902&nt=WIFI&plateformVersionName=null&req_id=1&abtest=0&trace_type=4-0&categoriy_type=1&pictype=webp&model=Pixel+2&platApkVer=0&id=1&arCore=1&trace_pkg=com.google.android.apps.nexuslauncher&density=2.625&elapsedtime=459131510&an=10&cfrom=52&cs=0&plat_key_ver=&vcType=UNKNOW_CARD&platApkVerName=null&u=1234567890&av=29&page_index=1&imei=012345678987654&build_number=QQ3A.200805.001&patch_sup=1&s=2%7C2116874761'
    r = get_html(method=requests.get, headers=headers, url=url)
    if not r:
        return
    return r.text

def get_catagory_list(cata_id, page, append=True):
    data = {
        'screensize': '1080_1794',
        'plateformVersion': '0',
        'apps_per_page': '20',
        'app_version': '1902',
        'nt': 'WIFI',
        'plateformVersionName': 'null',
        'req_id': '1_100',
        'abtest': '0',
        'trace_type': '4-0',
        'pictype': 'webp',
        'model': 'Pixel 2',
        'platApkVer': '0',
        'id': str(cata_id),
        'arCore': '1',
        'order': '1',
        'trace_pkg': 'com.google.android.apps.nexuslauncher',
        'isParent': '1',
        'density': '2.625',
        'elapsedtime': '459654212',
        'an': '10',
        'cfrom': '66',
        'cs': '0',
        'plat_key_ver':'',
        'vcType': 'UNKNOW_CARD',
        'platApkVerName': 'null',
        'u': '1234567890',
        'av': '29',
        'page_index': str(page),
        'imei': '012345678987654',
        'build_number': 'QQ3A.200805.001',
        'patch_sup': '1',

        's': '2|1315960247'
    }
    if append:
        data['append'] = '1'
    else:
        data['isParent'] = '2'
    url = 'https://main.appstore.vivo.com.cn/categories/apps?' + urlencode(data)
    r = get_html(method=requests.get, headers=headers, url=url)
    if not r:
        return
    return r.text


def get_detail(app_id):
    data = {
        'screensize': '1080_1794',
        'plateformVersion': '0',
        'app_version': '1902',
        'nt': 'WIFI',
        'need_comment': '0',
        'kst': '0',
        'plateformVersionName': 'null',
        'abtest': '0',
        'trace_type': '4-0',
        'pictype': 'webp',
        'pos': '2',
        'model': 'Pixel 2',
        'platApkVer': '0',
        'id': str(app_id),
        'arCore': '1',
        'versioncode': '1',
        'trace_pkg': 'com.google.android.apps.nexuslauncher',
        'density': '2.625',
        'elapsedtime': '818374',
        'recom_reqid': 'I4fYXqnkHY,appstore,appstore.idx.mix3,2899611,92057,e791bbc6f1e241718275e39f985ed86d,123,0.000956,0.023402,,183.589508,0.03921926737905181,,,vivo_as_129,0,012345678987654,0,0,0,1,,0,4.296328,,,1544,,8.100000,,,22,vivo_rerank_002,,1.000000'
    }
    url = 'https://info.appstore.vivo.com.cn/port/package/?' + urlencode(data)
    r = get_html(method=requests.get, headers=headers, url=url)
    if not r:
        return
    return r.text

def start():
    cata_info = get_all_catagory()
    try:
        cata_list = json.loads(cata_info)['value']
    except Exception as e:
        print(e)
        return
    for cata_list_info in cata_list:
        if 'child' not in cata_list_info:
            continue
        cata_id = cata_list_info.get('id', '')
        cat_lev1 = cata_list_info.get('title_zh', '')
        # print(cata_id, cat_lev1)
        cata_app_info = get_catagory_list(cata_id, 1)
        # print(cata_app_info)
        try:
            cata_app_info = json.loads(cata_app_info)
        except Exception as e:
            print(e)
            print(cata_app_info)
            continue
        second_cata_list = cata_app_info['secondType']
        for second_cata in second_cata_list:
            cat_lev2 = second_cata['typeName']
            cat_lev2_id = second_cata['id']
            # print(cata_id, cat_lev1, cat_lev2, cat_lev2_id)
            page = 1
            next_page = True
            while next_page:
                app_list_info = get_catagory_list(cat_lev2_id, page, False)
                # print(app_list_info)
                try:
                    app_list = json.loads(app_list_info)['value']
                    total_page = json.loads(app_list_info)['maxPage']
                except Exception as e:
                    print(e)
                    print(app_list_info)
                    next_page = False
                    continue
                page +=1
                if page >= total_page:
                    next_page = False
                for app_info in app_list:
                    app_id = app_info.get('id','')
                    app_detail_info = get_detail(app_id)
                    try:
                        app_detail = json.loads(app_detail_info)['value']
                    except Exception as e:
                        print(e)
                        print(app_detail_info)
                        next_page = False
                        continue
                    print(app_info, app_detail, cat_lev1, cat_lev2)
                    fmt_data(app_info, app_detail, cat_lev1, cat_lev2)
                    time.sleep(10*random.random())


if __name__ == '__main__':
    start()