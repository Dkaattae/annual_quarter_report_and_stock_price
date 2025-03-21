{{
    config(
        materialized='table'
    )
}}

with stock_return as (
    select *
    from {{ ref('stg_stock_price') }}
    where date >= '2024-01-01'
        and date < '2025-01-01'
),
index_return as (
    select *
    from {{ ref('stg_index_price') }}
    where date >= '2024-01-01'
        and date < '2025-01-01'
),
average_stock_return as (
    select ticker, avg(stock_return) as avg_stock_return
    from stock_return
    group by ticker
),
average_index_return as (
    select avg(index_return) as average_index_return
    from index_return
),
stock_deviation_return as (
    select 
        stock_return.ticker,
        stock_return.date,
        stock_return.return - avg_stock_return as stock_return_dev
    from stock_return
    left outer join average_stock_return
        on stock_return.ticker = average_stock_return.ticker
),
index_deviation_return as (
    select 
        index_return.date,
        index_return.return - avg_index_return as stock_index_dev
    from index_return
    left outer join average_index_return
        on index_return.ticker = average_index_return.ticker
)
select 
    stock_deviation_return.ticker,
    sum(stock_return_dev*index_return_dev) / sum(index_return_dev*index_return_dev) as beta
from stock_deviation_return
left outer join index_deviation_return
    on stock_deviation_return.date = index_deviation_return.date
group by stock_deviation_return.ticker
