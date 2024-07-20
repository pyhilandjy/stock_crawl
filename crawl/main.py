from services.request_data import (
    get_mktcap_data,
    get_FORN_HD_QTY,
    get_short_selling_data,
    to_csv,
)
from services.serch_code import get_stock_codes
from datetime import datetime, timedelta

today = datetime.now()

yesterday = today - timedelta(1)

strtDd = "20230719"  # 상장일
endDd = yesterday.strftime("%Y%m%d")


def get_data(strtDd, endDd, stock_name):
    full_code, short_code = get_stock_codes(stock_name)
    mktcap = get_mktcap_data(strtDd, endDd, stock_name, full_code, short_code)
    merge_data = get_FORN_HD_QTY(
        mktcap, strtDd, endDd, stock_name, full_code, short_code
    )
    merge_data = get_short_selling_data(
        merge_data, strtDd, endDd, stock_name, full_code, short_code
    )
    to_csv(merge_data, stock_name)


get_data(strtDd, endDd, "삼성전자")
