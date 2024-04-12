with mart as (

    select
        cart.cart_id
        , cart.product_id
        , cart.date
        , cart.quantity
        , cart.quantity * product.price as cart_amount
        , product.price as product_price
        , product.title as product_title
        , product.category as product_category
        , product.description as product_description
        , user.user_id
        , user.city as user_city
        , user.zip_code as user_zip_code
        , user.latitude as user_latitude
        , user.longitude as user_longitude
    from {{ ref("prod_cart") }} as cart
    join {{ ref("prod_user") }} as user on cart.user_id = user.user_id
    left join {{ ref("prod_product") }} as product on cart.product_id = product.product_id

)

, final as (

    select
        cart_id
        , product_id
        , date
        , quantity
        , cart_amount
        , product_price
        , product_title
        , product_category
        , product_description
        , user_id
        , user_city
        , user_zip_code
        , user_latitude
        , user_longitude
    from mart

)

select * from final