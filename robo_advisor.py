#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:45:27 2019

@author: madeline
"""

import dotenv
import json
import requests
import os
import pandas as pd
import datetime as datetime

load_dotenv()

api_key = os.environ.get('MY_API_KEY')

def user_input():
    valid = True
    symbol = input('Please input desired stock symbol: ')
    if any(char.isdigit() for char in symbol):
        valid = False
        print('sorry, invalid stock symbol... please try again')
        
    if len(symbol) > 4:
        valid = False
        print('sorry, invalid stock symbol ... please try again')
    
    if valid == False:
        symbol = input('Please input desired stock symbol: ')
    
    return(symbol)
    
def get_stock_data(symbol):
    
    api_key = os.environ.get('MY_API_KEY')
    requests_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + api_key

    response = requests.get(requests_url)
    
    parsed_response = json.loads(response.text)
    
    return(parsed_response)
    
    #print('latest closing price: ' + parsed_response['Time Series (Daily)']['2019-02-19']['4. close'])

def validate_stock_data(stock_dictionary):
    if 'Error message' in stock_dictionary:
        print('could not get stock dictionary...')

def print_stock_data(stock_dictionary):
    print('timestamp, open, high, low, close, volume')

    for i in stock_dictionary['Time Series (Daily)']:
        temp_path = stock_dictionary['Time Series (Daily)'][i]
        print(i + ', ' + temp_path['1. open'] + ', ' + temp_path['2. high'] +
              ', ' + temp_path['3. low'] + ', ' + temp_path['4. close'] +
              ', ' + temp_path['5. volume'])

def create_dataframe(stock_dictionary):
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    timestamp = []
    open_price = []
    high = []
    low = []
    close = []
    volume = []
    
    temp_frame = pd.DataFrame()
    for i in stock_dictionary['Time Series (Daily)']:
        temp_path = stock_dictionary['Time Series (Daily)'][i]
        timestamp.append(i)
        open_price.append(temp_path['1. open'])
        high.append(temp_path['2. high'])
        low.append(temp_path['3. low'])
        close.append(temp_path['4. close'])
        volume.append(temp_path['5. volume'])
        
        '''print(i + ', ' + temp_path['1. open'] + ', ' + temp_path['2. high'] +
              ', ' + temp_path['3. low'] + ', ' + temp_path['4. close'] +
              ', ' + temp_path['5. volume'])'''
    
    timestamp = pd.Series(timestamp)
    open_price = pd.Series(open_price)
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    volume = pd.Series(volume)
    
    temp_frame['timestamp'] = timestamp
    temp_frame['open_price'] = open_price
    temp_frame['high'] = high
    temp_frame['low'] = low
    temp_frame['close'] = close
    temp_frame['volume'] = volume
    
    return(temp_frame)
    
    
test_frame = create_dataframe(parsed_response)

def calculate_max(data_frame):
    temp_frame = data_frame
    temp_list = temp_frame['high'].tolist()
    temp_list = [float(i) for i in temp_list]
    max_high = max(temp_list)
    return(max_high)

def calculate_min(data_frame):
    temp_frame = data_frame
    temp_list = temp_frame['low'].tolist()
    temp_list = [float(i) for i in temp_list]
    min_low = min(temp_list)
    return(min_low)

def printout(symbol, data_frame):
    date = datetime.datetime.now()
    recent_close = data_frame['close'][0]
    print('Stock: ' + symbol)
    print('Run at: ' + date.year + '-' + date.month + '-' + date.day)
    print('Latest data from: ' + data_frame['date'][0])
    print('Latest closing price: ')
    print('Recent high price: ')
    print('Recent low price: ')
    print('Recommendation: ')
    print('Explanation: ')

symbol = 'MSFT'

parsed = get_stock_data('MSFT')
msft_data = create_dataframe(parsed)
msft_high = calculate_max(msft_data)
msft_low = calculate_min(msft_data)