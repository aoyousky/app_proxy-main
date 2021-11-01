# -*- coding: utf-8 -*-
import requests, time
import logging
from logging import StreamHandler
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def get_html(headers, url, method, data=None, retry_times=5, timeout=10, proxies=False):
    """
    请求数据
    :params headers: 请求头
    :params url: 请求链接
    :params method: 请求方法 `requests.get`|`requests.post`
    :params data: post数据
    :params proxies: 代理地址和端口
    """
    if proxies:
        host_address = proxies if proxies else {}
        logger.debug('请求的代理地址为:代理%s,地址为：%s', proxies, host_address)
        proxies = {
            "http": host_address,
            "https": host_address} if host_address else {}
    else:
        proxies = {}
    r = ''
    for _ in range(retry_times):
        try:
            r = method(headers=headers, url=url, timeout=timeout, data=data, proxies=proxies)
            break
        except requests.exceptions.Timeout:
            logger.error('requests timeout')
            time.sleep(1)
            timeout += 2
            continue
        except Exception as e:
            logger.error('other exceptions:' + str(e))
            logger.error(url)
            timeout += 2
            time.sleep(1)
            continue
    if not r:
        if hasattr(r, 'text'):
            logger.error('不正常返回 http status : ' + str(r.status_code) + '地址:' + url)
            logger.debug(r.text)
        return r
    return r