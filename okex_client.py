#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import inspect
import argparse
import datetime
import logging
import logzero
from logzero import logger
from logging.handlers import TimedRotatingFileHandler
from spot_api import OkexSpotApi
from future_api import OkexFutureApi

log_directory = './logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

time_rotating_file_handler = TimedRotatingFileHandler(
    filename='./logs/okex_{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
    when='midnight',
    encoding='utf8'
)
logger.addHandler(time_rotating_file_handler)
logzero.formatter(logzero.LogFormatter(fmt='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'), True)

apikey = ''
secretkey = ''
okex_rest_host = 'https://www.okex.com'


spot_api = OkexSpotApi(okex_rest_host,apikey,secretkey)
future_api = OkexFutureApi(okex_rest_host,apikey,secretkey)


if __name__ == '__main__':
    config = json.load(open('config.json'))
    apikey = config['api_key']
    secretkey = config['secret_key']
    spot_api = OkexSpotApi(okex_rest_host,apikey,secretkey)
    future_api = OkexFutureApi(okex_rest_host,apikey,secretkey)

    spot_api_functions = [func for func in dir(spot_api) if func[0] != '_']
    future_api_functions = [func for func in dir(future_api) if func[0] != '_']

    parser = argparse.ArgumentParser(prog='python okex_client.py', conflict_handler='resolve')
    sub_parser = parser.add_subparsers(help='security type')

    spot_parser = sub_parser.add_parser('spot', help='spot api')
    spot_parser.set_defaults(security_type='spot')
    api_sub_parser = spot_parser.add_subparsers(help='api functions')
    for func in spot_api_functions:
        func_parser = api_sub_parser.add_parser(func)
        func_parser.set_defaults(function=func)
        func_args = inspect.getargspec(getattr(spot_api, func)).args
        func_parser.add_argument('-params',
            default=[],
            nargs='*',
            help=str('parameters: ' + ' '.join(func_args[1::])))

    future_parser = sub_parser.add_parser('future', help='future api')
    future_parser.set_defaults(security_type='future')
    api_sub_parser = future_parser.add_subparsers(help='api functions')
    for func in future_api_functions:
        func_parser = api_sub_parser.add_parser(func)
        func_parser.set_defaults(function=func)
        func_args = inspect.getargspec(getattr(future_api, func)).args
        func_parser.add_argument('-params',
            default=[],
            nargs='*',
            help=str('parameters: ' + ' '.join(func_args[1::])))

    args = parser.parse_args()
    if args.security_type == 'spot':
        api = spot_api
    elif args.security_type == 'future':
        api = future_api

    func = getattr(api, args.function)
    args.params = [str(param) for param in args.params]
    response = func(*args.params)
    responst_str = json.dumps(response, indent=4)

    func_params = ''
    func_param_fields = inspect.getargspec(getattr(api, args.function)).args[1::]
    for i in range(0, len(args.params)):
        func_params += '{}={} '.format(func_param_fields[i], args.params[i])

    logger.info('[request] %s %s %s', args.security_type, args.function, func_params)
    logger.info('[response]\n%s', responst_str)
