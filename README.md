# project_1

Project members:
- Hyun Bin Shin (Project leader)
- Joanne Laomoc
- Amir Nizam



## Overview

Individual investors often find it challenging to evaluate the performance and risk associated with their asset portfolio.
This uncertainty can hinder their ability to make informed decisions that can help improve the performance of their portfolio and reduce the risk. <br>
To address this, we have designed and developed a set of python functions to help individual investors gain valuable insights into their portfolio.
By using these functions we have created, investors can utilize the generated dataset to drive more informed decisions to optimize their investment strategies. As well as, gain a better understanding of their portfolio performance. <br>


## List of functions


**### Preparing necessary data** 

#### 1. Retrieve stock price information

fetch_stock_data(start_date, end_date, stock_list)
- Parameters: 
    - start_date (YYYY-MM-DD)
    - end_date (YYYY-MM-DD)
    - stock_list: List of stocks 

This function takes the parameters of start date, end date, and list of stocks to collect historical stock price data to later transform it into a usable dataframe  

Keynote: In order to run this function you will need an Alpaca API Key and Secret Key stored into a .env file under the variable names 'ALPACA_API_KEY' and 'ALPACA_SECRET_KEY'

#### 2. Generate random portfolio weight

weights(stock_list, repeats)
- Parameters:
    - stock_list
    - repeats: Number of sets of weights to create

For simulation purposes this function randomly creates sets of generated weights. That can be used for your functions. 



**### Basic portfolio information**

#### 3. Calculate annual portfolio return

annual_portfolio_return(df, weight_list)
- Parameters:
    - df: Dataframe created using fetch_stock_data function
    - weight_list: List of weights for each stock 

This function takes the parameter of the created stock dataframe and a list of weights of your choosing to calculate the annual mean portfolio return

Keynote: for all functions with weight_list - All weight list must add up to 1 (100%)

#### 4. Calculate annual portfolio risk (standard deviation)

annual_portfolio_risk(df, weight_list)
- Parameters:
    - df
    - weight_list

This function takes the parameter of the created stock dataframe and a list of weights of your choosing to calculate the annual portfolio risk (standard deviation)

#### 5. Visualize yearly portfolio returns and risks

yearly_portfolio_info(df, weight_list)
- Parameters:
    - df
    - weight_list

This function calculates the historical yearly return and risk of your created dataframe and creates a bar graph to display the results
Ex. portfolio return and risk for 2016, 2017, 2018



**### Investment opportunity set**

#### 6. Visualize The Efficient Frontier and Composition of The Safest, Optimal and Risky Portfolio

opportunity_set(df, my_weights, repeats, risk_free_return = 0, cal = False)
- Parameters: 
    - df
    - my_weights
    - repeats: How many data points to create on the scatter plot
    - risk_free_return: Risk free rate. Used to calculate optimal risky portfolio
    - cal: Capital allocation line. If this is set as True, it will draw capital allocation line on the graph as well

This function creates a scatter plot of portfolio returns vs risks, for a number of simulations. This plot visualizes the efficient frontier allowing the user to identify how their portfolio is doing. This graph also suggests the best composition for the safest portfolio and the optimal risky portfolio. This gives the user the ability to utilize the information given to re-evaluate their current portfolio. It also allows them to make their own informed decision to increase their profits or decrease their risk. <br>
This function returns a list of optimal risky portfolio weights



**### Monte Carlo Simulation**

#### 7. Perform Monte Carlo Simulations

mc_sim(df, weight_list, timeframe, nsims, investment_amount = 1, kind = 'line')
- Parameters:
    - df
    - weight_list
    - timeframe: Number of days to perform Monte Carlo simulation. This timeframe goes by trading days (ex. 1 year will equal to 252 trading days)
    - nsims: Number of simulations
    - investment_amount: Initial investment amount
    - kind: Type of display (has 3 kinds: 'line', 'kde', 'visualize_ci')


This function performs a Monte Carlo simulation using the created dataframe and the given weights to run a simulation based on the portfolio return and risk. Once the function generates these datasets, it will display the information into 3 different kinds of graphs (line graph, KDE plot, and confidence interval display). This will help the individual have a better visual understanding of the possible outcomes of their investment. <br>
This function returns dataframe of simulations

#### 8. Compare two different sets of portfolios by comparing their Monte Carlo simulation results 

mc_sim_comparison(df, df2, weight_1, weight_2, timeframe, nsims, investment_amount = 1)
- Parameters:
    - df 1 & 2: Dataframe created using fetch_stock_data function for portfolio 1 and portfolio 2
    - weight 1 & 2: Weight composition of portfolio 1 and portfolio 2
    - timeframe
    - nsims
    - investment_amount

This function compares two different sets of portfolios by running Monte Carlo Simulation for each and compares the result. Each simulation results are displayed, then the third graph displays both results' KDE plots on the same graph for comparison purpose

#### 9. Comparison of Actual Return Data and Simulated Return

actual_return_plot(df, weight_list, timeframe, investment_amount = 1)
- Parameters:
    - df
    - weight_list
    - timeframe: Number of days the user wants to see the portfolio return. This timeframe goes by calendar days, not trading days (ex. 1 year will equal to 365 days)
    - investment_amount

The purpose of this function is to obtain the actual returns for a given time frame. The function results in a line graph to better visual a portfolio’s return. When this function is used together with mc_sim with kind = ‘visualize_ci’, the user can compare the simulation results with the actual return data. Ex.  If the timeframe is 365 and the dataframe end date was 2018-12-31 the function will display a portfolio return from 2019-01-01 until 2020-01-01

Keynote: If the end_date of df + timeframe is later than today's date, the function will not work






### Referencess
Apply lambda: ChatGPT <br>
Datetime to string: https://www.programiz.com/python-programming/datetime/strftime <br>
Drawing a horizontal line: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html <br>
Interpolate: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html and ChatGPT <br>
mMtplotlib color list: https://matplotlib.org/stable/gallery/color/named_colors.html <br>
N-asset portfolio risk and return calculation: https://youtu.be/Yqn5ypsCv3g?si=i7tPpsnSzk9BQLww <br>
Monte carlo simulation python: https://youtu.be/6-dhdMDiYWQ?si=xPIXBTUSb3Y6vbjw <br>
Timestamp change to datetime: https://docs.python.org/3/library/datetime.html <br>
















