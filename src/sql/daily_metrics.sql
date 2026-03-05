-- Daily Transaction Metrics
-- This query provides daily aggregated metrics for reporting

SELECT
    date_trunc('day', transaction_date) as date,
    currency,
    COUNT(DISTINCT transaction_id) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    SUM(CASE WHEN is_large_transaction THEN 1 ELSE 0 END) as large_transaction_count,
    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_count,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_count
FROM ${catalog}.${schema}.silver_transactions
WHERE transaction_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY date_trunc('day', transaction_date), currency
ORDER BY date DESC, currency;
