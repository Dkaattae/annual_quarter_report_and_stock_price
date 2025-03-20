# 10K/10Q filings and stock price

Note: this is an expandable project. 

## overview   
![Screenshot 2025-03-04 at 3 45 48 PM](https://github.com/user-attachments/assets/d04ac1ae-66ca-4ef2-b229-fe12ee59990c)


## terraform   
setup google cloud

## kestra
orchestration 
see flow in flow folder. 
bind mount the repo folder to kestra so that it could see the code and files needed. 
or you can manually import all files from code folder and file folder to kestra.

step 1, setup google cloud information as in the vedio. 
    flow gcp_ kv and gcp_setup are not uploaded in this repo. 
step 2, run update_stock_price_schedule.yaml in kestra. 
    the flow will update stock adjusted close price from yahoo finance for nasdaq 100 companies. scheduled monthly
step 3, run xbrl_pipeline.yaml in kestra.
    the flow will load xbrl data from yahoo finance to bigquery tables. 
step 4, run company_public_filing_business_section.yaml in kestra. 
    the flow will ask input of ticker, file type and a word of interest. 
    and it will extract business section of recent 10K filing into gcs, and count the total word/word of interest in file. 
    Note: 1, there are some companies that do not have 10K filings because they are foriegn companies. 
        2, there are a few companies, their filing does not include index in html. I ignore thoes companies for now. 
            will be updated to extract from pure text.
        3, this is expandable to 10q file, md&a part. will be updated to include that.
step 5, iterate all tickers from nasdaq companies
    the flow will iterate over tickers read from nasdaq100.csv file as input and run subflow company_public_filing_business_section
    if CPU consumption is overwhelming, run in chunk
further step, add scripts to extract other word of interest from 10K business section. 

## dlt
xbrl_pipeline.yaml running xbrl_pipeline.py which using dlt to load data from yahoo finance api to bigquery tables. 
dlt help me to flatten the json format into table. 

## dbt
see dbt folder   
