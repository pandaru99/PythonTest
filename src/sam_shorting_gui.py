import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pykrx import stock
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

# 환경 변수 로드
load_dotenv()
krx_id = os.getenv("KRX_ID")
krx_pw = os.getenv("KRX_PW")

if not krx_id or not krx_pw:
    print("❌ .env 파일에 KRX_ID와 KRX_PW를 설정해주세요!")
    sys.exit(1)

# ==================== 메인 GUI ====================
class ShortingViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KRX 공매도 데이터 조회기")
        self.root.geometry("1250x820")
        
        self.df = None
        self.ticker = tk.StringVar(value="0198D0")
        self.start_date = tk.StringVar(value="20250701")
        self.end_date = tk.StringVar(value=datetime.now().strftime("%Y%m%d"))
        
        self.create_widgets()

    def create_widgets(self):
        # 입력 프레임
        input_frame = ttk.LabelFrame(self.root, text="조회 설정", padding=12)
        input_frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(input_frame, text="종목코드:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(input_frame, textvariable=self.ticker, width=12).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="조회 항목:").grid(row=0, column=2, sticky="w", padx=5)
        self.func_combo = ttk.Combobox(input_frame, width=38, state="readonly")
        self.func_combo['values'] = [
            "get_shorting_status_by_date (종합)",
            "get_shorting_volume_by_date (거래량)",
            "get_shorting_value_by_date (거래대금)",
            "get_shorting_balance_by_date (잔고)",
            "get_shorting_volume_top50 (전체 거래량 Top50)",
            "get_shorting_balance_top50 (전체 잔고 Top50)"
        ]
        self.func_combo.current(0)
        self.func_combo.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="시작일:").grid(row=1, column=0, sticky="w", padx=5, pady=6)
        ttk.Entry(input_frame, textvariable=self.start_date, width=12).grid(row=1, column=1, padx=5, pady=6)
        
        ttk.Label(input_frame, text="종료일:").grid(row=1, column=2, sticky="w", padx=5, pady=6)
        ttk.Entry(input_frame, textvariable=self.end_date, width=12).grid(row=1, column=3, padx=5, pady=6)

        # 버튼
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="🔍 조회하기", command=self.fetch_data).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="💾 CSV 저장", command=self.save_csv).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="❌ 종료", command=self.root.destroy).pack(side="left", padx=6)

        # 결과 영역
        result_frame = ttk.LabelFrame(self.root, text="조회 결과", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(result_frame, show="headings", height=28)
        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.status = ttk.Label(self.root, text="준비됨", foreground="gray")
        self.status.pack(pady=6)

    def fetch_data(self):
        try:
            func_name = self.func_combo.get()
            ticker = self.ticker.get().strip()
            start = self.start_date.get().strip()
            end = self.end_date.get().strip()

            self.status.config(text="조회 중...", foreground="blue")
            self.root.update()

            if "Top50" in func_name:
                # ==================== 주말 처리 ====================
                today = datetime.now()
                weekday = today.weekday()  # 0=월 ~ 4=금, 5=토, 6=일
                
                if weekday >= 5:  # 토요일(5) 또는 일요일(6)
                    # 가장 최근 금요일로 이동
                    days_back = weekday - 4  # 토요일:1일 전, 일요일:2일 전
                    query_date = (today - pd.Timedelta(days=days_back)).strftime("%Y%m%d")
                    print(f"🗓️ 주말 감지 → {query_date} (최근 금요일) 데이터 사용")
                else:
                    query_date = today.strftime("%Y%m%d")
                
                # Top50 조회
                if "거래량" in func_name:
                    self.df = stock.get_shorting_volume_top50(query_date)
                else:
                    self.df = stock.get_shorting_balance_top50(query_date)
                
                self.status.config(text=f"Top50 조회 ({query_date})", foreground="blue")
            else:
                # 기존 종목별 조회 (변경 없음)
                if "종합" in func_name:
                    self.df = stock.get_shorting_status_by_date(start, end, ticker)
                elif "거래량" in func_name:
                    self.df = stock.get_shorting_volume_by_date(start, end, ticker)
                elif "거래대금" in func_name:
                    self.df = stock.get_shorting_value_by_date(start, end, ticker)
                else:
                    self.df = stock.get_shorting_balance_by_date(start, end, ticker)

            if self.df is None or self.df.empty:
                messagebox.showwarning("결과 없음", "해당 기간/조건에 데이터가 없습니다.")
                self.status.config(text="데이터 없음", foreground="orange")
                return

            self.display_data()
            self.status.config(text=f"조회 완료 — {len(self.df)} 건", foreground="green")

            # 파일 저장
            filename = f"{ticker}_{func_name}_{start}_{end}.csv"
            self.df.to_csv(filename, encoding="utf-8-sig")
            print(f"\n✅ 저장 완료: {filename}")

        except Exception as e:
            messagebox.showerror("조회 오류", f"{func_name} 호출 실패:\n{str(e)}")
            self.status.config(text="조회 실패", foreground="red")

    def display_data(self):
        # 이전 컬럼 모두 제거
        self.tree["columns"] = ()
        
        columns = list(self.df.columns)
        self.tree["columns"] = columns

        # 컬럼 헤더 및 너비 설정
        for col in columns:
            self.tree.heading(col, text=col)
            # 숫자 컬럼은 오른쪽 정렬
            if col in ['거래량', '잔고수량', '거래대금', '잔고금액', 'BAL_QTY', 'BAL_AMT', 'MKTCAP', 'VOL']:
                self.tree.column(col, width=130, anchor="e")
            else:
                self.tree.column(col, width=110, anchor="center")

        # 데이터 삽입 (최신 데이터가 위로)
        for _, row in self.df[::-1].iterrows():
            self.tree.insert("", tk.END, values=[row[col] for col in columns])

    def save_csv(self):
        if self.df is None or self.df.empty:
            messagebox.showwarning("경고", "먼저 데이터를 조회해주세요.")
            return

        try:
            default_name = f"공매도_{self.ticker.get()}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV 파일", "*.csv")],
                initialfile=default_name
            )
            if filename:
                self.df.to_csv(filename, encoding="utf-8-sig", index=False)
                messagebox.showinfo("저장 성공", f"파일이 저장되었습니다:\n{filename}")
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))


if __name__ == "__main__":
    app = ShortingViewer()
    app.root.mainloop()