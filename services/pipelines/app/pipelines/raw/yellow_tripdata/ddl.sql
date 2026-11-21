CREATE TABLE raw.yellow_tripdata (
    vendor_id INT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance NUMERIC,
    rate_code_id INT,
    store_and_fwd_flag VARCHAR,
    pu_location_id VARCHAR(4),
    do_location_id VARCHAR(4),
    payment_type INT,
    fare_amount NUMERIC,
    extra NUMERIC,
    mta_tax NUMERIC,
    tip_amount NUMERIC,
    tolls_amount NUMERIC,
    improvement_surcharge NUMERIC,
    total_amount NUMERIC,
    congestion_surcharge NUMERIC,
    airport_fee NUMERIC,
    cbd_congestion_fee NUMERIC,
    _md5 TEXT,
    _date DATE,
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/*
SELECT ordinal_position, column_name, data_type
FROM information_schema.columns
WHERE table_catalog = 'datalake' and table_schema = 'raw' and table_name = 'yellow_tripdata'
ORDER BY ordinal_position ASC
*/