# Alt + 3 to block comment
# beautifulsoup4 - web scrapping library

import bs4 as bs #import as bs so that if using different version (bs5),
#only need to change this line

import datetime as dt

import matplotlib.pyplot as plt
from matplotlib import style

import numpy as np
import os #to create new directories
import pandas as pd
import pandas_datareader.data as web
import pickle #to serialise any python object, to save any object as a varible
import requests

style.use('ggplot')

#grabbing S&P 500 data
#wikipedia page: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
#Ctrl+u to view source
#look for specific company

def save_sp500_tickers(): #gets source code
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml") #BeautifulSoup object
    #soup comes from resp
    #using request -> resp.txt (text of the source code)
    #parser
    #table = soup.find('table',{'class':'wikitable sortable'}) #table data
    #to use Beautifulsoup to find things -> soup.find(<What to find>, <The identifier of the thing to find eg: Class>)
    table = soup.find('table', {'id': 'constituents'})
    tickers = [] #empty tickers list
    for row in table.findAll('tr')[1:]: #tr = table row, for each table row
    #[1:] -> 1st row is a table header -> not need
        ticker = row.findAll ("td") [0].text.replace("\n","") #td = table data, each column
        #[0] -> Want the 0th column
        #.text -> convert soup object to text
        for r in (('\n', ''), ('.', '-')):
            ticker = ticker.replace(*r)
            
        tickers.append(ticker) #gives full tickers list of index

    with open("sp500tickers.pickle", "wb") as f: #open with intention to write bytes
        pickle.dump(tickers, f) #dumping tickers to file f

    print(tickers)

    return tickers

#save_sp500_tickers() #saves S&P 500 tickers as csv files, comment this after creation

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f: #open with intention to read bytes
            tickers = pickle.load(f) #tickers list

    #takes all stock data and convert to own csv file and store them in a directory
    #generally when working with API or data collecting task (parsing website), take entire dataset and store it locally since takes a long time to regrab data

    if not os.path.exists('stock_dfs'): #check to see if something (stock_dfs directory exists
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1) #datetime(YYYY, M, D)
    end = dt.datetime.now()

    #iterate through the tickers and grab all the ticker data
    for ticker in tickers: #for ticker in tickers[:25] = grab first 25 tickers
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)): #if csv file doesn't exists
            df = web.DataReader(ticker, 'yahoo', start, end) #read whatever for the ticker is, from yahoo
            df.to_csv('stock_dfs/{}.csv'.format(ticker)) #path to csv
        else:
            print('Already have {}'.format(ticker))
            
#get_data_from_yahoo()

#combine all into 1 dataframe
def compile_data():
    with open("sp500tickers.pickle", "rb") as f: #to read
        tickers = pickle.load(f)

    main_df = pd.DataFrame() #empty data frame object with no column or index

    #iterate thr tickers in the latest updated file
    for count, ticker in enumerate(tickers): #enumrate lets us count things, same as counting thr range, length; counts where we are in this list
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker)) #csv in stock_dfs/<WHATEVER THE TICKER IS>
        df.set_index('Date', inplace = True) #True so that don't have to refine, can do all in 1 place

        #sets up column
        df.rename(columns = {'Adj Close': ticker}, inplace = True) #rename the Adj Close column to whatever the ticker name is
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace = True) #drop these columns on the axes 1 (everything you drop, you drop on the 1st axes, if don't include 1, default is 0 -> will get error

        #to join all adj close data frames (called by their ticker name) together
        if main_df.empty: #bool: if main data frame is empty
            main_df = df #then not empty
        else:
            main_df = main_df.join(df, how='outer') #if certain column or row that some don't have, will give info (NaN) from both hence no loss of data
            #some tickers may not be trading in the time period

        if count % 10 == 0: #
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv') #save

#compile_data()

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')

    #to find correlation between returns instead of prices
    #returns tend to follow normal distribution and prices don't
    #a $1000 stock moves 1% = $100 change
    #compared to a $10 stock that moved $1 (1%)
    #they moved same amount, but if we correlate it looking at the price, it wouldn't provide accurate results
    df.set_index('Date', inplace = True)
    df_corr = df.pct_change().corr()

    #to plot individual ticker
##    df['AAPL'].plot()
##    plt.show()
    df_corr = df.corr() #creates correlation table of data frame - compares relationship between all columns and generate correlation values

    print(df_corr.head())
    #2 companies highly correlated, 1 deviates -> long 1, short 1, eventually they come back together
    # negatively correlated, both going in 1 direction -> long 1, short 1
    #neutrally correlated -> diversified

    data = df_corr.values #gets inner values (Numpy array of columns & rows) of dataframe, not index and headers
    fig = plt.figure()

    #define axes
    ax = fig.add_subplot(1,1,1) #1-by-1, plot #1

    #define heatmaps (no official way to do it)
    #1st step: take colors and plot them on a grid 
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn) #allows you to plot colours
    #Cmap is a range from red to yellow as neutral, to green as positive
    fig.colorbar(heatmap) #gives legend - color bar that depicts ranges

    #graphs, settings of ticks
    #2nd step: have ticks to mark (where are the companies lined up) and add company labels
    #arranging ticks at every half-mark (1.5 tick mark, 2.5 tick mark ...)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor = False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor = False)
    ax.invert_yaxis() #there's always a gap at the top of a matplotlib graph -> no point in this case
    ax.xaxis.tick_top() #moves x axis ticks from bottom of chart to the top -> this case more for tables

    column_labels = df_corr.columns
    row_labels = df_corr.index
    #in this case, both lists should be identical since it's a pure correlation table -> data.shape doesn't matter (505x505)

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    #by default, x labels are horizontal -> Want them to be vertical
    plt.xticks(rotation = 90)
    heatmap.set_clim(-1, 1) #color limit of heatmap (MIN = -1, MAX = 1), full scale
    #if doing covariance, don't bound scale -> comment out the previous line
    plt.tight_layout() #cleans things up
    plt.show()

    #or
    #import seaborn as sns
    #sns.heatmap( df.corr() )

visualize_data()
