with products as (

    select
        product_id
        , title
        , price
        , category
        , description
    from {{ ref("database.ecommerce.stg_products") }} 

)

, final as (

    select
        product_id
        , title
        , price
        , category
        , description
    from products

)

select * from final