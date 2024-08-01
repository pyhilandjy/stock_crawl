from sqlalchemy import text

SELECT_STOCK_CODE = text(
    """
SELECT DISTINCT dsp.stock_code, si.stock_name, issue_date
FROM daily_stock_price dsp
JOIN stock_info si ON dsp.stock_code = si.stock_code
WHERE dsp.stock_code NOT LIKE '%U%';
"""
)

INSERT_STOCK_CODE = text(
    """
INSERT INTO daily_stock_price_test (business_date, stock_code, market_cap, foreign_accumulated_net_buy)
VALUES (:business_date, :stock_code, :market_cap, :foreign_accumulated_net_buy);
"""
)
