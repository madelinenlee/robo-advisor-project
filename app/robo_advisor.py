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


#user input function
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

#function to create dataframe of stock data of one company
def create_dataframe(symbol, stock_dictionary):

    timestamp = []
    open_price = []
    high = []
    low = []
    close = []
    volume = []
    symbol_list = []
    
    temp_frame = pd.DataFrame()
    
    for i in stock_dictionary['Time Series (Daily)']:
        temp_path = stock_dictionary['Time Series (Daily)'][i]
        timestamp.append(i)
        open_price.append(temp_path['1. open'])
        high.append(temp_path['2. high'])
        low.append(temp_path['3. low'])
        close.append(temp_path['4. close'])
        volume.append(temp_path['5. volume'])
        symbol_list.append(symbol)

    
    timestamp = pd.Series(timestamp)
    open_price = pd.Series(open_price)
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)
    volume = pd.Series(volume)
    symbol_list = pd.Series(symbol_list)
    
    temp_frame['symbol'] = symbol_list
    temp_frame['timestamp'] = timestamp
    temp_frame['open_price'] = open_price
    temp_frame['high'] = high
    temp_frame['low'] = low
    temp_frame['close'] = close
    temp_frame['volume'] = volume

    return(temp_frame)
   
#function to write dataframe to csv in folder 'data'
#note: this function only works if you run the script in the directory
#above 'app' folder --> thinking about deleting app folder 
def to_csv(symbol, data_frame):
    csv_file_path = os.path.join("../data", symbol + '-' + data_frame['timestamp'][0] +'.csv')
    data_frame.to_csv(csv_file_path)

#function to calculate recent high
def calculate_max(data_frame):
    temp_frame = data_frame
    temp_list = temp_frame['high'].tolist()
    temp_list = [float(i) for i in temp_list]
    max_high = max(temp_list)
    return(max_high)

#function to calculate recent low
def calculate_min(data_frame):
    temp_frame = data_frame
    temp_list = temp_frame['low'].tolist()
    temp_list = [float(i) for i in temp_list]
    min_low = min(temp_list)
    return(min_low)

#function to convert any price to correct string format
def to_usd(price):
    price = float(price)
    return('${0:,.2f}'.format(price))

#function returns T/F based on stock data if user should buy or not
def recommend_alg(data_frame):
    recent_low = calculate_min(data_frame)
    if float(data_frame['close'][0]) < 1.2*recent_low:
        return(True)
    else:
        return(False)

#function prints recommendation
def print_recommendation(recommendation):
    if recommendation == True:
        return('Buy')
    elif recommendation == False:
        return('Do not buy')

#function prints explanation
def explanation(recommendation, data_frame):
    if recommendation == True:
        return('Latest closing price (' + to_usd(data_frame['close'][0]) + ') ' +
              'is less than 20% above the recent low (' +
              to_usd(calculate_min(data_frame)) + '), therefore, it is safe to buy with minimal risk.')
    elif recommendation == False:
        return('Latest closing price (' + to_usd(data_frame['close'][0]) + ') ' +
              'is more than 20% above the recent low (' +
              to_usd(calculate_min(data_frame)) + '), therefore, it is too risky to buy.')   

#function to correctly output information for each stock
def printout(symbol, data_frame):
    date_now = datetime.datetime.now()
    recent_close = data_frame['close'][0]
    recommendation = recommend_alg(data_frame)
    
    print('Stock: ' + symbol)
    print('Run at: ' + '{:02d}'.format(date_now.hour) + ':' + '{:02d}'.format(date_now.minute) + ', ' + 
          str(date_now.year) + '-' + str(date_now.month) + '-' + str(date_now.day))
    print('Latest data from: ' + data_frame['timestamp'][0])
    print('Latest closing price: '+ to_usd(recent_close))
    print('Recent high price: ' + to_usd(calculate_max(data_frame)))
    print('Recent low price: ' + to_usd(calculate_min(data_frame)))
    print('Recommendation:', print_recommendation(recommendation))
    print('Explanation:', explanation(recommendation, data_frame))
    print('\n')

#function to concat dataframes together (multuple stocks)
def append_data_frame(data_list):

    final_frame = pd.concat(data_list).reset_index(drop=True)
    
    return(final_frame)

#function to plot closing prices over time 
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
                  
    fig = dict(data =data_list, layout=layout)
    py.iplot(fig, filename = 'closing-prices-over-time')


#function to handle multiple stocks
def multi_stock_printout(stock_list):
    data_list = []
    for stock in stock_list:
        print(stock)
        temp_parse = get_stock_data(stock)
        #print('parsed')
        valid_data = validate_stock_data(temp_parse)
        if valid_data == True:
            #print('validated')
            stock_frame = create_dataframe(stock, temp_parse)
            data_list.append(stock_frame)
            #print('dataframe created')
            printout(stock, stock_frame)
            to_csv(stock, stock_frame)
            #print('to csv done')
                  
        elif valid_data == False:
            print('Error: could not retrieve ' + stock + 'stock.')
    

    multi_stock_frame = append_data_frame(data_list)

    plot_prices_over_time(multi_stock_frame)  
    print('view your plot of closing price vs time at https://plot.ly/~madelinelee/81/closing-price-vs-time-per-stock/#/')      


#function to run entire robo-advisor project
def run_robo_advisor():
    stock_list = user_input()
    multi_stock_printout(stock_list)

run_robo_advisor()
    