# project_1

Porject_members:
- Hyun Bin Shin (Project leader)
- Joanne Laomoc
- Amir Nizam



## Overview

Individual investors often find it challenging to *gauge the performance and risk associated with their asset portfolio. <br>
This uncertainty can hinder their ability to make informed decisions that can help improve the performance of their portfolio and reduce the risk. <br>
To address this, we have developed and designed a set of python functions to help individual investors gain valuable insights into their portfolio. <br>
By using these tools, investors are able to make more informed decisions to optimize their investment strategies. As well as, gain a better understanding of their portfolio performance. <br>

## List of functions

fetch_stock_data(start_date, end_date, tickers, timeframe = '1Day')
- Parameters: 
    - start_date
    - end_date
    - tickers: List of stocks 
    - timeframe
- Collects information about list of stocks and range of period to fetch historical stock price data
- Alpaca API key and secret key are necessary in order to run this function. 
- Make sure the Alpaca API key and secret key are saved in .env file, and they must be stored as variables named 'ALPACA_API_KEY' and 'ALPACA_SECRET_KEY'

portfolio_return(df, weight_list)
- Parameters:
    - df: Dataframe created using fetch_stock_data function
    - weight_list: List of weights for each stocks. Must add up to 1
- Calculates annual mean portfolio return 

portfolio_risk(df, weight_list)
- Parameters:
    - df: Dataframe created using fetch_stock_data function
    - weight_list: List of weights for each stocks. Must add up to 1
- Calculates annual portfolio risk (standard deviation)

mc_sim(df, weight_list, timeframe, nsims, investment_amount = 1, kind = 'line')
- Parameters:
    - df: Dataframe created using fetch_stock_data function
    - weight_list: List of weights for each stocks. Must add up to 1
    - timeframe: Duration of days to perform Monte Carlo simulation
    - nsim: Number of simulations
    - investment_amount: Initial investment amount
    - kind: Type of display
- Performs Monte Carlo simulation using the selected list of stocks and their given weights
- Has 3 types of displays (line graph, KDE plot, and confidence of interval display)

mc_sim_comparison(df, df2, timeframe, nsims, my_weights, your_weights, investment_amount = 1)
- Parameters:
    - df 1 & 2: Dataframe created using fetch_stock_data function
    - timeframe: Duration of days to perform Monte Carlo simulation
    - nsims: Number of sumulations
    - my_weights & your_weights: List of weights for each set of stocks. Each set must add up to 1
    - investment_amount: Initial investment amount
- Performs Monte Carlo simulation for 2 sets of data and compares the result between the two
- Displays line graph simulation results for both sets, then displays the KDE plots of both sets of data

yearly_portfolio_info(df, weight_list)
- Parameters:
    - df: Dataframe created using fetch_stock_data function
    - weight_list: List of weights for each stocks. Must add up to 1
- Calculates the historical portfolio returns and risks per year (ex. portfolio return and risk for 2016, 2017, 2018)
- Information is displated in bar graph format 
















### Referencess
N-asset portfolio risk and return calculation: https://youtu.be/Yqn5ypsCv3g?si=i7tPpsnSzk9BQLww <br>
Monte carlo simulation python: https://youtu.be/6-dhdMDiYWQ?si=xPIXBTUSb3Y6vbjw <br>
Interpolate: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html and ChatGPT <br>
Apply lambda: ChatGPT <br>
Timestamp change to datetime: https://docs.python.org/3/library/datetime.html <br>
Datetime to string: https://www.programiz.com/python-programming/datetime/strftime <br>
Drawing a horizontal line: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html <br>
matplotlib color list: https://matplotlib.org/stable/gallery/color/named_colors.html <br>
