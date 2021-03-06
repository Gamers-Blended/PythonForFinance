# PythonFinance-WebScrap
With reference from https://www.youtube.com/playlist?list=PLQVvvaa0QuDcOdF96TBtRtuQksErCEBYZ
## Python for Finance

**1: Plotting of Individual Stocks <br/>** 
This file retrieves stock prices of a specific ticker (to be chosen by the user) from Yahoo Finance API, then stores them in a newly created CSV file. <br/>
It then plots a candlestick graph of the adjusted closing price of the selected stock. <br/>
**TSLA** is the default ticker. <br/>
A different stock can be selected by changing the ticker name in the `web.DataReader()` function. <br/>

![](Images/candlestick_ohlc.JPG)


**2: Web Scrap & Visualisation <br/>** 
A program used to scrap data from tables in websites and convert them into CSV file. <br/>
It then visualises the data from the CSV file as a correlation heatmap. <br/>
By default, data is scrapped from the **S&P500 Wikipedia page**. <br/>

![](Images/Python%20Heatmap.JPG)

**3: Preprocessing Data for Machine Learning <br/>** 
Uses the CSV file generated from Web Scrap & Visualisation.py and votes buy/sell/hold decision through 3 classifiers: <br/>
1. `svm.LinearSVC()`
2. `neighbors.KNeighborsClassifier()`
3. `RandomForestClassifier()`

Results: <br>
![](Images/Voting%20Example.JPG)

Voting labels:
- 1 -> buy
- -1 -> sell
- 0 -> hold

**BAC** is the default ticker.
