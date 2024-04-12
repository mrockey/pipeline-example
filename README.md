# Tecovas Code Exercise for DE

This repo contains both the data pipeline and the dbt models for the coding exercise provided. In the sections below I'll write a brief documentation about my thought processes during each section. Feel free to reach out to me with any questions.

### Data Pipeline Section

For my data pipeline, I used the framework from the Singer project (open-source) and uses the tap & target approach. Ideally, I would decouple the two components however for the purpose of this exercise I left them in a single script. 

For the tap, I created a data schema that contains essential information about each of the streams (product, cart, user). The schema contains the information necessary to use either full replication of key-based replication, however, for the purpose of this exercise I only implemented the full replication process (I left notes in the script about the key-based process as well).

For the target, I mostly wrote skeleton code since I am not familiar with connectors to GCP (more familiar with Snowflake). I also implemented the full replication approach which truncates the table and rewrites all the data to the table. Notes are also there for the key-based approach.

### DBT Section

For my DBT models, I created a staging and production layer for each of the tables. I've used a few approach in the past but I like to keep it simple and clean the columns, datatypes, etc in the staging table and include more complex business/analytical logic in the production table. For this exercise, I did not include business logic in the production table so it may seem redundant. 

For the mart I just joined all the tables together so that a BI tool can use it in the future. I made the following assumptions: 
1. A user needs to be logged in to create a cart (carts always have a user associated) hence the inner join.
2. A cart can be empty (no products) hence the left join.

Lastly, I created a schema that includes the source and model information for documentation purposes.
