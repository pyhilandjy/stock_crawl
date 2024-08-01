import requests
import csv
from datetime import datetime, timedelta

# 각 데이터 조회 가능한 시작일자
START_DATE_MKTCAP = "19950502"
START_DATE_FORN_HD_QTY = "20051003"
START_DATE_SHORT_SELLING = "20160630"


def adjust_start_date(strtDd, available_start_date):
    start_date = datetime.combine(strtDd, datetime.min.time())
    available_start = datetime.strptime(available_start_date, "%Y%m%d")
    if start_date < available_start:
        start_date = available_start
    return start_date


def get_mktcap_data(strtDd, endDd, stock_name, full_code, short_code):
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd",
    }

    start_date = adjust_start_date(strtDd, START_DATE_MKTCAP)
    end_date = datetime.strptime(endDd, "%Y%m%d")

    current_start_date = start_date
    all_extracted_data = []

    while current_start_date < end_date:
        current_end_date = current_start_date + timedelta(days=364)
        if current_end_date > end_date:
            current_end_date = end_date

        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01701",
            "locale": "ko_KR",
            "tboxisuCd_finder_stkisu0_0": f"{short_code}/{stock_name}",
            "isuCd": full_code,
            "isuCd2": full_code,
            "codeNmisuCd_finder_stkisu0_0": stock_name,
            "param1isuCd_finder_stkisu0_0": "ALL",
            "strtDd": current_start_date.strftime("%Y%m%d"),
            "endDd": current_end_date.strftime("%Y%m%d"),
            "adjStkPrc_check": "Y",
            "adjStkPrc": "2",
            "share": "1",
            "money": "1",
            "csvxls_isNo": "false",
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            print(
                f"Data retrieved successfully for period {current_start_date.strftime('%Y%m%d')} to {current_end_date.strftime('%Y%m%d')}"
            )
            json_data = response.json()

            output_data = json_data["output"]
            for item in output_data:
                date = item["TRD_DD"]
                mktcap = item["MKTCAP"]
                all_extracted_data.append(
                    {
                        "business_date": date,
                        "stock_code": short_code,
                        "market_cap": mktcap,
                    }
                )
        else:
            print(
                f"Failed to retrieve data for period {current_start_date.strftime('%Y%m%d')} to {current_end_date.strftime('%Y%m%d')}"
            )
            print(response.text)

        current_start_date = current_end_date + timedelta(days=1)
    all_extracted_data = sorted(
        all_extracted_data,
        key=lambda x: datetime.strptime(x["business_date"], "%Y/%m/%d"),
    )
    return all_extracted_data


def get_FORN_HD_QTY(
    all_extracted_data, strtDd, endDd, stock_name, full_code, short_code
):
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd",
    }

    start_date = adjust_start_date(strtDd, START_DATE_FORN_HD_QTY)
    end_date = datetime.strptime(endDd, "%Y%m%d")

    current_start_date = start_date
    foreign_data = {}

    while current_start_date < end_date:
        current_end_date = current_start_date + timedelta(days=364)
        if current_end_date > end_date:
            current_end_date = end_date

        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03702",
            "locale": "ko_KR",
            "searchType": "2",
            "mktId": "ALL",
            "trdDd": endDd,
            "tboxisuCd_finder_stkisu0_0": f"{short_code}/{stock_name}",
            "isuCd": full_code,
            "isuCd2": full_code,
            "codeNmisuCd_finder_stkisu0_0": stock_name,
            "param1isuCd_finder_srtisu0_0": "",
            "strtDd": current_start_date.strftime("%Y%m%d"),
            "endDd": current_end_date.strftime("%Y%m%d"),
            "share": "1",
            "csvxls_isNo": "false",
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            print(
                f"Foreign data retrieved successfully for period {current_start_date.strftime('%Y%m%d')} to {current_end_date.strftime('%Y%m%d')}"
            )
            json_data = response.json()

            for item in json_data["output"]:
                date = item["TRD_DD"]
                foreign_data[date] = item["FORN_HD_QTY"]
        else:
            print(
                f"Failed to retrieve foreign data for period {current_start_date.strftime('%Y%m%d')} to {current_end_date.strftime('%Y%m%d')}"
            )
            print(response.text)

        current_start_date = current_end_date + timedelta(days=1)

    for data in all_extracted_data:
        date = data["business_date"]
        data["foreign_accumulated_net_buy"] = foreign_data.get(date, "N/A")

    return all_extracted_data


# def get_short_selling_data(
#     all_extracted_data, strtDd, endDd, stock_name, full_code, short_code
# ):
#     url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#         "Referer": "http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd",
#     }

#     start_date = adjust_start_date(strtDd, START_DATE_SHORT_SELLING)
#     end_date = datetime.strptime(endDd, "%Y%m%d")
#     short_selling_data = {}

#     current_start_date = start_date

#     while current_start_date <= end_date:
#         current_end_date = current_start_date + timedelta(days=364)
#         if current_end_date > end_date:
#             current_end_date = end_date

#         data = {
#             "bld": "dbms/MDC/STAT/srt/MDCSTAT30001",
#             "locale": "ko_KR",
#             "tboxisuCd_finder_srtisu0_0": f"{short_code}/{stock_name}",
#             "isuCd": full_code,
#             "isuCd2": full_code,
#             "codeNmisuCd_finder_srtisu0_0": stock_name,
#             "param1isuCd_finder_srtisu0_0": "",
#             "strtDd": current_start_date.strftime("%Y%m%d"),
#             "endDd": current_end_date.strftime("%Y%m%d"),
#             "share": "1",
#             "money": "1",
#             "csvxls_isNo": "false",
#         }

#         response = requests.post(url, headers=headers, data=data)

#         if response.status_code == 200:
#             print(
#                 f"Short selling data retrieved successfully for period {current_start_date.strftime('%Y%m%d')} to {current_end_date.strftime('%Y%m%d')}"
#             )
#             json_data = response.json()

#             for item in json_data["OutBlock_1"]:
#                 date = item["TRD_DD"]
#                 short_selling_qty = item["CVSRTSELL_TRDVOL"]
#                 short_selling_data[date] = short_selling_qty
#         else:
#             print(
#                 f"Failed to retrieve short selling data for period {current_start_date.strftime('%Y%m%d')} to {current_end_date.strftime('%Y%m%d')}"
#             )
#             print(response.text)

#         current_start_date = current_end_date + timedelta(days=1)

#     for data in all_extracted_data:
#         date = data["business_date"]
#         if date in short_selling_data:
#             data["공매도 거래 수량"] = short_selling_data[date]

#     return all_extracted_data


# def to_csv(data, stock_name):
#     filename = f"{stock_name}.csv"
#     try:
#         with open(filename, "w", newline="", encoding="utf-8") as csvfile:
#             fieldnames = [
#                 "business_date",
#                 "종목명",
#                 "시가총액",
#                 "외국인 보유수량",
#                 "공매도 거래 수량",
#             ]
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             writer.writeheader()
#             for entry in data:
#                 writer.writerow(entry)

#         print(f"Filtered data saved to {filename}")

#     except Exception as e:
#         print(f"An error occurred while writing to the CSV file: {e}")
