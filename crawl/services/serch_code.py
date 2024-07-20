import requests


def get_stock_codes(stock_name):
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
