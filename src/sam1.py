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
ticker = "005930"                    # 삼성전자 예시
start_date = "20260601"
end_date = datetime.now().strftime("%Y%m%d")

print(f"조회 기간: {start_date} ~ {end_date} | 종목: {ticker}")

# ==================== 3. 데이터 조회 ====================
try:
    df = stock.get_market_trading_volume_by_investor(
        fromdate=start_date,
        todate=end_date,
        ticker=ticker
    )

    # 결과 출력
    print("\n=== 최근 10일 투자자별 매매동향 ===")
    print(df.tail(14))

    # 파일 저장
    filename = f"{ticker}_KRX_투자자매매동향_{start_date}_{end_date}.csv"

    df.to_csv(filename, encoding="utf-8-sig", index=False)
    print(f"\n✅ 저장 완료: {filename}")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    print("KRX 계정 정보가 정확한지, 또는 KRX 사이트가 정상인지 확인해주세요.")