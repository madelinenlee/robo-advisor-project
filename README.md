# robo-advisor-project

goal: create a program that can take any stock symbol, or a list of stock symbols, and generate a recommendation to the user about whether to buy the stock or not. Output stock data for that time period to a CSV, in a folder called 'data'.

PACKAGES REQUIRED:
plotly
dotenv
os
pandas
numpy
datetime

FUNCTIONS:
user_input()
  function to get user input
  returns: list of stock symbols
get_stock_data(symbol)
  uses requests package to get stock data from alphavantage
  input: string
  returns: dictionary of stock data
create_dataframe(symbol)
  creates pandas dataframe of stock based on symbol,
  input: string
  returns: pandas dataframe
to_csv(symbol, data_frame)
  writes a dataframe to csv
  inputs: string input for symbol, pandas dataframe
  returns: null
calculate_max(data_frame)
  function to calculate the high price over past 100 days
  input: pandas dataframe
  returns: float
calculate_min(data_frame)
  function to calculate low price over past 100 days
  input: pandas dataframe
  returns: float
to_usd(price)
  function to convert float price to string USD, proper formatting
  input: float
  returns: string
recommend_alg(data_frame)
  function to create recommendation based off pandas dataframe
  inputs:pandas dataframe
  returns: true/false
print_recommendation(recommendation)
  function to print the recommendation based on the value of recommend_alg
  returns: string
explanation(recommendation, data_frame)
  function to print explanation based on print_recommendation
  returns: string
printout(symbol, data_frame)
  #function to format printout correctly
append_data_frame(stock_list)
  function to concatenate a dataframe based on stock symbol list
plot_prices_over_time(stock_list)
  function to plot prices over time through plotly
multi_stock_printout(stock_list)
  function to printout multiple stock information
  returns: printout
run_robo_advisor()
  function to run all functions 
