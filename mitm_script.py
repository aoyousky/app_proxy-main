# -*- coding: utf-8 -*-

import json
import os
import re
from urllib.parse import urlparse
import hashlib


class HttpProxy:
    def __init__(self):
        self.domain_set = set()
        self.info_list = []
        self.path = os.getcwd() + '/request'

    def error(self, flow):
        print('error', flow.request.url)
        self.extract_domain(flow)

    def http_connect(self, flow):
        self.extract_domain(flow)

    def extract_domain(self, flow):
        response_url = flow.request.url
        try:
            host = flow.request.headers['Host']
        except KeyError as e:
            host = urlparse(response_url).hostname
        try:
            ua = flow.request.headers['User-Agent']
        except KeyError as e:
            ua = ''
        try:
            flag = re.findall(r'\d+\.\d+\.\d+\.\d+', host)
        except Exception as e:
            print(e)
            flag = True
        if not flag:
            try:
                host = host.split(':')[0]
            except KeyError as e:
                print(e)
            tmp = {
                'host': host,
                'ua': ua
            }
            str_host_ua = json.dumps(tmp)
            md5_host_ua = hashlib.md5(str_host_ua.encode(encoding="utf-8")).hexdigest()
            if md5_host_ua not in self.domain_set:
                self.domain_set.add(md5_host_ua)
                self.info_list.append(tmp)
                with open(self.path, 'w') as f:
                    f.write(json.dumps(self.info_list))
                    f.flush()
            print(self.domain_set)


addons = [
    HttpProxy()
]
