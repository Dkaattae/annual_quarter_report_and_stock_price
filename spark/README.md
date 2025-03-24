1, setup dataproc in google cloud as instructed in [05-batch](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/code/cloud.md)

grant main service account roles: dataproc admin, compute admin, service account user, storage admin, storage compute admin, bigquery admin.     
grant dataproc service account roles: dataproc worker   

2, load pyspark code into google cloud storage

3, submit job, put code uri into main py file and folder uri, dataset.table as arguments  
or submit job through gcloud CLI
```
gs://edgar_company_submission_files/code/count_words_in_file.py \
-- \
    --input_business_section=gs://edgar_company_submission_files/business_section/* \
    --output=edgar_data.business_section_word_count
```
