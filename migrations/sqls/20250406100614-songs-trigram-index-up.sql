CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX trgm_idx ON songs USING GIN (track_name gin_trgm_ops);