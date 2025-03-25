{{
    config(
        materialized='table'
    )
}}

with debt_and_liabilities as (
    select 
        ticker, 
        extract(year from index) as reporting_year,
        total_debt, 
        total_liabilities_net_minority_interest as total_liabilities,
        total_debt / total_liabilities_net_minority_interest as debt_2liabilites_ratio
    from {{ ref('stg_balance_sheet') }}
),
company_sector as (
    select ticker, sector
    from {{ ref('stg_company_info') }}
),
ratio_and_sector as (
select 
    debt_and_liabilities.ticker,
    debt_and_liabilities.reporting_year,
    sector,
    debt_2liabilites_ratio
from debt_and_liabilities
left outer join company_sector
    on debt_and_liabilities.ticker = company_sector.ticker
),
cal_ratio_median as (
select
    reporting_year,
    sector,
    PERCENTILE_CONT(debt_2liabilites_ratio, 0.5) over(partition by sector, reporting_year) as debt_2liabilites_ratio_median,
from ratio_and_sector
)
select
    reporting_year, sector, any_value(debt_2liabilites_ratio_median) as debt_to_liabilites_ratio_median
from cal_ratio_median
group by reporting_year, sector
where debt_2liabilites_ratio_median is not null