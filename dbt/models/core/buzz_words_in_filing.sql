{{
    config(
        materialized='table'
    )
}}

with buzzword_count as (
    select *
    from {{ ref('stg_word_count') }}
),
daily_stock_return as (
    select *
    from {{ ref('stg_stock_return') }}
),
daily_index_return as (
    select *
    from {{ ref('stg_index_return') }}
),
stock_beta as (
    select *
    from {{ ref('calculating_beta') }}
),
buzz_word_and_return as (
    select 
        buzzword_count.ticker, 
        buzzword_count.filedate, 
        word, 
        word_count, 
        stock_return, 
        index_return
    from buzzword_count
    left outer join daily_stock_return
        on buzzword_count.ticker = daily_stock_return.ticker
        and buzzword_count.filedate = daily_stock_return.date
    left outer join daily_index_return
        on buzzword_count.filedate = daily_index_return.date
)
select 
    buzz_word_and_return.ticker,
    stock_return,
    stock_return - stock_beta.alpha - stock_beta.beta*index_return as return_deviation,
    word,
    word_count
from buzz_word_and_return
left outer join stock_beta
    on buzz_word_and_return.ticker = stock_beta.ticker