"""
collect_data.py

[이 파일이 하는 일]
코스피(KOSPI), 원/달러 환율, 한국은행 기준금리 - 이렇게 3개의 데이터를
각각 인터넷에서 받아온 다음, 날짜를 기준으로 하나의 표(CSV 파일)로 합칩니다.

[사용하는 데이터 출처]
- 코스피 지수(종가, 거래량)   : FinanceDataReader 라이브러리, 티커 'KS11'
- 원/달러 환율               : FinanceDataReader 라이브러리, 티커 'USD/KRW'
- 한국은행 기준금리           : FinanceDataReader 라이브러리, 'ECOS-KEYSTAT:K051'
  (한국은행 API 키 없이도 가져올 수 있는 100대 통계지표 중 하나예요)

[결과물]
data/merged_raw.csv 파일이 생성됩니다. 컬럼 구성:
  date(날짜), kospi_close(코스피 종가), kospi_volume(코스피 거래량),
  usd_krw(원/달러 환율), base_rate(기준금리)
"""

import sys
import os
import pandas as pd
import FinanceDataReader as fdr

# Windows 콘솔(cmd, PowerShell)에서 한글 print()가 깨져 보이는 문제를 막기 위한 설정.
# 콘솔 자체의 인코딩과 무관하게, 파이썬이 출력할 때 UTF-8을 강제로 쓰게 합니다.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 데이터를 언제부터 언제까지 가져올지 설정하는 부분입니다.
# END_DATE를 None으로 두면 "오늘까지"를 의미해요.
START_DATE = "2010-01-01"
END_DATE = None


def fetch_kospi(start, end):
    """
    코스피 지수 데이터를 가져오는 함수.
    fdr.DataReader('KS11', ...) 한 줄이면 코스피의 시가/고가/저가/종가/거래량이
    전부 담긴 표(DataFrame)를 받아올 수 있어요.
    우리는 이 중에서 종가(Close)와 거래량(Volume)만 사용할 거예요.
    """
    raw = fdr.DataReader("KS11", start, end)

    # 원본 컬럼 이름은 영어로 'Close', 'Volume' 이런 식이에요.
    # 나중에 다른 데이터(환율, 금리)와 합쳤을 때 헷갈리지 않도록
    # 이름을 우리가 알아보기 쉬운 이름으로 바꿔줍니다.
    kospi = raw[["Close", "Volume"]].rename(
        columns={"Close": "kospi_close", "Volume": "kospi_volume"}
    )
    return kospi


def fetch_usd_krw(start, end):
    """
    원/달러 환율 데이터를 가져오는 함수.
    코스피와 마찬가지로 fdr.DataReader 한 줄로 가져올 수 있어요.
    """
    raw = fdr.DataReader("USD/KRW", start, end)
    fx = raw[["Close"]].rename(columns={"Close": "usd_krw"})
    return fx


def fetch_base_rate(start, end):
    """
    한국은행 기준금리 데이터를 가져오는 함수.

    주의할 점: 기준금리는 코스피/환율처럼 '매일' 바뀌는 데이터가 아니에요.
    한국은행 금융통화위원회가 회의를 열어서 "금리를 올린다/내린다/유지한다"를
    결정하는 날에만 값이 바뀌어요. 그래서 이 함수가 반환하는 표에는
    날짜가 듬성듬성 있을 수 있어요. (이 문제는 뒤에서 처리합니다.)
    """
    raw = fdr.DataReader("ECOS-KEYSTAT:K051", start, end)

    # 이 API는 컬럼 이름이 매번 조금씩 다르게 나올 수 있어서,
    # "몇 번째 컬럼인지"가 아니라 "첫 번째 컬럼"을 기준금리로 간주합니다.
    first_column_name = raw.columns[0]
    rate = raw[[first_column_name]].rename(columns={first_column_name: "base_rate"})
    return rate


def merge_all_sources(kospi, fx, rate):
    """
    코스피 / 환율 / 기준금리, 이렇게 3개의 표를 날짜 기준으로 하나로 합치는 함수.

    join()은 "같은 날짜 기준으로 옆으로 이어붙인다"는 의미예요.
    엑셀에서 VLOOKUP으로 다른 시트의 값을 가져와서 붙이는 것과 비슷해요.
    """
    merged = kospi.join(fx, how="left")
    merged = merged.join(rate, how="left")

    # 기준금리는 정책이 바뀌는 날에만 값이 있고, 그 외의 날짜는 비어있어요(NaN).
    # ffill()은 "바로 위에 있는 값으로 빈 칸을 채운다"는 뜻이에요.
    # 예: 1월 1일 금리 3.5%, 1월 2~10일은 비어있음
    #     -> ffill() 적용 후 1월 2~10일도 전부 3.5%로 채워짐
    #     (다음 결정일 전까지는 그 금리가 계속 적용되고 있었으니까요)
    merged["base_rate"] = merged["base_rate"].ffill()

    # 코스피나 환율 값 자체가 없는 날(휴장일 등)은 분석에 쓸 수 없으니 제거합니다.
    merged = merged.dropna(subset=["kospi_close", "usd_krw"])

    merged.index.name = "date"
    return merged


def fetch_from_raw_ecos_api(stat_code, item_code1, cycle, start, end):
    """
    [참고용] FinanceDataReader의 ECOS-KEYSTAT에 없는 세부 통계가 필요할 때 쓰는 예비 함수.
    이건 지금 당장 안 써도 되고, 나중에 다른 한국은행 통계가 필요해지면 완성하면 돼요.

    이 방식을 쓰려면 https://ecos.bok.or.kr 에서 무료로 개인 API 키를 발급받아야 하고,
    아래처럼 환경변수로 등록해서 사용해요 (코드에 직접 키를 적으면 안 돼요):

        export ECOS_API_KEY="발급받은_키"
    """
    api_key = os.environ.get("ECOS_API_KEY")
    if not api_key:
        raise RuntimeError("먼저 ECOS_API_KEY 환경변수를 설정해주세요.")

    url = (
        f"https://ecos.bok.or.kr/api/StatisticSearch/{api_key}/json/kr/1/10000/"
        f"{stat_code}/{cycle}/{start}/{end}/{item_code1}"
    )
    # TODO: requests로 url을 호출하고, 응답(JSON)을 DataFrame으로 변환하는 코드 작성
    raise NotImplementedError("아직 구현되지 않았어요. 지금은 사용하지 않아도 됩니다.")


def main():
    print("1/4) 코스피 데이터 가져오는 중...")
    kospi = fetch_kospi(START_DATE, END_DATE)

    print("2/4) 원/달러 환율 데이터 가져오는 중...")
    fx = fetch_usd_krw(START_DATE, END_DATE)

    print("3/4) 기준금리 데이터 가져오는 중...")
    rate = fetch_base_rate(START_DATE, END_DATE)

    print("4/4) 세 데이터를 날짜 기준으로 합치는 중...")
    merged = merge_all_sources(kospi, fx, rate)

    os.makedirs("data", exist_ok=True)
    output_path = "data/merged_raw.csv"
    merged.to_csv(output_path)

    print("\n완료! 최근 5줄 미리보기:")
    print(merged.tail())
    print(f"\n총 {len(merged)}개 행을 {output_path} 에 저장했습니다.")


if __name__ == "__main__":
    main()
