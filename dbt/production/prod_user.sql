with users as (

    select
        user_id
        , email
        , username
        , first_name
        , last_name
        , city
        , zip_code
        , latitude
        , longitude
    from {{ ref("database.ecommerce.stg_users") }} 

)

, final as (

    select
        user_id
        , email
        , username
        , first_name
        , last_name
        , city
        , zip_code
        , latitude
        , longitude
    from users

)

select * from final