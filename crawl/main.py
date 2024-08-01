import csv
from services.request_data import (
    get_mktcap_data,
    get_FORN_HD_QTY,
)
from services.serch_code import get_stock_fullcodes, get_stock_code, post_stock_data
from datetime import datetime, timedelta
import sys

sys.path.append("/Users/choi-junyong/local/dhkim")
today = datetime.now()
yesterday = today - timedelta(1)
endDd = yesterday.strftime("%Y%m%d")


def get_data(strtDd, endDd, stock_name):
    try:
        full_code, short_code = get_stock_fullcodes(stock_name)

        # full_code나 short_code가 빈 값일 경우 'not_code' 에러로 처리
        if not full_code or not short_code:
            print(f"No data found for stock name: {stock_name}")
            return None

        mktcap = get_mktcap_data(strtDd, endDd, stock_name, full_code, short_code)
        merge_data = get_FORN_HD_QTY(
            mktcap, strtDd, endDd, stock_name, full_code, short_code
        )
        post_stock_data(merge_data)
        return merge_data
    except Exception as e:
        print(f"Error processing {stock_name}: {e}")
        return "error"


def main():
    stock_info = get_stock_code()
    error_records = []

    for i in range(len(stock_info)):
        result = get_data(stock_info[i].issue_date, endDd, stock_info[i].stock_name)
        if result is None:
            error_records.append(
                {"stock_name": stock_info[i].stock_name, "error_type": "not_code"}
            )
        elif result == "error":
            error_records.append(
                {"stock_name": stock_info[i].stock_name, "error_type": "error"}
            )

    # 오류가 발생한 주식 이름을 CSV 파일에 기록
    with open("error_records.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["stock_name", "error_type"])
        writer.writeheader()
        for record in error_records:
            writer.writerow(record)


if __name__ == "__main__":
    main()
