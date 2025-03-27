{{
    config(
        materialized='view'
    )
}}

select 
    ticker, index, free_cash_flow, issuance_of_debt
from {{source('staging', 'cashflow')}}