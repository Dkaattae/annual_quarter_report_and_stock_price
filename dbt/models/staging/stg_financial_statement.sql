{{
    config(
        materialized='view'
    )
}}

select 
    ticker, ebitda, gross_profit, interest_expense, cost_of_revenue, total_revenue
from {{source('staging', 'financial_statement')}}