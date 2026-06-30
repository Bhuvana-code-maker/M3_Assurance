-- Created automatically on first docker compose up
-- Provides an isolated database for pytest runs
SELECT 'CREATE DATABASE assurance_test'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'assurance_test'
)\gexec
