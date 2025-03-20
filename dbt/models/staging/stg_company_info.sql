{{
    config(
        materialized='view'
    )
}}

select 
    ticker, sector
from {{source('staging', 'company_info')}}
