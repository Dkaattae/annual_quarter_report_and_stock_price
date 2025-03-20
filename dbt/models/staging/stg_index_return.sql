{{
    config(
        materialized='view'
    )
}}

with yesterday_index_price as (
    select 
        ticker, date, price,
        lag(price) over(partition by ticker order by date) as yesterday_price
    from {{source('staging', 'index_price')}}
)
select 
    ticker, date, price, yesterday_price,
    (price - yesterday_price) / yesterday_price as index_return
from yesterday_index_price

{% if var('is_test_run', default=true) %}
    limit 100
{% endif %}