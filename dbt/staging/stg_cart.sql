with carts as (

    select
        id as cart_id
        , userId as user_id
        , product.productId as product_id
        , product.quantity as quantity
        , date
    from {{ ref("raw_database.raw_ecommerce.carts") }},
    unnest(products) as product

)

, final as (

    select
        cart_id
        , user_id
        , product_id
        , quantity
        , date
    from carts

)

select * from final