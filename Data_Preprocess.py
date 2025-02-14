import pandas as pd
import datetime
import numpy as np


def IAM_data_setup(fn="IAM_product.txt"):
    product_master = pd.read_csv(fn)
    # display(product_master.head())
    product_master.dropna(axis='index', how='any', inplace=True)
    # display(product_master.head())
    
    asset_classes = product_master[['Assets','Class','Sector','Type','Currency','Rate']]
    # display(asset_classes.Type.unique())
    # display(asset_classes.Sector.unique())

    assets = product_master.Assets.to_list()
    assets.sort()
    # display(f'{len(assets)} assets')

    return assets, asset_classes

def download_IAM(inpath="IAM_full_data.txt"):
    return pd.read_csv(inpath, header=[0,1], index_col=[0], parse_dates=True)

############################################################
# Selecting Dates for Rebalancing
# and output the row number 
############################################################

def SelectIndex(price_in, mode, start_index):
    # Selecting last day of month of available data
    # index_Month = price_in.groupby([price_in.index.year, price_in.index.month]).tail(1).index
    index_Month = price_in.index.to_series().groupby(price_in.index.to_period("M")).max().to_list()

    if mode == "Q": 
        index =  [x for x in index_Month if float(x.month) % 3.0 == 0 ] 
    elif mode == "M": 
        index = index_Month
    elif mode == "D": 
        index = price_in.index
    elif mode == "S": 
        index = [x for x in index_Month if float(x.month) % 6.0 == 0 ] 
    elif mode == "W": 
        index = price_in.index.to_series().groupby(price_in.index.to_period("W")).max().to_list()
    # Dates where the strategy will be backtested
    index_ = [price_in.index.get_loc(x) for x in index if price_in.index.get_loc(x) >= start_index]
    return index_

##
# Merge the numeric index with the Datetime indexed Dataframe
# and return a dataframe with a column of 'Date' + the numeric index
# and output the dataframe to file of 'fn'
###

def generate_interval(DF, idx_list, fn=None):
    ret = DF.reset_index()
    df = ret.iloc[idx_list]['Date'].reset_index()
    if fn is not None:
        df.to_csv(fn, index=False)
    return df.set_index('index')

#
# Calculate returns from the dataframes using 'Adj Close'
# reset the column names to the tickers
#
def calculate_returns(data):
    c_data = data.loc[:, ('Adj Close', slice(None))]
    c_data.index.names = ['Date']
    a_names = []
    for  f, n in c_data.columns.to_list():
        a_names.append(n)
    c_data.columns = a_names
    return c_data.pct_change().round(4)

def calculate_date_range(data, n_list):
    i_index = data.reset_index().reset_index().set_index("Date")["index"]
    intercept_dates=[]
    for n in n_list:
        print(f"Process {n}")
        n_i_data = data.loc[:, (slice(None), n)]
        n_i_data.columns = ['Adj Close','Close','High','Low','Open','Volume']
        rr = n_i_data.dropna(axis=0, how='all').copy()
        print(rr)
        if len(rr)>0:
            intercept_dates.append({'Symbol':n, 'start':rr.index[0], "i_start": i_index.loc[rr.index[0]], 
                                    'end':rr.index[-1], 'i_end': i_index.loc[rr.index[-1]]})
        else:
            print(f"** ERROR: {n} has no data")

    return pd.DataFrame(intercept_dates).set_index('Symbol')
