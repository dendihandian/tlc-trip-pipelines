MERGE INTO transformed.yellow_tripdata_detail AS tgt
USING (
    SELECT
          _ytd.vendor_id
        , _ytd.tpep_pickup_datetime
        , _ytd.tpep_dropoff_datetime
        , _ytd.passenger_count
        , _ytd.trip_distance
        , _ytd.rate_code_id
        , _ytd.store_and_fwd_flag
        , _ytd.pu_location_id
        , _ytd.do_location_id
        , _ytd.payment_type
        , _ytd.fare_amount
        , _ytd.extra
        , _ytd.mta_tax
        , _ytd.tip_amount
        , _ytd.tolls_amount
        , _ytd.improvement_surcharge
        , _ytd.total_amount
        , _ytd.congestion_surcharge
        , _ytd.airport_fee
        , _ytd.cbd_congestion_fee
        , _ytd._md5
        , _ytd._date
        , _ytd._ingested_at
        , _pul.borough AS pu_borough
        , _pul.zone AS pu_zone
        , _pul.service_zone AS pu_service_zone
        , _dol.borough AS do_borough
        , _dol.zone AS do_zone
        , _dol.service_zone AS do_service_zone
    FROM (
        SELECT *
        FROM raw.yellow_tripdata
        WHERE {query_filter}
    ) _ytd

    LEFT JOIN (
        SELECT 
            "LocationID" as location_id
            , "Borough" as borough
            , "Zone" as zone
            , "service_zone"
        FROM master.taxi_zone_lookup
    ) _pul ON _pul.location_id = _ytd.pu_location_id

    LEFT JOIN (
        SELECT 
            "LocationID" as location_id
            , "Borough" as borough
            , "Zone" as zone
            , "service_zone"
        FROM master.taxi_zone_lookup
    ) _dol ON _dol.location_id = _ytd.do_location_id
) AS src
ON tgt._md5 = src._md5

WHEN MATCHED THEN
UPDATE SET
      vendor_id                = src.vendor_id
    , tpep_pickup_datetime     = src.tpep_pickup_datetime
    , tpep_dropoff_datetime    = src.tpep_dropoff_datetime
    , passenger_count          = src.passenger_count
    , trip_distance            = src.trip_distance
    , rate_code_id             = src.rate_code_id
    , store_and_fwd_flag       = src.store_and_fwd_flag
    , pu_location_id           = src.pu_location_id
    , do_location_id           = src.do_location_id
    , payment_type             = src.payment_type
    , fare_amount              = src.fare_amount
    , extra                    = src.extra
    , mta_tax                  = src.mta_tax
    , tip_amount               = src.tip_amount
    , tolls_amount             = src.tolls_amount
    , improvement_surcharge    = src.improvement_surcharge
    , total_amount             = src.total_amount
    , congestion_surcharge     = src.congestion_surcharge
    , airport_fee              = src.airport_fee
    , cbd_congestion_fee       = src.cbd_congestion_fee
    , _md5                     = src._md5
    , _date                    = src._date
    , _ingested_at             = src._ingested_at
    , pu_borough               = src.pu_borough
    , pu_zone                  = src.pu_zone
    , pu_service_zone          = src.pu_service_zone
    , do_borough               = src.do_borough
    , do_zone                  = src.do_zone
    , do_service_zone          = src.do_service_zone

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
    , pu_borough
    , pu_zone
    , pu_service_zone
    , do_borough
    , do_zone
    , do_service_zone
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
    , src.pu_borough
    , src.pu_zone
    , src.pu_service_zone
    , src.do_borough
    , src.do_zone
    , src.do_service_zone
);