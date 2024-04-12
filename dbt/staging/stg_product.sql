with products as (

    select
        id as product_id
        , title
        , price
        , category
        , description
    from {{ ref("raw_database.raw_ecommerce.products") }} 

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