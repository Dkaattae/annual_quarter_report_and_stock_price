import pandas as pd
import sys
from kestra import Kestra

def get_cik(ticker):
    cik_ticker_df = pd.read_csv('cik_ticker_dictionary.csv')
    width = 10
    cik_ticker_df['cik_str'] = cik_ticker_df['cik_str'].astype(str).str.zfill(width)
    cik = cik_ticker_df[cik_ticker_df['ticker'] == ticker]['cik_str'].iloc[0]
    return cik


if __name__ == "__main__":
    input_data = " ".join(sys.argv[1:]).upper()  # Read from command-line args
    output_data = get_cik(input_data)
    outputs = {
        'CIK': output_data
    }
    Kestra.outputs(outputs)