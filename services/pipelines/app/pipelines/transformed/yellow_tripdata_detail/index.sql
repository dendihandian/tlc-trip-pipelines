-- Optimasi Index pada kolom _date
CREATE INDEX idx__transformed__yellow_tripdata__date ON transformed.yellow_tripdata_detail (_date);