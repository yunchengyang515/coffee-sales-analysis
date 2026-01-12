-- Coffee Sales Analysis - SQL Queries
-- This file contains analytical queries for the coffee sales dataset

-- ============================================================================
-- 1. SALES OVERVIEW
-- ============================================================================

-- Total sales and transactions
SELECT 
    COUNT(*) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value
FROM coffee_sales;

-- ============================================================================
-- 2. TIME-BASED ANALYSIS
-- ============================================================================

-- Sales by date
SELECT 
    DATE(transaction_date) as sale_date,
    COUNT(*) as transaction_count,
    SUM(total_amount) as daily_revenue,
    AVG(total_amount) as avg_transaction_value
FROM coffee_sales
GROUP BY DATE(transaction_date)
ORDER BY sale_date;

-- Sales by hour of day
SELECT 
    EXTRACT(HOUR FROM transaction_date) as hour_of_day,
    COUNT(*) as transaction_count,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_transaction_value
FROM coffee_sales
GROUP BY EXTRACT(HOUR FROM transaction_date)
ORDER BY hour_of_day;

-- Sales by day of week
SELECT 
    EXTRACT(DOW FROM transaction_date) as day_of_week,
    CASE EXTRACT(DOW FROM transaction_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    COUNT(*) as transaction_count,
    SUM(total_amount) as revenue
FROM coffee_sales
GROUP BY EXTRACT(DOW FROM transaction_date)
ORDER BY day_of_week;

-- Monthly sales trend
SELECT 
    DATE_TRUNC('month', transaction_date) as month,
    COUNT(*) as transaction_count,
    SUM(total_amount) as monthly_revenue,
    AVG(total_amount) as avg_transaction_value
FROM coffee_sales
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month;

-- ============================================================================
-- 3. PRODUCT ANALYSIS
-- ============================================================================

-- Top selling products
SELECT 
    product_name,
    COUNT(*) as times_sold,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_revenue,
    AVG(unit_price) as avg_price
FROM coffee_sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Product category performance
SELECT 
    product_category,
    COUNT(*) as transaction_count,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value
FROM coffee_sales
GROUP BY product_category
ORDER BY total_revenue DESC;

-- ============================================================================
-- 4. CUSTOMER ANALYSIS
-- ============================================================================

-- Top customers by revenue
SELECT 
    customer_id,
    COUNT(*) as purchase_count,
    SUM(total_amount) as total_spent,
    AVG(total_amount) as avg_transaction_value,
    MAX(transaction_date) as last_purchase_date
FROM coffee_sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 20;

-- Customer purchase frequency
SELECT 
    purchase_frequency_bucket,
    COUNT(*) as customer_count
FROM (
    SELECT 
        customer_id,
        COUNT(*) as purchase_count,
        CASE 
            WHEN COUNT(*) = 1 THEN '1 purchase'
            WHEN COUNT(*) BETWEEN 2 AND 5 THEN '2-5 purchases'
            WHEN COUNT(*) BETWEEN 6 AND 10 THEN '6-10 purchases'
            WHEN COUNT(*) > 10 THEN '10+ purchases'
        END as purchase_frequency_bucket
    FROM coffee_sales
    GROUP BY customer_id
) customer_segments
GROUP BY purchase_frequency_bucket
ORDER BY purchase_frequency_bucket;

-- ============================================================================
-- 5. REVENUE ANALYSIS
-- ============================================================================

-- Revenue by location (store)
SELECT 
    store_location,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value
FROM coffee_sales
GROUP BY store_location
ORDER BY total_revenue DESC;

-- Average basket size
SELECT 
    AVG(items_per_transaction) as avg_items_per_transaction,
    AVG(transaction_value) as avg_transaction_value
FROM (
    SELECT 
        transaction_id,
        COUNT(*) as items_per_transaction,
        SUM(total_amount) as transaction_value
    FROM coffee_sales
    GROUP BY transaction_id
) basket_analysis;

-- ============================================================================
-- 6. ADVANCED ANALYTICS
-- ============================================================================

-- Cohort analysis - customer retention
WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(DATE_TRUNC('month', transaction_date)) as cohort_month
    FROM coffee_sales
    GROUP BY customer_id
)
SELECT 
    fp.cohort_month,
    DATE_TRUNC('month', cs.transaction_date) as purchase_month,
    COUNT(DISTINCT cs.customer_id) as customer_count
FROM coffee_sales cs
JOIN first_purchase fp ON cs.customer_id = fp.customer_id
GROUP BY fp.cohort_month, DATE_TRUNC('month', cs.transaction_date)
ORDER BY fp.cohort_month, purchase_month;

-- Running total revenue
SELECT 
    DATE(transaction_date) as sale_date,
    SUM(total_amount) as daily_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE(transaction_date)) as cumulative_revenue
FROM coffee_sales
GROUP BY DATE(transaction_date)
ORDER BY sale_date;

-- Product performance by time of day
SELECT 
    product_name,
    EXTRACT(HOUR FROM transaction_date) as hour_of_day,
    COUNT(*) as times_sold,
    SUM(total_amount) as revenue
FROM coffee_sales
GROUP BY product_name, EXTRACT(HOUR FROM transaction_date)
ORDER BY product_name, hour_of_day;

-- Customer lifetime value (CLV)
SELECT 
    customer_id,
    MIN(transaction_date) as first_purchase,
    MAX(transaction_date) as last_purchase,
    COUNT(*) as total_purchases,
    SUM(total_amount) as lifetime_value,
    AVG(total_amount) as avg_transaction_value,
    EXTRACT(DAY FROM MAX(transaction_date) - MIN(transaction_date)) as customer_tenure_days
FROM coffee_sales
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY lifetime_value DESC
LIMIT 100;

-- ============================================================================
-- 7. PERFORMANCE METRICS
-- ============================================================================

-- Peak hours analysis
SELECT 
    EXTRACT(HOUR FROM transaction_date) as hour_of_day,
    COUNT(*) as transaction_count,
    SUM(total_amount) as revenue,
    RANK() OVER (ORDER BY COUNT(*) DESC) as busy_rank
FROM coffee_sales
GROUP BY EXTRACT(HOUR FROM transaction_date)
ORDER BY transaction_count DESC;

-- Week over week growth
WITH weekly_sales AS (
    SELECT 
        DATE_TRUNC('week', transaction_date) as week,
        SUM(total_amount) as weekly_revenue
    FROM coffee_sales
    GROUP BY DATE_TRUNC('week', transaction_date)
)
SELECT 
    week,
    weekly_revenue,
    LAG(weekly_revenue) OVER (ORDER BY week) as previous_week_revenue,
    weekly_revenue - LAG(weekly_revenue) OVER (ORDER BY week) as revenue_change,
    ROUND(
        ((weekly_revenue - LAG(weekly_revenue) OVER (ORDER BY week)) / 
        LAG(weekly_revenue) OVER (ORDER BY week)) * 100, 2
    ) as growth_percentage
FROM weekly_sales
ORDER BY week;
