-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS uuid-ossp;

-- Initialize TimescaleDB for the smarttourism database
SELECT timescaledb_pre_restore();
SELECT timescaledb_post_restore();
