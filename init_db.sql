-- Create weather_records table
CREATE TABLE IF NOT EXISTS weather_records (
    station_id VARCHAR NOT NULL,
    date DATE NOT NULL,
    max_temp FLOAT,
    min_temp FLOAT,
    precipitation FLOAT,
    PRIMARY KEY (station_id, date)
);

-- Create yearly_weather_statistics table
CREATE TABLE IF NOT EXISTS yearly_weather_statistics (
    station_id VARCHAR NOT NULL,
    year INT NOT NULL,
    avg_max_temp FLOAT,
    avg_min_temp FLOAT,
    total_precipitation FLOAT,
    PRIMARY KEY (station_id, year)
);
