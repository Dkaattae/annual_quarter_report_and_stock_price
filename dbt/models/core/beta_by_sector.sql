{{
    config(
        materialized='table'
    )
}}

with company_beta as (select * from {{ ref('calculating_beta') }}),

company_sector as (select * from {{ ref('stg_company_info') }}),

company_beta_and_sector as (
select
    company_beta.ticker, beta, sector
from company_beta
left outer join company_sector
    on company_beta.ticker = company_sector.ticker
)

select
    sector,
    avg(beta) as avg_beta
from company_beta_and_sector
group by sector