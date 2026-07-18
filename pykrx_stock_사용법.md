**✅ 아래 전체 내용을 그대로 복사해서 `pykrx_stock_사용법.md` 파일로 저장하세요.**

```markdown
# pykrx.stock 사용법 가이드 (한글)

`from pykrx import stock` 모듈에서 제공하는 주요 함수들을 정리한 가이드입니다.

---

## 1. 종목 기본 정보

### `get_market_ticker_list(date=None, market="ALL")`
- **설명**: 특정 날짜의 시장별 종목 티커 리스트를 반환합니다.
- **market 옵션**: `"ALL"`, `"KOSPI"`, `"KOSDAQ"`, `"KONEX"`

### `get_market_ticker_name(ticker)`
- **설명**: 티커 코드로 종목명을 반환합니다.
```python
print(stock.get_market_ticker_name("005930"))  # 삼성전자
```

---

## 2. 가격 데이터 (OHLCV)

### `get_market_ohlcv(fromdate, todate, ticker, freq='d')`
- **설명**: 개별 종목의 일봉(OHLCV) 데이터를 가져옵니다. (가장 기본적이고 자주 사용)

### `get_market_ohlcv_by_date(fromdate, todate, ticker)`
- **설명**: 기간 동안의 OHLCV 데이터

### `get_market_ohlcv_by_ticker(date)`
- **설명**: 특정 날짜의 **전체 종목** OHLCV 데이터

---

## 3. 투자자별 매매동향 (가장 중요)

### `get_market_trading_volume_by_investor(fromdate, todate, ticker)`
- **설명**: **투자자별 거래량** (개인, 기관, 외국인, 기타)
- **너의 기존 스크립트에서 사용 중인 함수**

### `get_market_trading_value_by_investor(fromdate, todate, ticker)`
- **설명**: **투자자별 거래대금** (금액 기준)

### `get_market_trading_value_and_volume_by_ticker(date)`
- **설명**: 특정 날짜의 종목별 투자자 거래대금 및 거래량

---

## 4. 시가총액 / 펀더멘털

### `get_market_cap(date=None, market="ALL")`
- **설명**: 시가총액 순위

### `get_market_fundamental(fromdate, todate, ticker)`
- **설명**: PER, PBR, EPS, BPS, DIV 등 기본 지표

### `get_market_price_change(fromdate, todate)`
- **설명**: 기간 내 상승/하락률

---

## 5. 지수 (Index) 관련

- `get_index_ticker_list()`
- `get_index_ticker_name()`
- `get_index_ohlcv()`
- `get_index_fundamental()`

---

## 6. ETF / ETN / 선물 / ELW

- `get_etf_ticker_list()`, `get_etf_ohlcv_by_date()`
- `get_etn_ticker_list()`
- `get_future_ticker_list()`, `get_future_ohlcv()`
- `get_elw_ticker_list()`

---

## 7. 공매도 데이터

- `get_shorting_volume_by_date()`
- `get_shorting_value_by_date()`
- `get_shorting_balance_by_date()`
- `get_shorting_volume_top50()`
- `get_shorting_balance_top50()`

---

## 8. 유틸리티 함수

- `get_business_days(start_date, end_date)`: 영업일 리스트
- `get_previous_business_days(date, n=1)`: 이전 영업일
- `get_stock_major_changes(ticker)`: 주요 변동 내역 (증자, 감자 등)
- `get_exhaustion_rates_of_foreign_investment()`: 외국인 보유한도 소진율

---

## 전체 사용 예제

```python
from pykrx import stock
from datetime import datetime
import pandas as pd

ticker = "005930"                    # 삼성전자
start_date = "20260601"
end_date = datetime.now().strftime("%Y%m%d")

print(f"조회 기간: {start_date} ~ {end_date}")

# 1. 투자자별 매매동향
df_vol = stock.get_market_trading_volume_by_investor(start_date, end_date, ticker)
df_val = stock.get_market_trading_value_by_investor(start_date, end_date, ticker)

# 2. 가격 데이터
df_price = stock.get_market_ohlcv(start_date, end_date, ticker)

print("\n=== 투자자별 거래량 ===")
print(df_vol.tail(10))

print("\n=== 가격 데이터 ===")
print(df_price.tail(5))

# 저장
df_vol.to_csv(f"{ticker}_투자자_거래량.csv", encoding="utf-8-sig")
```

---

**작성일**: 2026-07-12  
**버전**: pykrx 1.2.8 기준

필요하면 특정 함수를 더 자세히 추가하거나 예제를 확장해드릴게요!
```

---

**복사해서 사용하세요!**  
파일로 저장할 때는 위 내용을 그대로 붙여넣기 하면 됩니다.