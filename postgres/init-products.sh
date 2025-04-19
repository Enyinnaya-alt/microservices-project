#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE products_db;
    \c products_db
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL
    );
    INSERT INTO products (name, price) VALUES
        ('Product 1', 19.99),
        ('Product 2', 29.99)
    ON CONFLICT (id) DO NOTHING;
EOSQL