-- ============================================================
-- CIBC Analytics | Query 1: Overall Churn Summary
-- ============================================================
SELECT 
    attrition_flag,
    COUNT(*) AS total_customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM cibc_cleaned
GROUP BY attrition_flag
ORDER BY total_customers DESC;

-- ============================================================
-- CIBC Analytics | Query 2: Churn Rate by Province
-- ============================================================
SELECT 
    province,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    COUNT(*) - SUM(churn_flag) AS retained,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM cibc_cleaned
GROUP BY province
ORDER BY churn_rate_pct DESC;


-- ============================================================
-- CIBC Analytics | Query 3: Churn by CIBC Card Category
-- ============================================================
SELECT 
    card_category,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit,
    ROUND(AVG(total_trans_amt), 2) AS avg_transaction_amt
FROM cibc_cleaned
GROUP BY card_category
ORDER BY churn_rate_pct DESC;


-- ============================================================
-- CIBC Analytics | Query 4: Churn by Age Group
-- ============================================================
SELECT 
    age_group,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(total_trans_amt), 2) AS avg_transaction,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit
FROM cibc_cleaned
GROUP BY age_group
ORDER BY age_group;


-- ============================================================
-- CIBC Analytics | Query 5: Churn by Income Category
-- ============================================================
SELECT 
    income_category,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit
FROM cibc_cleaned
GROUP BY income_category
ORDER BY churn_rate_pct DESC;


-- ============================================================
-- CIBC Analytics | Query 6: High Risk Churn Segments
-- ============================================================
SELECT 
    card_category,
    age_group,
    income_category,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(avg_utilization_ratio) * 100, 2) AS avg_utilization_pct
FROM cibc_cleaned
GROUP BY card_category, age_group, income_category
HAVING COUNT(*) >= 10
ORDER BY churn_rate_pct DESC
LIMIT 15;



-- ============================================================
-- CIBC Analytics | Query 7: Transaction Behaviour by Churn
-- ============================================================
SELECT 
    attrition_flag,
    ROUND(AVG(total_trans_amt), 2) AS avg_trans_amount,
    ROUND(AVG(total_trans_ct), 2) AS avg_trans_count,
    ROUND(AVG(avg_utilization_ratio) * 100, 2) AS avg_utilization_pct,
    ROUND(AVG(months_inactive_12_mon), 2) AS avg_months_inactive,
    ROUND(AVG(contacts_count_12_mon), 2) AS avg_contacts
FROM cibc_cleaned
GROUP BY attrition_flag;


-- ============================================================
-- CIBC Analytics | Query 8: Credit Tier vs Churn
-- ============================================================
SELECT 
    credit_tier,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit,
    ROUND(AVG(total_trans_amt), 2) AS avg_transaction
FROM cibc_cleaned
GROUP BY credit_tier
ORDER BY avg_credit_limit;


-- ============================================================
-- CIBC Analytics | Query 9: Demographics Churn Analysis
-- ============================================================
SELECT 
    gender,
    marital_status,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(total_trans_amt), 2) AS avg_transaction
FROM cibc_cleaned
GROUP BY gender, marital_status
ORDER BY churn_rate_pct DESC;


-- ============================================================
-- CIBC Analytics | Query 10: Executive KPI Summary
-- ============================================================
SELECT
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS total_churned,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(*), 2) AS overall_churn_rate,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit,
    ROUND(AVG(total_trans_amt), 2) AS avg_transaction_amt,
    ROUND(AVG(avg_utilization_ratio) * 100, 2) AS avg_utilization_pct,
    ROUND(AVG(months_on_book), 1) AS avg_tenure_months,
    ROUND(AVG(total_trans_ct), 1) AS avg_transaction_count
FROM cibc_cleaned;