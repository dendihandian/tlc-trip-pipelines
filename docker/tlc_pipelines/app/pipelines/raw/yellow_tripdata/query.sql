MERGE INTO raw.yellow_tripdata AS tgt
USING (
    SELECT
          CAST(CAST("VendorID" AS NUMERIC) AS INT)                    AS vendor_id
        , CAST(tpep_pickup_datetime AS TIMESTAMP)                     AS tpep_pickup_datetime
        , CAST(tpep_dropoff_datetime AS TIMESTAMP)                    AS tpep_dropoff_datetime
        , CAST(CAST(passenger_count AS NUMERIC) AS INT)               AS passenger_count
        , CAST(trip_distance AS NUMERIC)                              AS trip_distance
        , CAST(CAST("RatecodeID" AS NUMERIC) AS INT)                  AS rate_code_id
        , store_and_fwd_flag                                          AS store_and_fwd_flag
        , CAST(CAST("PULocationID" AS NUMERIC) AS INT)                AS pu_location_id
        , CAST(CAST("DOLocationID" AS NUMERIC) AS INT)                AS do_location_id
        , CAST(CAST(payment_type AS NUMERIC) AS INT)                  AS payment_type
        , CAST(fare_amount AS NUMERIC)                                AS fare_amount
        , CAST(extra AS NUMERIC)                                      AS extra
        , CAST(mta_tax AS NUMERIC)                                    AS mta_tax
        , CAST(tip_amount AS NUMERIC)                                 AS tip_amount
        , CAST(tolls_amount AS NUMERIC)                               AS tolls_amount
        , CAST(improvement_surcharge AS NUMERIC)                      AS improvement_surcharge
        , CAST(total_amount AS NUMERIC)                               AS total_amount
        , CAST(congestion_surcharge AS NUMERIC)                       AS congestion_surcharge
        , CAST("Airport_fee" AS NUMERIC)                              AS airport_fee
        , CAST(cbd_congestion_fee AS NUMERIC)                         AS cbd_congestion_fee
        , _md5                                                        AS _md5
        , CAST(CAST(tpep_pickup_datetime AS TIMESTAMP) AS DATE)       AS _date
        , CAST(_ingested_at AS TIMESTAMP)                             AS _ingested_at
    FROM landing.yellow_tripdata
    WHERE {query_filter}
) AS src
ON tgt._md5 = src._md5

WHEN MATCHED THEN
UPDATE SET
      vendor_id             = src.vendor_id
    , tpep_pickup_datetime  = src.tpep_pickup_datetime
    , tpep_dropoff_datetime = src.tpep_dropoff_datetime
    , passenger_count       = src.passenger_count
    , trip_distance         = src.trip_distance
    , rate_code_id          = src.rate_code_id
    , store_and_fwd_flag    = src.store_and_fwd_flag
    , pu_location_id        = src.pu_location_id
    , do_location_id        = src.do_location_id
    , payment_type          = src.payment_type
    , fare_amount           = src.fare_amount
    , extra                 = src.extra
    , mta_tax               = src.mta_tax
    , tip_amount            = src.tip_amount
    , tolls_amount          = src.tolls_amount
    , improvement_surcharge = src.improvement_surcharge
    , total_amount          = src.total_amount
    , congestion_surcharge  = src.congestion_surcharge
    , airport_fee           = src.airport_fee
    , cbd_congestion_fee    = src.cbd_congestion_fee
    , _date                 = src._date
    , _ingested_at          = src._ingested_at

WHEN NOT MATCHED THEN
INSERT (
      vendor_id
    , tpep_pickup_datetime
    , tpep_dropoff_datetime
    , passenger_count
    , trip_distance
    , rate_code_id
    , store_and_fwd_flag
    , pu_location_id
    , do_location_id
    , payment_type
    , fare_amount
    , extra
    , mta_tax
    , tip_amount
    , tolls_amount
    , improvement_surcharge
    , total_amount
    , congestion_surcharge
    , airport_fee
    , cbd_congestion_fee
    , _md5
    , _date
    , _ingested_at
)
VALUES (
      src.vendor_id
    , src.tpep_pickup_datetime
    , src.tpep_dropoff_datetime
    , src.passenger_count
    , src.trip_distance
    , src.rate_code_id
    , src.store_and_fwd_flag
    , src.pu_location_id
    , src.do_location_id
    , src.payment_type
    , src.fare_amount
    , src.extra
    , src.mta_tax
    , src.tip_amount
    , src.tolls_amount
    , src.improvement_surcharge
    , src.total_amount
    , src.congestion_surcharge
    , src.airport_fee
    , src.cbd_congestion_fee
    , src._md5
    , src._date
    , src._ingested_at
);