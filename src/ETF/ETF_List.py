import tkinter as tk
from tkinter import ttk
from pykrx import stock
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

# ==================== 1. 환경 변수 로드 ====================
load_dotenv()

krx_id = os.getenv("KRX_ID")
krx_pw = os.getenv("KRX_PW")

if not krx_id or not krx_pw:
    print("❌ .env 파일에 KRX_ID와 KRX_PW를 설정해주세요!")
    sys.exit(1)

print("✅ KRX 로그인 정보 로드 완료")

# ==================== 2. 설정 ====================
# ETF 예시: KODEX 200
ticker = "069500"                    # ETF 티커 (변경 가능)
ticker_name = stock.get_etf_ticker_name(ticker)
# 조회일 (PDF는 특정 일자 기준, None이면 최근 영업일)
query_date = datetime.now().strftime("%Y%m%d")   # 또는 "20260731" 등으로 고정 가능

print(f"조회일: {query_date} | ETF: {ticker} ({ticker_name})")

# ==================== 3. ETF 항목(구성종목) 조회 ====================
try:
    # ETF 구성종목(PDF) 조회
    df = stock.get_etf_portfolio_deposit_file(ticker, query_date)

    if df is None or df.empty:
        print("⚠️ 해당 일자에 ETF 구성종목 데이터가 없습니다. 최근 영업일로 재시도합니다.")
        df = stock.get_etf_portfolio_deposit_file(ticker)  # 날짜 미지정 → 최근 영업일

    if df.empty:
        print("⚠️ ETF 구성종목 데이터를 가져올 수 없습니다.")
        sys.exit(1)

    # 컬럼 정리 (일반적으로 '계약수', '금액', '비중' 등)
    # 필요 시 원하는 순서로 재정렬
    print(f"\n=== {ticker_name} ETF 구성종목 (총 {len(df)}개 항목) ===")
    print(df.head(20))  # 콘솔 미리보기

    # 인덱스(티커)를 컬럼으로 변환해서 UI에 표시하기 좋게
    df = df.reset_index()
    if '티커' not in df.columns and df.columns[0] != '티커':
        df = df.rename(columns={df.columns[0]: '티커'})

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    print("KRX 계정 정보 확인 또는 영업일/ETF 티커인지 확인해주세요.")
    sys.exit(1)


# ==================== 4. Tkinter UI ====================
def create_ui(df: pd.DataFrame):
    root = tk.Tk()
    root.title(f"{ticker} ({ticker_name}) - ETF 구성종목 현황")
    root.geometry("1100x750")

    # 상단 정보
    info_frame = ttk.Frame(root, padding="10")
    info_frame.pack(fill="x")
    
    ttk.Label(info_frame, text=f"ETF: {ticker} ({ticker_name})", 
              font=("나눔고딕", 12, "bold")).pack(anchor="w")
    ttk.Label(info_frame, text=f"조회일: {query_date}").pack(anchor="w")
    ttk.Label(info_frame, text="※ ETF 구성종목(PDF) 항목: 티커 / 계약수 / 금액 / 비중 등", 
              foreground="blue").pack(anchor="w")

    # Treeview
    columns = list(df.columns)
    tree = ttk.Treeview(root, columns=columns, show="headings", height=25)
    
    # 헤더 및 컬럼 너비 설정
    for col in columns:
        tree.heading(col, text=col)
        if col in ["티커", "종목명"]:
            tree.column(col, width=120, anchor="center")
        elif col in ["계약수", "비중"]:
            tree.column(col, width=100, anchor="e")
        else:  # 금액 등
            tree.column(col, width=150, anchor="e")
    
    # 데이터 삽입
    for _, row in df.iterrows():
        values = [row[col] for col in columns]
        tree.insert("", tk.END, values=values)

    # 스크롤바
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
    scrollbar.pack(side="right", fill="y")

    # 하단 버튼
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)
    
    ttk.Button(btn_frame, text="CSV로 저장", 
               command=lambda: save_to_csv(df)).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="닫기", 
               command=root.destroy).pack(side="left", padx=8)

    root.mainloop()


def save_to_csv(df: pd.DataFrame):
    filename = f"{ticker}_ETF구성종목_{query_date}.csv"
    df.to_csv(filename, encoding="utf-8-sig", index=False)
    print(f"✅ 저장 완료: {filename}")


# UI 실행
if __name__ == "__main__":
    create_ui(df)