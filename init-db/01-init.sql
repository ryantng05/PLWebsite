-- Initialize the database
CREATE DATABASE pl_predictor;

-- Create a user (already created by POSTGRES_USER)
-- GRANT ALL PRIVILEGES ON DATABASE pl_predictor TO postgres;

-- Connect to the pl_predictor database
\c pl_predictor;

-- Create any additional extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create any initial tables or configurations here
-- (Django will handle the actual table creation via migrations)


