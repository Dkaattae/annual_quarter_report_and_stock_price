{{
    config(
        materialized='table'
    )
}}

with stock_return_in_range as (
    select *
    from {{ ref('stg_stock_return') }}
),
cal_percentile_cont as (
select
    date, 
    PERCENTILE_CONT(stock_return, 0.9) over(partition by date) as pct_90,
    PERCENTILE_CONT(stock_return, 0.5) over(partition by date) as pct_50,
    PERCENTILE_CONT(stock_return, 0.1) over(partition by date) as pct_10
from stock_return_in_range
where stock_return is not null
)
select
    date, 
    any_value(pct_90) as return_percentile_90,
    any_value(pct_50) as return_percentile_50,
    any_value(pct_10) as return_percentile_10
from cal_percentile_cont
group by date
order by date