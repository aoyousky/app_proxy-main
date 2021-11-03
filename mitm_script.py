# -*- coding: utf-8 -*-

import json
import os
import re
from urllib.parse import urlparse
import threading


class HttpProxy:
    def __init__(self):
        self.domain_set = set()
        self.info_list = []
        self.path = os.getcwd() + '/request'

    def error(self, flow):
        print('error', flow.request.url)
        self.extract_domain(flow)

    def http_connect(self, flow):
        print('http', flow.request.url)
        self.extract_domain(flow)

    def request(self, flow):
        print('request', flow.request.url)
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
            if host not in self.domain_set:
                tmp = {
                    'host': host,
                    'ua': ua
                }
                self.domain_set.add(host)
                self.info_list.append(tmp)
                with open(self.path, 'w') as f:
                    f.write(json.dumps(self.info_list))
                    f.flush()
            print(self.domain_set)


addons = [
    HttpProxy()
]