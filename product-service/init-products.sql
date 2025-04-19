-- First create the database if it doesn't exist
SELECT 'CREATE DATABASE products_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'products_db')\gexec

-- Then connect to it and create tables
\c products_db

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

INSERT INTO products (name, price) VALUES 
    ('Product 1', 19.99),
    ('Product 2', 29.99),
    ('Product 3', 39.99)
ON CONFLICT (id) DO NOTHING;