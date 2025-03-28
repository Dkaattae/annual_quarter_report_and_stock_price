# 10K/10Q filings and stock price

## problem definition   
When i worked in financial industries, almost all of the data pipeline was in excel. data loading is from bloomberg API, data transforming is in excel.    
This was very messy, it took me a lot of time to just download the data, and manually download files from SEC website to put in the right folder.    
After I learned techniques through data engineering course, now i can automate the whole thing, even schedule to download stock data, xbrl and 10K/10Q files.   
no more excel, no more messy steps, and it is free (GCP does cost some money if pass free trial), no bloomberg.   
This is an expandable project. later on, i will learn more from MLops and LLMops courses, i can apply all that techniques using this data pipeline. 

## overview   
<img width="892" alt="Screenshot 2025-03-22 at 3 40 09 PM" src="https://github.com/user-attachments/assets/7479d356-8b55-4dcf-95e8-9f022b85eca1" />



## terraform   
setup google cloud storage and bigquery dataset.   
in dataproc.tf, setup a temp bucket for dataproc and dataproc cluster. 
granting roles to service account is required. 

```
terraform init
terraform plan
terraform apply
```
type in credential path when prompt


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
delete this line, 
you can manually import all files from code folder and file folder to kestra.

`docker-compose up`   
in root folder

> *step 1, setup google cloud information as instructed.*
    
[gcp setup](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/flows/05_gcp_setup.yaml)

gcp_kv and gcp_setup are not uploaded to this repo. but it will needed to run other flow. 

setup google credentials in kv store. my key is called 'GCP_SERVICE_ACCOUNT' in flows. changed that in other flows if needed. 

> *step 2, run update_stock_price_schedule.yaml in kestra.*

the flow will update stock adjusted close price from yahoo finance for nasdaq 100 companies. scheduled monthly   
    
> *step 3, run xbrl_pipeline.yaml in kestra.*

the flow will load xbrl data from yahoo finance to bigquery tables.    
    
> *step 4, run company_public_filing_business_section.yaml in kestra.*  

in file business_overview_v3.py and file public_company_filing_business_section.yaml, please change the header to your information.  

the flow will ask input of ticker, file type. this flow will extract item 1 business section from recent 10-K file. 10-Q file is under development, will be updated. and older 10-K/10-Q file may be updated to include. 

there are some useless code about counting word of interest which is disabled. will count words in pyspark.     

Note: 1, there are some companies that do not have 10K filings because they are foriegn companies.    

2, there are a few companies, their filing does not include index in html. I ignore those companies for now.    
will be updated to extract from pure text.   

3, this is expandable to 10q file, md&a part. will be updated to include that.   

> *step 5, iterate all tickers from nasdaq companies.*
manually load nasdaq100ticker list into google cloud storage.   

the flow will iterate over tickers read from nasdaq100.csv file as input and run subflow company_public_filing_business_section

if CPU consumption is overwhelming, run in chunk   

> *step 6, running dbt in flow.*
  
running dbt in kestra

## dlt
xbrl_pipeline.yaml running xbrl_pipeline.py which using dlt to load data from yahoo finance api to bigquery tables. 

dlt help me to flatten the json format into table. 

## dbt
lineage   
<img width="497" alt="Screenshot 2025-03-24 at 10 18 58 PM" src="https://github.com/user-attachments/assets/9c740f80-e372-4093-87ec-635c2b9d14a7" />


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

## report

[looker studio report](https://lookerstudio.google.com/embed/reporting/314d368e-4ed1-495e-b4d4-f6e63ca9b898/page/tEnnC)
