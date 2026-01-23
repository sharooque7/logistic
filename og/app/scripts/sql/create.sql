CREATE TABLE routes (
    route_id VARCHAR(50) PRIMARY KEY,
    station_code VARCHAR(10),
    date_YYYY_MM_DD DATE,
    departure_time_utc TIME,
    executor_capacity_cm3 NUMERIC(10, 2),
    route_score VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_routes_date ON routes(date_YYYY_MM_DD);
CREATE INDEX idx_routes_station ON routes(station_code);

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

ALTER TABLE stops ADD CONSTRAINT unique_route_stop UNIQUE (route_id, stop_code);
CREATE INDEX idx_stops_route ON stops(route_id);
-- CREATE INDEX idx_stops_location ON stops(lat, lng);
-- CREATE INDEX idx_stops_zone ON stops(zone_id);

CREATE TABLE actual_route_sequence (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50) REFERENCES routes(route_id) ON DELETE CASCADE,
    stop_code VARCHAR(10) NOT NULL,
    actual_sequence INTEGER NOT NULL,  
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_actual_stops_route ON actual_route_sequence(route_id);
ALTER TABLE actual_route_sequence ADD CONSTRAINT unique_actual_route_stop UNIQUE (route_id, stop_code);


CREATE TABLE planned_route_sequence (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50) REFERENCES routes(route_id) ON DELETE CASCADE,
    stop_code VARCHAR(10),
    planned_sequence INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_planned_route_sequence ON planned_route_sequence(route_id);
ALTER TABLE planned_route_sequence ADD CONSTRAINT unique_planned_route_stop UNIQUE (route_id, stop_code);

CREATE TABLE route_metrics (
    id SERIAL PRIMARY KEY,

    route_id VARCHAR(50) REFERENCES routes(route_id) ON DELETE CASCADE,

    total_planned_distance_km DOUBLE PRECISION,
    total_actual_distance_km DOUBLE PRECISION,

    distance_delta_km DOUBLE PRECISION,
    distance_delta_percent DOUBLE PRECISION,
    
    order_matched_stops INTEGER,
    order_match_percentage DOUBLE PRECISION,
    prefix_match_count INTEGER,

    total_stops INTEGER,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_route_metrics UNIQUE (route_id)
);