#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:45:27 2019

@author: madeline
"""

import dotenv as de
import os as os

de.load_dotenv()

api_key = os.environ.get('MY_API_KEY')
plotly_api_key = os.environ.get('plotly_api_key')

import json
import requests

import pandas as pd
import datetime as datetime

import plotly
from plotly import tools
plotly.tools.set_credentials_file(username='madelinelee', api_key=plotly_api_key)

import plotly.plotly as py


import plotly.graph_objs as go
#from plotly.tools import FigureFactory as FF


def user_input():
    stock_list = []
    #valid = True
    symbol = ''
        
    while symbol != 'DONE':
        symbol = input('Please input desired stock symbol (e.g. MSFT) or DONE when done: ')
        
        if symbol == 'DONE':
            stock_list = list(set(stock_list))
            print(stock_list)
            return(stock_list)
        
        if any(char.isdigit() for char in symbol):
            #valid = False
            print('sorry, invalid stock symbol (chars only) ... please try again')
            
        elif len(symbol) != 4:
            #valid = False
            print('sorry, invalid stock symbol (wrong number of characters) ... please try again')
        
        else:
            stock_list.append(symbol)

#from api exercise, 2/13    
def get_stock_data(symbol):
    
    api_key = os.environ.get('MY_API_KEY')
    requests_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + api_key

    response = requests.get(requests_url)
    
    parsed_response = json.loads(response.text)
    
    return(parsed_response)

#
    
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

def create_dataframe(symbol, stock_dictionary):
    #columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    #stock_dictionary = get_stock_data(symbol)
    #print(stock_dictionary)
    timestamp = []
    open_price = []
    high = []
    low = []
    close = []
    volume = []
    
    #print('creating empty dataframe...')
    temp_frame = pd.DataFrame()
    
    for i in stock_dictionary['Time Series (Daily)']:
        temp_path = stock_dictionary['Time Series (Daily)'][i]
        timestamp.append(i)
        open_price.append(temp_path['1. open'])
        high.append(temp_path['2. high'])
        low.append(temp_path['3. low'])
        close.append(temp_path['4. close'])
        volume.append(temp_path['5. volume'])

    
    timestamp = pd.Series(timestamp)
    open_price = pd.Series(open_price)
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    volume = pd.Series(volume)
    
    temp_frame['symbol'] = symbol
    temp_frame['timestamp'] = timestamp
    temp_frame['open_price'] = open_price
    temp_frame['high'] = high
    temp_frame['low'] = low
    temp_frame['close'] = close
    temp_frame['volume'] = volume

    return(temp_frame)
   

def to_csv(symbol, data_frame):
    #os.getcwd()
    csv_file_path = os.path.join(os.path.dirname('__file__'),
                                 "data", symbol + '-' + data_frame['timestamp'][0] +'.csv')
    data_frame.to_csv(csv_file_path)

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
    date_now = datetime.datetime.now()
    recent_close = data_frame['close'][0]
    recommendation = recommend_alg(data_frame)
    
    print('Stock: ' + symbol)
    print('Run at: ' + str(date_now.hour) + ':' + str(date_now.minute) + ', ' + 
          str(date_now.year) + '-' + str(date_now.month) + '-' + str(date_now.day))
    print('Latest data from: ' + data_frame['timestamp'][0])
    print('Latest closing price: '+ to_usd(recent_close))
    print('Recent high price: ' + to_usd(calculate_max(data_frame)))
    print('Recent low price: ' + to_usd(calculate_min(data_frame)))
    print('Recommendation:', print_recommendation(recommendation))
    print('Explanation:', explanation(recommendation, data_frame))
    print('\n')

def append_data_frame(data_list):

    final_frame = pd.concat(data_list).reset_index(drop=True)
    
    return(final_frame)

stock_list = ['MSFT','AMZN', 'AAPL']

#test_frame = append_data_frame(stock_list)

#plot_prices_over_time(test_frame)

def plot_prices_over_time(data_frame):
    #note: only have up to 13 distinct colors, so can only plot 13 stocks
    #to compare at a time ... 
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','darkgrey','goldenrod', 'lavenderblush',
              'fuschia', 'darkolivegreen', 'firebrick', 'blueviolet']
    data_list = []
    stock_list = data_frame['symbol'].unique().tolist()

    
    for i in range(0, len(stock_list)):
        #subset
        temp_frame = data_frame[data_frame['symbol'] == stock_list[i]]
        timestamp_list = pd.to_datetime(temp_frame['timestamp'])

        temp_scatter = go.Scatter(x = timestamp_list,
                                 y = temp_frame['close'],
                                 name = stock_list[i],
                                 line = dict(color = colors[i]))
        data_list.append(temp_scatter)

    
    layout = dict(title='Closing Price vs Time Per Stock',
              showlegend=False,
              xaxis=dict(
                    title = 'Time'
                    ),
              yaxis=dict(
                    title = 'Closing Price ($)'
                    )
              )
                  
    fig = dict(data = data_list, layout = layout)
    py.iplot(fig, filename = 'closing-prices-over-time')


def multi_stock_printout(stock_list):
    data_list = []
    for stock in stock_list:
        temp_parse = get_stock_data(stock)
        print('parsed')
        valid_data = validate_stock_data(temp_parse)
        if valid_data == True:
            print('validated')
            stock_frame = create_dataframe(stock, temp_parse)
            data_list.append(stock_frame)
            print('dataframe created')
            printout(stock, stock_frame)
            to_csv(stock, stock_frame)
            print('to csv done')
                  
        elif valid_data == False:
            print('Error: could not retrieve ' + stock + 'stock.')
    
    multi_stock_frame = append_data_frame(data_list)        
    plot_prices_over_time(multi_stock_frame)  
    print('view your plot of closing price vs time at https://plot.ly/~madelinelee/81/closing-price-vs-time-per-stock/#/')      

#multi_stock_printout(stock_list)

def run_robo_advisor():
    stock_list = user_input()
    multi_stock_printout(stock_list)


#run_robo_advisor()
    