{{
    config(
        materialized='table'
    )
}}

with stock_return_in_range as (
    select *
    from {{ ref('stg_stock_return') }}
    where date >= '2024-01-01'
        and date < '2025-01-01'
),
index_return_in_range as (
    select *
    from {{ ref('stg_index_return') }}
    where date >= '2024-01-01'
        and date < '2025-01-01'
),
average_stock_return as (
    select ticker, avg(stock_return) as avg_stock_return
    from stock_return_in_range
    group by ticker
),
average_index_return as (
    select avg(index_return) as avg_index_return
    from index_return_in_range
),
stock_deviation_return as (
    select 
        stock_return_in_range.ticker,
        stock_return_in_range.date,
        stock_return_in_range.stock_return - avg_stock_return as stock_return_dev
    from stock_return_in_range
    left outer join average_stock_return
        on stock_return_in_range.ticker = average_stock_return.ticker
),
index_deviation_return as (
    select 
        index_return_in_range.date,
        index_return_in_range.index_return - avg_index_return as index_return_dev
    from index_return_in_range
    cross join average_index_return
),
find_beta as (
select 
    stock_deviation_return.ticker,
    sum(stock_return_dev*index_return_dev) / sum(index_return_dev*index_return_dev) as beta,
from stock_deviation_return
left outer join index_deviation_return
    on stock_deviation_return.date = index_deviation_return.date
group by stock_deviation_return.ticker
)
select
    find_beta.ticker,
    beta,
    avg_stock_return - avg_index_return * beta as alpha
from find_beta
cross join average_index_return
left outer join average_stock_return
    on find_beta.ticker = average_stock_return.ticker
