# -*- coding: utf-8 -*-
import hashlib, time
import requests
from utils import get_html


def param_sign(headers, url):
    md5 = hashlib.md5()
    md5.update('cdb09c43063ea6bb08f4fe8a43775179bdc58acb383220be'.encode('utf-8'))
    text = headers['ocs'] + headers['t'] + headers['id'] + \
           url.split('?')[0].split('com')[-1] + url.split('?')[-1]
    md5.update(text.encode('utf-8'))
    md5.update(str(
        len('cdb09c43063ea6bb08f4fe8a43775179bdc58acb383220be' + text)).encode('utf-8'))
    md5.update(
        'STORENEWMIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBANYFY/UJGSzhIhpx6YM5KJ9yRHc7YeURxzb9tDvJvMfENHlnP3DtVkOIjERbpsSd76fjtZnMWY60TpGLGyrNkvuV40L15JQhHAo9yURpPQoI0eg3SLFmTEI/MUiPRCwfwYf2deqKKlsmMSysYYHX9JiGzQuWiYZaawxprSuiqDGvAgMBAAECgYEAtQ0QV00gGABISljNMy5aeDBBTSBWG2OjxJhxLRbndZM81OsMFysgC7dq+bUS6ke1YrDWgsoFhRxxTtx/2gDYciGp/c/h0Td5pGw7T9W6zo2xWI5oh1WyTnn0Xj17O9CmOk4fFDpJ6bapL+fyDy7gkEUChJ9+p66WSAlsfUhJ2TECQQD5sFWMGE2IiEuz4fIPaDrNSTHeFQQr/ZpZ7VzB2tcG7GyZRx5YORbZmX1jR7l3H4F98MgqCGs88w6FKnCpxDK3AkEA225CphAcfyiH0ShlZxEXBgIYt3V8nQuc/g2KJtiV6eeFkxmOMHbVTPGkARvt5VoPYEjwPTg43oqTDJVtlWagyQJBAOvEeJLno9aHNExvznyD4/pR4hec6qqLNgMyIYMfHCl6d3UodVvC1HO1/nMPl+4GvuRnxuoBtxj/PTe7AlUbYPMCQQDOkf4sVv58tqslO+I6JNyHy3F5RCELtuMUR6rG5x46FLqqwGQbO8ORq+m5IZHTV/Uhr4h6GXNwDQRh1EpVW0gBAkAp/v3tPI1riz6UuG0I6uf5er26yl5evPyPrjrD299L4Qy/1EIunayC7JYcSGlR01+EDYYgwUkec+QgrRC/NstV'.encode(
            'utf-8'))
    print(md5.hexdigest())
    return md5.hexdigest()


def download_apk(apk_link):
    headers = {
        'ch': '2101',
        'token': '-1',
        'cpu-arch': 'x86_64',
        'enter-id': '1',
        't': str(int(time.time())) + '218',
        'appversion': '8.6.4beta1',
        'id': '008796752816546///',
        # 'sg':'cec64454e8d4db01c246f2a8d6f720fb',
        # 'traceid'	:'fO7gECtn-1632922353215',
        'pkg-ver': '0',
        # 'accept': 'application/json; charset=UTF-8',
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
        'accept-encoding': 'gzip',
        'Connection': 'Keep-Alive'
    }
    apk_link += '?bs=1&ref=100&type=1'
    headers['sign'] = param_sign(headers, apk_link)
    r = get_html(url=apk_link, headers=headers, method=requests.get)
    if not r:
        return
    return r.content


def download_save_apk(save_path, apk_link):
    if not apk_link or not save_path:
        return
    apk_content = download_apk(apk_link)
    if not apk_content:
        return
    with open(save_path, 'wb') as f:
        f.write(apk_content)
        file_name = f.name
    f.close()
    return file_name
