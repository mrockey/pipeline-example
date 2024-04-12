with users as (

    select
        id as user_id
        , email
        , username
        , name:firstname as first_name
        , name:lastname as last_name
        , address:city as city
        , address:zipcode as zip_code
        , geolocation:lat as latitude
        , geolocation:long as longitude
    from {{ ref("raw_database.raw_ecommerce.users") }} 

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