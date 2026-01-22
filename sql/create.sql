select * from users u 

select * from roles;

truncate users cascade;

delete from users where id = '08d01c30-869c-45f1-8186-3099c0118381'

DROP TABLE roles cascade;

DROP TABLE roles_aud cascade;

CREATE TABLE routes (
    route_id VARCHAR(50) PRIMARY KEY,
    station_code VARCHAR(10),
    date_YYYY_MM_DD DATE,
    departure_time_utc TIME,
    executor_capacity_cm3 NUMERIC(10, 2),
    route_score VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE stops (
    stop_id SERIAL PRIMARY KEY,
    route_id VARCHAR(50),
    stop_code VARCHAR(10),
    lat NUMERIC(9, 6),
    lng NUMERIC(9, 6),
    type VARCHAR(20),
    zone_id VARCHAR(20),
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
);

CREATE TABLE actual_route_sequence (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50) REFERENCES routes(route_id) ON DELETE CASCADE,
    stop_code VARCHAR(10) NOT NULL,
    actual_sequence INTEGER NOT NULL,  -- ← THIS IS CRITICAL!
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE stops ADD CONSTRAINT unique_route_stop UNIQUE (route_id, stop_code);


CREATE INDEX idx_routes_date ON routes(date_YYYY_MM_DD);
CREATE INDEX idx_routes_station ON routes(station_code);
CREATE INDEX idx_stops_route ON stops(route_id);
CREATE INDEX idx_stops_location ON stops(lat, lng);
CREATE INDEX idx_stops_zone ON stops(zone_id);

select count(distinct(route_id)) from routes;

select * from stops;

select * from actual_route_sequence;


select * from routes r 

select count(distinct(route_id)) from stops ;
