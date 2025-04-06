CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
SET pg_trgm.similarity_threshold = .25;
CREATE INDEX trgm_idx ON songs USING GIN (track_name gin_trgm_ops);