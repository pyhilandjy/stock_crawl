import sys
import csv
from datetime import datetime

sys.path.append("/src")
from crawl.db.worker import execute_select_query
from crawl.db.query import SELECT_ISSUE_DATE


def open_stock_issue_dates_csv():
    stock_info = []
    with open(
        "/src/error_records_.csv",
        mode="r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["issue_date"] = datetime.strptime(row["issue_date"], "%Y-%m-%d").date()
            stock_info.append(row)
    return stock_info


def read_error_csv():
    error_stock_info = []
    with open(
        "/src/error_records.csv",
        mode="r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        for row in reader:
            stock_name = row["stock_name"]
            issue_date = get_issue_date_from_db(stock_name)
            if issue_date:
                error_stock_info.append(
                    {
                        "stock_name": stock_name,
                        "issue_date": issue_date[0]["issue_date"],
                    }
                )
            else:
                print(f"No issue date found for {stock_name}")

    # 결과를 CSV 파일로 추가 저장
    with open(
        "/src/stock_issue_dates.csv",
        mode="a",  # Append mode
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=["stock_name", "issue_date"])

        # 파일이 비어 있으면 헤더 작성
        if file.tell() == 0:
            writer.writeheader()

        for record in error_stock_info:
            writer.writerow(record)

    print("CSV file updated: /src/stock_issue_dates.csv")
    return error_stock_info


def get_issue_date_from_db(stock_name):
    params = {"stock_name": stock_name}
    metadata = execute_select_query(query=SELECT_ISSUE_DATE, params=params)
    return metadata
