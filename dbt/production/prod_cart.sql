with carts as (

    select
        cart_id
        , user_id
        , product_id
        , quantity
        , date
    from {{ ref("database.ecommerce.stg_carts") }}

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