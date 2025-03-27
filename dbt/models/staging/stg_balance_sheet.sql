{{
    config(
        materialized='view'
    )
}}

select 
    ticker, index, total_debt, total_equity_gross_minority_interest, total_liabilities_net_minority_interest
from {{source('staging', 'balance_sheet')}}