/*
SELECT ordinal_position, column_name, data_type
FROM information_schema.columns
WHERE table_catalog = 'datalake' and table_schema = 'master' and table_name = 'taxi_zone_lookup'
ORDER BY ordinal_position ASC
*/