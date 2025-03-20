import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from kestra import Kestra
import sys

def count_words(filepath):
    """Counts the number of words in a text file.

    Args:
        filepath: The path to the text file.

    Returns:
        The number of words in the file, or None if the file could not be opened.
    """
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            words = content.split()
            return len(words)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None


def count_word_in_file(filepath, word):
    """Counts the number of times a word appears in a text file.

    Args:
        filepath: The path to the text file.
        word: The word to count.

    Returns:
        The number of times the word appears in the file.
    """
    count = 0
    try:
        with open(filepath, 'r') as file:
            for line in file:
                words = line.split()
                count += words.count(word)
    except FileNotFoundError:
         return f"Error: File not found at {filepath}"
    return count



def get_business_section(CIK, ticker, file_type, submission_file, word_of_interest):
    headers = {
            'User-Agent': 'xchencws@citibank.com',  # Replace with your details
            'Accept-Encoding': 'application/json',
            'Host': 'www.sec.gov'
        }
    # Step 1: Get the list of filings
    with open(submission_file, 'r') as file:
        filings_data = json.load(file)

    # Step 2: Find the latest 10-K filing
    for filing in filings_data["filings"]["recent"]["form"]:
        if filing == file_type:
            index = filings_data["filings"]["recent"]["form"].index(filing)
            accession_no = filings_data["filings"]["recent"]["accessionNumber"][index].replace("-", "")
            break

    try:
        print(accession_no)
    except NameError:
        return (None, 0, 0)

    doc_url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accession_no}/index.json"
    response = requests.get(doc_url, headers=headers)
    doc_data = response.json()

    # Step 3: Get the raw 10-K document
    doc_index_df = pd.DataFrame(doc_data["directory"]["item"])
    include_file_type = "htm"
    exclude_file_type = 'xml'
    size_threshold = 10000
    doc_index_filtered_df = doc_index_df[doc_index_df['name'].str.contains(ticker.lower(), na=False)]
    doc_index_filtered_df = doc_index_filtered_df[doc_index_filtered_df['name'].str.contains(include_file_type, na=False)]
    doc_index_filtered_df = doc_index_filtered_df[~doc_index_filtered_df['name'].str.contains(exclude_file_type, na=False)]
    doc_index_filtered_df = doc_index_filtered_df[doc_index_filtered_df['size'].replace('', 0).astype(int) > size_threshold]

    file_url_path = doc_index_filtered_df.iloc[0]['name']
    last_modified_date = doc_index_filtered_df.iloc[0]['last-modified']
    last_modified_date = last_modified_date.split(' ')[0]

    txt_url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accession_no}/{file_url_path}"
    response = requests.get(txt_url, headers=headers)
    doc_text = response.text
    print(txt_url)
    # Parse the HTML
    soup = BeautifulSoup(doc_text, "html.parser")

    # Find the link to the Business section
    business_link = soup.find("a", string="Business")
    risk_factor_link = soup.find("a", string="Risk Factors")

    # If found, extract the href attribute
    if business_link:
        business_href = business_link.get("href")
        print("Business section href:", business_href)
    else:
        print("Business section link not found")
        return (last_modified_date, 0, 0)
    if risk_factor_link:
        risk_factor_href = risk_factor_link.get("href")
        print("risk factor section href:", risk_factor_href)
    else:
        print("risk factor section link not found")
        return (last_modified_date, 0, 0)

    # Step 4: Go to base_url + risk_factors_href and find the start of the "Risk Factors" section
    risk_factor_url =  txt_url + risk_factor_href
    response_risk = requests.get(risk_factor_url, headers = headers)
    soup_risk = BeautifulSoup(response_risk.text, 'html.parser')

    risk_factor_tag = soup.find(attrs={"id": risk_factor_href.lstrip('#')}) or soup.find(attrs={"name": risk_factors_href.lstrip('#')})
    # print(risk_factor_tag)
    # risk_factor_id = risk_factor_tag.get("id")

    if not risk_factor_tag:
        print("Could not find the Risk Factors section in the document")
        exit()

    # Step 5: Find Business Section Start
    business_start_tag = soup.find(attrs={"id": business_href.lstrip('#')}) or soup.find(attrs={"name": business_href.lstrip('#')})
    # print(business_start_tag)

    if not business_start_tag:
        print("Could not find the Business section in the document")
        exit()

    # Step 6: Extract Text from Business Section Until Risk Factors
    content = []
    seen_text = set()
    for tag in business_start_tag.find_all_next():
        if tag == risk_factor_tag:
            break
    
        text = tag.get_text(strip=True)
        if text and text not in seen_text:  # Avoid duplicates
            seen_text.add(text)
            content.append(text)

    # Step 5: Save or print the extracted content
    filename = f'{ticker}_{file_type}_business_section.txt'
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write("\n".join(content))

    print("Section content extracted successfully.")

    total_word_count = count_words(filename)
    interest_word_count = count_word_in_file(filename, word_of_interest)

    return (last_modified_date, total_word_count, interest_word_count)


if __name__ == "__main__":
    input_data = sys.argv[1:]  # Read from command-line args
    output_data = get_business_section(*input_data)
    outputs = {
        'last_modified_date': output_data[0],
        'total_word_count': output_data[1],
        'interest_word_count': output_data[2]
    }
    Kestra.outputs(outputs)