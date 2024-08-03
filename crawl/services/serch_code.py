import sys
import csv

sys.path.append("/src")
import requests
from crawl.db.worker import execute_select_query, execute_insert_update_query
from crawl.db.query import SELECT_STOCK_CODE, INSERT_STOCK_CODE, SELECT_ISSUE_DATE


def get_stock_fullcodes(stock_name):
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd",
    }

    data = {
        "locale": "ko_KR",
        "mktsel": "ALL",
        "typeNo": "0",
        "searchText": stock_name,
        "bld": "dbms/comm/finder/finder_stkisu",
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Stock codes retrieved successfully")
        json_data = response.json()

        for item in json_data["block1"]:
            if item["codeName"] == stock_name:
                full_code = item["full_code"]
                short_code = item["short_code"]
                return full_code, short_code

        return None, None
    else:
        print("Failed to retrieve stock codes")
        print(response.text)
        return None, None


def get_stock_code():
    metadata = execute_select_query(query=SELECT_STOCK_CODE)
    return metadata


def post_stock_data(metadata: dict):
    for record in metadata:
        if record["foreign_accumulated_net_buy"] in ("", "N/A"):
            record["foreign_accumulated_net_buy"] = 0
        else:
            try:
                record["foreign_accumulated_net_buy"] = int(
                    record["foreign_accumulated_net_buy"].replace(",", "")
                )
            except ValueError:
                print(
                    f"Error converting foreign_accumulated_net_buy: {record['foreign_accumulated_net_buy']}"
                )
                record["foreign_accumulated_net_buy"] = 0

        if record["market_cap"] in ("", "N/A"):
            record["market_cap"] = 0
        else:
            try:
                record["market_cap"] = int(record["market_cap"].replace(",", ""))
            except ValueError:
                print(f"Error converting market_cap: {record['market_cap']}")
                record["market_cap"] = 0

    # INSERT 쿼리 실행
    execute_insert_update_query(query=INSERT_STOCK_CODE, params=metadata)


def get_issue_date_from_db():
    with open("error_records.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stock_name = row["stock_name"]
            issue_date = get_issue_date_from_db(stock_name)
            if issue_date:
                print(f"Issue date for {stock_name}: {issue_date}")
            else:
                print(f"No issue date found for {stock_name}")
    metadata = execute_select_query(query=SELECT_ISSUE_DATE, params=stock_name)
    return metadata
