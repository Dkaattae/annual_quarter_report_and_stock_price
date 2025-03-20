import dlt
import yfinance as yf
import pandas as pd

nasdaq_tickers_df = pd.read_csv('Nasdaq100List.csv')


@dlt.resource(table_name="nasdaq_tickers")
def nasdaq_ticker_list():
    yield from nasdaq_tickers_df.to_dict("records")

# Function to fetch different financial data types from Yahoo Finance
def fetch_data(endpoint, ticker):
    ticker_obj = yf.Ticker(ticker)
    
    data = getattr(ticker_obj, endpoint, None)
    if data is None:
        return []  # Return an empty list if no data is available

    # If it's a dictionary (e.g., `info`), wrap it in a list and add the ticker
    if isinstance(data, dict):
        return [{"ticker": ticker, **data}]

    # If it's a DataFrame (e.g., `financials`, `balance_sheet`, `cashflow`), convert it properly
    if isinstance(data, pd.DataFrame):
        data = data.T  # Transpose to get correct format
        data.reset_index(inplace=True)  # Ensure "index" is available
        records = data.to_dict("records")  # Convert to list of dictionaries
        
        # Add ticker explicitly to each record
        for record in records:
            record["ticker"] = ticker

        return records

    return []  # Default to an empty list if data is not recognized

# Define DLT resources for each financial dataset
@dlt.resource(table_name="company_info")
def company_info():
    for company in nasdaq_tickers_df["Symbol"]:
        yield from fetch_data("info", company)

@dlt.resource(table_name="financial_statement")
def company_financial_statement():
    for company in nasdaq_tickers_df["Symbol"]:
        yield from fetch_data("financials", company)

@dlt.resource(table_name="balance_sheet")
def company_balance_sheet():
    for company in nasdaq_tickers_df["Symbol"]:
        yield from fetch_data("balance_sheet", company)

@dlt.resource(table_name="cashflow")
def company_cashflow():
    for company in nasdaq_tickers_df["Symbol"]:
        yield from fetch_data("cashflow", company)

# Define the DLT pipeline
pipeline = dlt.pipeline(
    pipeline_name="company_public_info",
    destination="bigquery",
    dataset_name="edgar_data"
)

# Run the pipeline
pipeline.run([nasdaq_ticker_list, company_info, company_financial_statement, company_balance_sheet, company_cashflow])