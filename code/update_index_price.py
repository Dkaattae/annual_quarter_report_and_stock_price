from google.cloud import bigquery
import yfinance as yf
import datetime
from google.cloud.exceptions import NotFound
import os
import pandas as pd
import json
from kestra.core.client import KestraClient

kestra_client = KestraClient()
credentials = kestra_client.get_secret("GCP_SERCICE_ACCOUNT")

with open("/tmp/google_credentials.json", "w") as creds_file:
    json.dump(credentials, creds_file)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/google_credentials.json"
# Initialize BigQuery client
client = bigquery.Client()

# Define table information
project_id = "edgar-data-pipeline"
dataset_id = "edgar_data"
table_id = "index_price"
full_table_id = f"{project_id}.{dataset_id}.{table_id}"


def download_index_price(start_date, end_date):
    index_data = yf.download("^GSPC", start=start_date, end=end_date)

    adj_close_prices = index_data['Close']
    adj_close_prices.reset_index(inplace=True)
    index_price = adj_close_prices.rename(columns={'Date': 'date', '^GSPC': 'SPX'})
    return index_price

try:
    client.get_table(full_table_id)  # Make an API request.
    QUERY = (
        'SELECT max(date) as latest_date FROM `edgar-data-pipeline.edgar_data.nasdaq_stock_price`'
        )
    get_latest_date_query_job = client.query(QUERY)  # API request
    last_date = get_latest_date_query_job.result()  # Waits for query to finish
except NotFound:
    last_date = '2021-01-01'


# get current date, if market close, set to today, else set to yesterday
ct = datetime.datetime.now(pytz.timezone('America/New_York'))
if ct.hour >= 16:
    current_date = ct.date
else:
    current_date = (ct - timedelta(days=1)).date

# download stock price from last date to current date
df = download_index_price(last_date, current_date)  
df.reset_index(inplace=True)  
df["Date"] = df["Date"].astype(str)  # Convert date to string for BigQuery compatibility

# Append new data to BigQuery
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_APPEND",  # Append data if table exists
    autodetect=True,  # Automatically detect schema
)

job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
job.result()  # Wait for the job to complete

print("Data uploaded successfully!")