import yfinance as yf
import datetime
import pandas as pd
from kestra import Kestra
import pytz
from datetime import timedelta
import sys

def download_stock_price(start_date, end_date):
    # List of stock tickers
    ticker_df = pd.read_csv('Nasdaq100List.csv')
    stock_tickers = ticker_df['Symbol'].to_list()

    # Download data for all tickers

    stock_data = yf.download(stock_tickers, start=start_date, end=end_date, auto_adjust=True) 

    # Extract adjusted close prices
    adj_close_prices = stock_data['Close']
    adj_close_prices.reset_index(inplace=True)
    df_unpivot = pd.melt(adj_close_prices, col_level=0, id_vars=['Date'], value_vars=adj_close_prices.columns.tolist())
    price_df = df_unpivot.rename(columns={'value': 'price', 'Ticker': 'ticker', 'Date': 'date'})
    price_filename = 'stock_price.csv'
    price_df.to_csv(price_filename, columns=['date', 'ticker', 'price'], index=False)

    return start_date.replace('-', '')

def download_index_price(start_date, end_date):
    index_data = yf.download("^GSPC", start=start_date, end=end_date, auto_adjust=True)

    adj_close_prices = index_data['Close']
    adj_close_prices.reset_index(inplace=True)
    index_price = adj_close_prices.rename(columns={'Date': 'date', '^GSPC': 'price'})
    index_price['ticker'] = 'SPX'

    index_filename = 'index_price.csv'
    index_price.to_csv(index_filename, columns=['date', 'ticker', 'price'], index=False)

    return start_date.replace('-', '')


if __name__ == "__main__":
    input_data = sys.argv[1:]  # Read from command-line args
    price_start, index_start = input_data
    ct = datetime.datetime.now(pytz.timezone('America/New_York'))
    if ct.hour >= 16:
        current_date = ct.strftime('%Y-%m-%d')
    else:
        current_date = (ct - timedelta(days=1)).strftime('%Y-%m-%d')
    price_data = download_stock_price(price_start, current_date)
    index_data = download_index_price(index_start, current_date)
    outputs = {
        'price_start_date': price_data,
        'index_start_date': index_data
    }
    Kestra.outputs(outputs)