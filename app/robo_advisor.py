#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:45:27 2019

@author: madeline
"""

import dotenv as de
import json
import requests
import os
import pandas as pd
import datetime as datetime
from statistics import mean

de.load_dotenv()

api_key = os.environ.get('MY_API_KEY')

def user_input():
    stock_list = []
    valid = True
    symbol = ''
        
    while symbol != 'DONE':
        symbol = input('Please input desired stock symbol or DONE when done: ')
        
        if symbol == 'DONE':
            stock_list = list(set(stock_list))
            return(stock_list)
        
        if any(char.isdigit() for char in symbol):
            #valid = False
            print('sorry, invalid stock symbol... please try again')
            
        elif len(symbol) > 4:
            #valid = False
            print('sorry, invalid stock symbol ... please try again')
        
        else:
            stock_list.append(symbol)

#from api exercise, 2/13    
def get_stock_data(symbol):
    
    api_key = os.environ.get('MY_API_KEY')
    requests_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + api_key

    response = requests.get(requests_url)
    
    parsed_response = json.loads(response.text)
    
    return(parsed_response)
    
#function to validate that the dictionary was correctly loaded
def validate_stock_data(stock_dictionary):
    if 'Error message' in stock_dictionary:
        print('could not get stock dictionary...')
        return(False)
    else:
        return(True)

#function to print all data from the dictionary
def print_stock_data(stock_dictionary):
    print('timestamp, open, high, low, close, volume')

    for i in stock_dictionary['Time Series (Daily)']:
        temp_path = stock_dictionary['Time Series (Daily)'][i]
        print(i + ', ' + temp_path['1. open'] + ', ' + temp_path['2. high'] +
              ', ' + temp_path['3. low'] + ', ' + temp_path['4. close'] +
              ', ' + temp_path['5. volume'])

def create_dataframe(stock_dictionary):
    #columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
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
    
def to_csv(symbol, data_frame):
    #can't figure out how to write this to a folder named 'data', keeps giving me 
    data_frame.to_csv('/Users/madeline/Desktop/robo-advisor-project/data/'+
                      symbol + '-' + data_frame['timestamp'][0] +'.csv')

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

def to_usd(price):
    price = float(price)
    return('${0:,.2f}'.format(price))

def recommend_alg(data_frame):
    recent_low = calculate_min(data_frame)
    if float(data_frame['close'][0]) < 1.2*recent_low:
        #print('Buy')
        return(True)
    else:
        #print('Do not buy')
        return(False)

def print_recommendation(recommendation):
    if recommendation == True:
        return('Buy')
    elif recommendation == False:
        return('Do not buy')

def explanation(recommendation, data_frame):
    if recommendation == True:
        return('Latest closing price (' + data_frame['close'][0] + ') ' +
              'is less than 20% above the recent low (' +
              str(calculate_min(data_frame)) + '), therefore, it is safe to buy with minimal risk.')
    elif recommendation == False:
        return('Latest closing price (' + data_frame['close'][0] + ') ' +
              'is more than 20% above the recent low (' +
              str(calculate_min(data_frame)) + '), therefore, it is too risky to buy.')   

def printout(symbol, data_frame):
    date = datetime.datetime.now()
    recent_close = data_frame['close'][0]
    recommendation = recommend_alg(data_frame)
    
    print('Stock: ' + symbol)
    print('Run at: ' + str(date.hour) + ':' + str(date.minute) + ', ' + 
          str(date.year) + '-' + str(date.month) + '-' + str(date.day))
    print('Latest data from: ' + data_frame['timestamp'][0])
    print('Latest closing price: '+ to_usd(recent_close))
    print('Recent high price: ' + to_usd(calculate_max(data_frame)))
    print('Recent low price: ' + to_usd(calculate_min(data_frame)))
    print('Recommendation:', print_recommendation(recommendation))
    print('Explanation:', explanation(recommendation, data_frame))

'''
symbol = 'MSFT'
parsed = get_stock_data('MSFT')
msft_data = create_dataframe(parsed)
test_close = msft_data['close'][0]
msft_high = calculate_max(msft_data)
msft_low = calculate_min(msft_data)
recommend_alg(msft_data)
to_csv('MSFT', msft_data)
printout('MSFT', msft_data)'''


def multi_stock_printout(stock_list):
    for stock in stock_list:
        temp_parse = get_stock_data(stock)
        valid_data = validate_stock_data(temp_parse)
        if valid_data == True:
            temp_frame = create_dataframe(temp_parse)
            printout(stock, temp_frame)
            to_csv(stock, temp_frame)
        elif valid_data == False:
            print('Error: could not retrieve ' + stock + 'stock.')

def run_robo_advisor():
    stock_list = user_input()
    multi_stock_printout(stock_list)


run_robo_advisor()
    