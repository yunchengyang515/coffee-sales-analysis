-- Database Schema for Coffee Sales Analysis
-- This file contains the schema definition for the coffee sales database

-- ============================================================================
-- DROP EXISTING TABLES (if needed)
-- ============================================================================

DROP TABLE IF EXISTS coffee_sales CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS stores CASCADE;

-- ============================================================================
-- CREATE TABLES
-- ============================================================================

-- Stores table
CREATE TABLE IF NOT EXISTS stores (
    store_id SERIAL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    store_location VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(50),
    product_type VARCHAR(50),
    unit_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coffee Sales table (main fact table)
CREATE TABLE IF NOT EXISTS coffee_sales (
    transaction_id SERIAL PRIMARY KEY,
    transaction_date TIMESTAMP NOT NULL,
    store_id INTEGER REFERENCES stores(store_id),
    customer_id INTEGER REFERENCES customers(customer_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- CREATE INDEXES
-- ============================================================================

-- Indexes for better query performance
CREATE INDEX idx_coffee_sales_date ON coffee_sales(transaction_date);
CREATE INDEX idx_coffee_sales_customer ON coffee_sales(customer_id);
CREATE INDEX idx_coffee_sales_product ON coffee_sales(product_id);
CREATE INDEX idx_coffee_sales_store ON coffee_sales(store_id);
CREATE INDEX idx_coffee_sales_amount ON coffee_sales(total_amount);

-- Composite indexes for common query patterns
CREATE INDEX idx_coffee_sales_date_customer ON coffee_sales(transaction_date, customer_id);
CREATE INDEX idx_coffee_sales_date_product ON coffee_sales(transaction_date, product_id);

-- ============================================================================
-- CREATE VIEWS
-- ============================================================================

-- Daily sales summary view
CREATE OR REPLACE VIEW daily_sales_summary AS
SELECT 
    DATE(transaction_date) as sale_date,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(quantity) as total_items_sold,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    MIN(total_amount) as min_transaction_value,
    MAX(total_amount) as max_transaction_value
FROM coffee_sales
GROUP BY DATE(transaction_date);

-- Product performance view
CREATE OR REPLACE VIEW product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.product_category,
    COUNT(*) as times_sold,
    SUM(cs.quantity) as total_quantity_sold,
    SUM(cs.total_amount) as total_revenue,
    AVG(cs.total_amount) as avg_transaction_value
FROM coffee_sales cs
JOIN products p ON cs.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.product_category;

-- Customer insights view
CREATE OR REPLACE VIEW customer_insights AS
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(*) as total_purchases,
    SUM(cs.total_amount) as lifetime_value,
    AVG(cs.total_amount) as avg_transaction_value,
    MIN(cs.transaction_date) as first_purchase_date,
    MAX(cs.transaction_date) as last_purchase_date,
    EXTRACT(DAY FROM MAX(cs.transaction_date) - MIN(cs.transaction_date)) as customer_tenure_days
FROM coffee_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name;

-- Store performance view
CREATE OR REPLACE VIEW store_performance AS
SELECT 
    s.store_id,
    s.store_name,
    s.store_location,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT cs.customer_id) as unique_customers,
    SUM(cs.total_amount) as total_revenue,
    AVG(cs.total_amount) as avg_transaction_value
FROM coffee_sales cs
JOIN stores s ON cs.store_id = s.store_id
GROUP BY s.store_id, s.store_name, s.store_location;

-- ============================================================================
-- SAMPLE DATA COMMENTS
-- ============================================================================

COMMENT ON TABLE coffee_sales IS 'Main fact table containing all coffee sales transactions';
COMMENT ON TABLE products IS 'Dimension table containing product information';
COMMENT ON TABLE customers IS 'Dimension table containing customer information';
COMMENT ON TABLE stores IS 'Dimension table containing store information';

COMMENT ON COLUMN coffee_sales.transaction_date IS 'Date and time of the transaction';
COMMENT ON COLUMN coffee_sales.total_amount IS 'Total transaction amount (quantity * unit_price)';
COMMENT ON COLUMN coffee_sales.payment_method IS 'Payment method used (cash, card, mobile, etc.)';
