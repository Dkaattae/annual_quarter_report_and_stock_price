{{
    config(
        materialized='view'
    )
}}

select 
    ticker, free_cash_flow, issuance_of_debt
from {{source('staging', 'financial_statement')}}