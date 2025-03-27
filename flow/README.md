1, change docker-compose file

2, setup google cloud 

3, change the header information in code and upload files and code in kestra   
business_overview_v3.py: line 52 - 54   
company_public_filing_business_section.yaml: line 68   
change header information to yours as SEC required.   
Note: personal email address may not work. if not try random company instead.    
(i have no relationship with citibank. )

4, run flow

5, iterating 100 tickers needs CPU and memory, if it not working just run 5-10 manually.    

Note: ticker 'GOOGL' will fail for flow company public filing business section, because filings are under 'GOOG'   
i ignore this error for now. will update to catch it later. 
