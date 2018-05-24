#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    sub_parser = parser.add_subparsers(help='api type help')

    spot_parser = sub_parser.add_parser('spot', help='spot api help')
    spot_parser.set_defaults(security_type='spot')
    spot_op_group = spot_parser.add_mutually_exclusive_group()
    for func in spot_api_functions:
        spot_op_group.add_argument('--{}'.format(func))

    future_parser = sub_parser.add_parser('future', help='future api help')
    future_parser.set_defaults(security_type='future')
    future_op_group = future_parser.add_mutually_exclusive_group()
    for func in future_api_functions:
        future_op_group.add_argument('--{}'.format(func))

    args = parser.parse_args()
    print(args.security_type)

