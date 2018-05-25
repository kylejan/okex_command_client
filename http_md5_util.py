#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import hashlib
import requests
import time


http_proxies = {
    'http': '127.0.0.1:1080',
    'https': '127.0.0.1:1080'
}

def build_sign(params, secret_key):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secret_key
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()

def http_get(url, resource, params=''):
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
    }
    response = requests.get('{}{}?{}'.format(url, resource, params), headers=headers, timeout=30, proxies=http_proxies)
    data = response.content.decode('utf8')
    return json.loads(data)

def http_post(url, resource, params):
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
    }
    response = requests.post(url+resource, data=params, headers=headers, timeout=10, proxies=http_proxies)
    data = response.content.decode('utf8')
    return json.loads(data)
