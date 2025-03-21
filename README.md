# 10K/10Q filings and stock price

Note: this is an expandable project. 

## overview   
![Screenshot 2025-03-04 at 3 45 48 PM](https://github.com/user-attachments/assets/d04ac1ae-66ca-4ef2-b229-fe12ee59990c)


## terraform   
setup google cloud

## kestra
**orchestration**

see flow in flow folder.     

in docker-compose file, there are a few things need to adjust.  

```
  env_file: .env_encoded
```
    
if you have google cloud credentials encoded as .env_encoded, keep this line.   
if you put google cloud credentials in kv store, delete this line.   
    
```
    volumns:      
        - /Documents/Github/annual_quarter_report_and_stock_price
```

    
this line is for mounting the repo folder to kestra so that it could see the code and files needed. 
or you can manually import all files from code folder and file folder to kestra.

`docker-compose up`   
in root folder

**step 1, setup google cloud information as instructed.**        
    https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/flows/05_gcp_setup.yaml
    
    gcp_kv and gcp_setup are not uploaded to this repo. but it will needed to run other flow. 
    
    setup google credentials in kv store. my key is called GCP_SERVICE_ACCOUNT in flows. changed that in other flows if needed. 
    
**step 2, run update_stock_price_schedule.yaml in kestra.**   
    the flow will update stock adjusted close price from yahoo finance for nasdaq 100 companies. scheduled monthly   
    
**step 3, run xbrl_pipeline.yaml in kestra.**
    the flow will load xbrl data from yahoo finance to bigquery tables.    
    
**step 4, run company_public_filing_business_section.yaml in kestra.**  
    in file business_overview_v3.py an file public_company_filing_business_section.yaml, please change the header to your information.    
    
    the flow will ask input of ticker, file type and a word of interest.   
    
    and it will extract business section of recent 10K filing into gcs.   
    
    counting one word of interest is disabled. will count words in pyspark.     
    
    Note: 1, there are some companies that do not have 10K filings because they are foriegn companies.    
    
        2, there are a few companies, their filing does not include index in html. I ignore thoes companies for now.    
            will be updated to extract from pure text.   
            
        3, this is expandable to 10q file, md&a part. will be updated to include that.   
        
**step 5, iterate all tickers from nasdaq companies.**
    manually load nasdaq100ticker list into google cloud storage.   
    
    the flow will iterate over tickers read from nasdaq100.csv file as input and run subflow company_public_filing_business_section
    
    if CPU consumption is overwhelming, run in chunk   

## dlt
xbrl_pipeline.yaml running xbrl_pipeline.py which using dlt to load data from yahoo finance api to bigquery tables. 

dlt help me to flatten the json format into table. 

## dbt
see dbt folder   

## spark   
in spark folder, there is a py script to count words in business_section file and write to bigquery. 

it will ask two input, the business section gcs folder name, and the output bigquery table. 

I am running pyspark in google dataproc in google cloud console. 

upload python script in google cloud bucket and copy the uri into console

and put the following input into console.    

```
--input_business_section=gs://<your_bucket_name>/business_section \
--output=<your_dataset>.<your_table>
```

note: no need to put jar file to run pyspark-bigquery. 
