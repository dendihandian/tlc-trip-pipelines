/*
    SELECT ordinal_position, column_name, data_type
    FROM information_schema.columns
    WHERE table_catalog = 'datalake' and table_schema = 'landing' and table_name = 'yellow_tripdata'
    ORDER BY ordinal_position ASC
*/