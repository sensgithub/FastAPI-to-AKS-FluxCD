DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'fastapi') THEN
        CREATE DATABASE fastapi;
    END IF;
END $$;
\c fastapi;
CREATE TABLE IF NOT EXISTS persons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT
);