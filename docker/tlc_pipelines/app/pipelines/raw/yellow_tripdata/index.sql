-- Optimasi Index pada kolom _date
CREATE INDEX idx__raw__yellow_tripdata__date ON raw.yellow_tripdata (_date);