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
ticker = "005930"                    # 삼성전자
ticker_name = stock.get_market_ticker_name(ticker)
start_date = "20250701"              # 조회 시작일 (조정 가능)
end_date = datetime.now().strftime("%Y%m%d")

print(f"조회 기간: {start_date} ~ {end_date} | 종목: {ticker} ({ticker_name})")

# ==================== 3. 데이터 조회 ====================
try:
    # 종목별 공매도 현황
    df = stock.get_shorting_status_by_date(
        fromdate=start_date,
        todate=end_date,
        ticker=ticker
    )

    if df.empty:
        print("⚠️ 해당 기간에 공매도 데이터가 없습니다.")
        sys.exit(1)

    # 컬럼 순서 재정렬 (요청한 순서)
    desired_order = ['날짜', '거래량', '잔고수량', '거래대금', '잔고금액']
    # 실제 존재하는 컬럼만 사용
    available_cols = [col for col in desired_order if col in df.columns]
    df = df[available_cols]

    # 최근 데이터만 출력 (콘솔)
    print(f"\n=== {ticker_name} 공매도 현황 (최근 {min(14, len(df))}일) ===")
    print(df.tail(14))

    # 전체 시장 공매도 Top 10
    today = datetime.now().strftime("%Y%m%d")
    df_top = stock.get_shorting_volume_top50(today)
    print(f"\n=== 오늘 공매도 거래량 Top 10 (전체 종목) ===")
    print(df_top.head(10))

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    print("KRX 계정 정보 확인 또는 영업일인지 확인해주세요.")
    sys.exit(1)


# ==================== 4. Tkinter UI ====================
def create_ui(df: pd.DataFrame):
    root = tk.Tk()
    root.title(f"{ticker} ({ticker_name}) - 공매도 현황")
    root.geometry("1100x750")

    # 상단 정보
    info_frame = ttk.Frame(root, padding="10")
    info_frame.pack(fill="x")
    
    ttk.Label(info_frame, text=f"종목: {ticker} ({ticker_name})", 
              font=("나눔고딕", 12, "bold")).pack(anchor="w")
    ttk.Label(info_frame, text=f"조회 기간: {start_date} ~ {end_date}").pack(anchor="w")
    ttk.Label(info_frame, text="※ 컬럼 순서: 날짜 → 거래량 → 잔고수량 → 거래대금 → 잔고금액", 
              foreground="blue").pack(anchor="w")

    # Treeview
    columns = list(df.columns)
    tree = ttk.Treeview(root, columns=columns, show="headings", height=25)
    
    # 헤더 및 컬럼 너비 설정
    for col in columns:
        tree.heading(col, text=col)
        if col == "날짜":
            tree.column(col, width=100, anchor="center")
        elif col in ["거래량", "잔고수량"]:
            tree.column(col, width=130, anchor="e")
        else:  # 거래대금, 잔고금액
            tree.column(col, width=150, anchor="e")
    
    # 데이터 삽입 (최근 데이터가 위로 오도록)
    for _, row in df[::-1].iterrows():
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
    filename = f"{ticker}_공매도현황_{start_date}_{end_date}.csv"
    df.to_csv(filename, encoding="utf-8-sig", index=False)
    print(f"✅ 저장 완료: {filename}")


# UI 실행
if __name__ == "__main__":
    create_ui(df)