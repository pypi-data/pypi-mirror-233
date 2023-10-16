import numpy as np
import pandas as pd
import os, requests, time, json
from datetime import datetime, timedelta


class MikiApi(object):
    def __init__(self):
        self.server_url = 'http://www.waico.cn'
        self.token_path = os.path.dirname(__file__)+'/token.txt'
        self.token = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'r') as f:
                self.token = f.read()

    def set_token(self, token):
        with open(self.token_path, 'w') as f:
            f.write(token)

    def get_today(self, dtype):
        if not self.token:
            raise Exception('set_token first')
        response = requests.get(self.server_url+f'/download/get_today?token={self.token}&dtype={dtype}')
        data = json.loads(response.content)
        return data

    def get_all_trade_days(self):
        if not self.token:
            raise Exception('set_token first')
        response = requests.get(self.server_url+f'/download/get_trade_days?token={self.token}')
        data = json.loads(response.content)
        return data

    def get_factor(self, code, start, end):
        if not self.token:
            raise Exception('set_token first')
        response = requests.get(self.server_url + f'/download/get_factor?token={self.token}&start={start}&end={end}&code={code}')
        data = json.loads(response.content)
        return data

    def get_code_list(self, dtype):
        if not self.token:
            raise Exception('set_token first')
        response = requests.get(self.server_url + f'/download/get_code_list?token={self.token}&dtype={dtype}')
        data = json.loads(response.content)
        return data

    def get_macro_data(self, country, kind, start, end):
        # 获取宏观数据
        pass

    def get_component(self, ctype, level, date):
        # 获取板块成分股信息
        if not self.token:
            raise Exception('set_token first')
        response = requests.get(self.server_url+f'/download/get_component?token={self.token}&ctype={ctype}&level={level}&date={date}')
        data = json.loads(response.content)
        return data

    def get_indicator(self, date):
        # 获取每日指标数据
        if not self.token:
            raise Exception('set_token first')
        response = requests.get(self.server_url+f'/download/get_indicator?token={self.token}&date={date}')
        data = json.loads(response.content)
        return data

    def get_bar(self, code, unit, start, end, field_list=['open','high','low','close','volume'], fq='hfq'):
        # 获取行情数据
        if not self.token:
            raise Exception('set_token first')
        field_list = ','.join(field_list)
        response = requests.get(self.server_url+f'/download/get_bar?token={self.token}&start={start}&end={end}&code={code}&unit={unit}&fields={field_list}&fq={fq}')
        data = np.array(json.loads(response.content))
        return data






























