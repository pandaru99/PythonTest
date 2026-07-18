import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
import sys
import os

# ==================== 설정 ====================
ticker = "005930"                    # 삼성전자
ticker_name = "삼성전자"

# 파일 경로 (필요시 수정)
data_file = "005930_KRX_공매도현황_20250717_20260718.csv"   # ← 여기에 실제 파일명 넣기

# ==================== 데이터 로드 ====================
try:
    if not os.path.exists(data_file):
        print(f"❌ 파일을 찾을 수 없습니다: {data_file}")
        print("파일명을 확인하거나 올바른 경로로 수정해주세요.")
        sys.exit(1)

    # CSV 파일 읽기 (날짜 컬럼을 datetime으로 파싱)
    df = pd.read_csv(data_file, encoding="utf-8-sig")
    
    # 컬럼명 정리 (공백 제거)
    df.columns = [col.strip() for col in df.columns]
    
    # 요청한 컬럼 순서로 재정렬
    desired_order = ['날짜', '거래량', '잔고수량', '거래대금', '잔고금액']
    available_cols = [col for col in desired_order if col in df.columns]
    df = df[available_cols]
    
    # 날짜 형식 정리
    if '날짜' in df.columns:
        df['날짜'] = pd.to_datetime(df['날짜']).dt.strftime('%Y-%m-%d')
    
    print(f"✅ 파일 로드 완료: {data_file}")
    print(f"총 {len(df)}개 데이터")
    print(f"\n=== {ticker_name} 공매도 현황 (최근 14일) ===")
    print(df.tail(14))

except Exception as e:
    print(f"❌ 파일 읽기 오류: {e}")
    sys.exit(1)


# ==================== Tkinter UI ====================
def create_ui(df: pd.DataFrame):
    root = tk.Tk()
    root.title(f"{ticker} ({ticker_name}) - 공매도 현황")
    root.geometry("1150x780")

    # 상단 정보
    info_frame = ttk.Frame(root, padding="10")
    info_frame.pack(fill="x")
    
    ttk.Label(info_frame, text=f"종목: {ticker} ({ticker_name})", 
              font=("나눔고딕", 12, "bold")).pack(anchor="w")
    ttk.Label(info_frame, text=f"데이터 파일: {data_file}").pack(anchor="w")
    ttk.Label(info_frame, text=f"총 데이터 수: {len(df)}개").pack(anchor="w")
    ttk.Label(info_frame, text="※ 컬럼 순서: 날짜 → 거래량 → 잔고수량 → 거래대금 → 잔고금액", 
              foreground="blue").pack(anchor="w")

    # Treeview
    columns = list(df.columns)
    tree = ttk.Treeview(root, columns=columns, show="headings", height=28)
    
    # 헤더 및 컬럼 설정
    for col in columns:
        tree.heading(col, text=col)
        if col == "날짜":
            tree.column(col, width=110, anchor="center")
        elif col in ["거래량", "잔고수량"]:
            tree.column(col, width=140, anchor="e")
        else:  # 거래대금, 잔고금액
            tree.column(col, width=170, anchor="e")
    
    # 데이터 삽입 (최근 날짜가 위로)
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
    
    ttk.Button(btn_frame, text="CSV로 저장 (현재 순서)", 
               command=lambda: save_to_csv(df)).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="닫기", 
               command=root.destroy).pack(side="left", padx=8)

    root.mainloop()


def save_to_csv(df: pd.DataFrame):
    filename = f"{ticker}_공매도현황_정렬됨_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, encoding="utf-8-sig", index=False)
    print(f"✅ 저장 완료: {filename}")


# UI 실행
if __name__ == "__main__":
    create_ui(df)