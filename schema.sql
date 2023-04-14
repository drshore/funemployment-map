DROP TABLE IF EXISTS legs;

CREATE TABLE legs (
    mode text,
    origin_latitude numeric(16,10),
    origin_longitude numeric(16,10),
    destination_latitude numeric(16,10),
    destination_longitude numeric(16,10),
    route_name text
);