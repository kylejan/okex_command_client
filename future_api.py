#!/usr/bin/python
# -*- coding: utf-8 -*-

from http_md5_util import build_sign, http_get, http_post


class OkexFutureApi:
    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    #OKCOIN期货行情信息
    def ticker(self, symbol, contractType):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return http_get(self.__url, TICKER_RESOURCE, params)

    #OKCoin期货市场深度信息
    def depth(self, symbol, contractType, size):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        if size:
            params += '&size=' + size if params else 'size=' + size
        return http_get(self.__url, DEPTH_RESOURCE, params)

    #OKCoin期货交易记录信息
    def trades(self, symbol, contractType):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return http_get(self.__url, TRADES_RESOURCE, params)

    #OKCoin期货指数
    def index(self, symbol):
        INDEX = "/api/v1/index.do"
        params = ''
        if symbol:
            params = 'symbol=' + symbol
        return http_get(self.__url, INDEX, params)

    #获取美元人民币汇率
    def exchange_rate(self):
        EXCHANGE_RATE = "/api/v1/exchange_rate.do"
        return http_get(self.__url, EXCHANGE_RATE, '')

    #获取预估交割价
    def estimated_price(self, symbol):
        ESTIMATED_PRICE = "/api/v1/estimated_price.do"
        params = ''
        if symbol:
            params = 'symbol=' + symbol
        return http_get(self.__url, ESTIMATED_PRICE, params)

    #期货全仓账户信息
    def userinfo(self):
        USERINFO = "/api/v1/userinfo.do?"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, USERINFO, params)

    #期货全仓持仓信息
    def position(self, symbol, contractType):
        POSITION = "/api/v1/position.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType
        }
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, POSITION, params)

    #期货下单
    def trade(self, symbol, contractType, price='', amount='', tradeType='', matchPrice='', leverRate=''):
        TRADE = "/api/v1/trade.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'amount': amount,
            'type': tradeType,
            'match_price': matchPrice,
            'lever_rate': leverRate
        }
        if price:
            params['price'] = price
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, TRADE, params)

    #期货批量下单
    def batch_trade(self, symbol, contractType, orders_data, leverRate):
        BATCH_TRADE = "/api/v1/batch_trade.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'orders_data': orders_data,
            'lever_rate': leverRate
        }
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, BATCH_TRADE, params)

    #期货取消订单
    def cancel(self, symbol, contractType, orderId):
        CANCEL = "/api/v1/cancel.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'order_id': orderId
        }
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, CANCEL, params)

    #期货获取订单信息
    def orderinfo(self, symbol, contractType, orderId, status, currentPage, pageLength):
        ORDERINFO = "/api/v1/order_info.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'order_id': orderId,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, ORDERINFO, params)

    #期货逐仓账户信息
    def userinfo_4fix(self):
        INFO_4FIX = "/api/v1/userinfo_4fix.do?"
        params = {'api_key': self.__apikey}
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, INFO_4FIX, params)

    #期货逐仓持仓信息
    def position_4fix(self, symbol, contractType, type1):
        POSITION_4FIX = "/api/v1/position_4fix.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'type': type1
        }
        params['sign'] = build_sign(params, self.__secretkey)
        return http_post(self.__url, POSITION_4FIX, params)
