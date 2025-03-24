{{
    config(
        materialized='view'
    )
}}

with yesterday_stock_price as (
    select 
        ticker, date, price,
        lag(price) over(partition by ticker order by date) as yesterday_price
    from {{source('staging', 'stock_price')}}
)
select 
    ticker, date, price, yesterday_price,
    (price - yesterday_price) / yesterday_price as stock_return
from yesterday_stock_price
