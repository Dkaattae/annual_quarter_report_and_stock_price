{{
    config(
        materialized='view'
    )
}}

select 
    split(file_name, '_') [offset(0)] as ticker,
    PARSE_DATE('%Y-%m-%d',  file_date) as filedate,
    total_word_count,
    word,
    word_count
from {{source('staging', 'business_section_word_count')}}