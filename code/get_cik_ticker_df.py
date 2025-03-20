import pandas as pd
import requests


url = 'https://www.sec.gov/files/company_tickers.json'
headers = {
            'User-Agent': 'xchencws@citibank.com',  # Replace with your details
            'Accept-Encoding': 'application/json',
            'Host': 'www.sec.gov'
        }


def json_to_dataframe(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        json_data = response.json()
        df = pd.DataFrame(json_data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
         print(f"JSON decoding error: {e}. Check if the URL returns valid JSON.")
         return None
    except pd.errors.EmptyDataError as e:
        print(f"Pandas EmptyDataError: {e}. The JSON data is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_cik_ticker_dataframe():
	df = json_to_dataframe(url, headers)
	cik_ticker_df = df.transpose()

	width = 10
	cik_ticker_df['cik_str'] = cik_ticker_df['cik_str'].astype(str).str.zfill(width)
	return cik_ticker_df


