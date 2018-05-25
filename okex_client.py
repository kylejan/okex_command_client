#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import inspect
import argparse
from spot_api import OkexSpotApi
from future_api import OkexFutureApi


apikey = ''
secretkey = ''
okex_rest_host = 'https://www.okex.com'


spot_api = OkexSpotApi(okex_rest_host,apikey,secretkey)
future_api = OkexFutureApi(okex_rest_host,apikey,secretkey)


if __name__ == '__main__':
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
            action='append',
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
            action='append',
            help=str('parameters: ' + ' '.join(func_args[1::])))

    args = parser.parse_args()
    if args.security_type == 'spot':
        api = spot_api
    elif args.security_type == 'future':
        api = future_api

    func = getattr(api, args.function)
    response = func(*args.params)
    print(json.dumps(response, indent=4))
