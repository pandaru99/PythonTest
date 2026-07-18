from pykrx import stock
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# ==================== 1. 환경 변수 로드 ====================
load_dotenv()  # .env 파일 읽기

krx_id = os.getenv("KRX_ID")
krx_pw = os.getenv("KRX_PW")

if not krx_id or not krx_pw:
    raise ValueError("❌ .env 파일에 KRX_ID와 KRX_PW를 설정해주세요!")

print("✅ KRX 로그인 정보 로드 완료")

# ==================== 2. 설정 ====================
ticker = "005930"                    # 삼성전자
start_date = "20250717"              # 조회 시작일 (YYYYMMDD)
end_date = datetime.now().strftime("%Y%m%d")

print(f"조회 기간: {start_date} ~ {end_date} | 종목: {ticker} ({stock.get_market_ticker_name(ticker)})")

# ==================== 3. 데이터 조회 ====================
try:
    # 종목별 공매도 현황 (거래량 + 잔고 + 금액)
    df = stock.get_shorting_status_by_date(
        fromdate=start_date,
        todate=end_date,
        ticker=ticker
    )

    # 결과 출력
    print("\n=== 삼성전자 공매도 현황 (최근 14일) ===")
    print(df.tail(250))

    # 추가 정보: 공매도 거래량 Top (전체 시장)
    print("\n=== 최근 공매도 거래량 Top 10 (전체 종목) ===")
    df_top_vol = stock.get_shorting_volume_top50(datetime.now().strftime("%Y%m%d"))
    print(df_top_vol.head(10))

    # 파일 저장
    filename = f"{ticker}_KRX_공매도현황_{start_date}_{end_date}.csv"
    df.to_csv(filename, encoding="utf-8-sig")
    print(f"\n✅ 저장 완료: {filename}")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    print("KRX 계정 정보가 정확한지, 또는 KRX 사이트가 정상인지 확인해주세요.")
    print("※ 공매도 데이터는 영업일 기준으로 제공되며, 지연될 수 있습니다.")



# 사용 방법

# 기존 sam1.py와 같은 폴더에 sam_shorting.py로 저장
# .env 파일에 KRX_ID/PW 설정 (이미 있으면 그대로 사용)
# 실행: python sam_shorting.py

# 추가로 알아두면 좋은 함수 (pykrx 공매도)

# stock.get_shorting_volume_by_date(...) : 공매도 거래량만
# stock.get_shorting_value_by_date(...) : 공매도 거래대금
# stock.get_shorting_balance_by_date(...) : 잔고 중심
# stock.get_shorting_volume_top50(date) / get_shorting_balance_top50(date) : 상위 종목
# 필요하면 여러 종목 한번에 조회하거나, 가격 데이터와 함께 병합하는 버전도 만들어드릴게요!