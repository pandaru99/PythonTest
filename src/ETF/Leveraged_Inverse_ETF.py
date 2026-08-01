import tkinter as tk
from tkinter import ttk, messagebox
from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta
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
REAL_TICKERS = {
    # 인버스 2X
    "0197X0": "SOL SK하이닉스선물단일종목인버스2X",
    "0193L0": "PLUS 삼성전자선물단일종목인버스2X",
    
    # 레버리지 2X (삼성전자)
    "0193W0": "KODEX 삼성전자단일종목레버리지",
    "0195R0": "TIGER 삼성전자단일종목레버리지",
    "0193K0": "PLUS 삼성전자단일종목레버리지",
    "0192M0": "RISE 삼성전자단일종목레버리지",
    "0194N0": "KIWOOM 삼성전자선물단일종목레버리지",
    "0198B0": "1Q 삼성전자선물단일종목레버리지",
    "0194M0": "ACE 삼성전자단일종목레버리지",
    
    # 레버리지 2X (SK하이닉스)
    "0193T0": "KODEX SK하이닉스단일종목레버리지",
    "0195S0": "TIGER SK하이닉스단일종목레버리지",
    "0197W0": "SOL SK하이닉스단일종목레버리지",
    "0192L0": "RISE SK하이닉스단일종목레버리지",
    "0194R0": "KIWOOM SK하이닉스선물단일종목레버리지",
    "0194T0": "ACE SK하이닉스단일종목레버리지",
    "0198D0": "1Q SK하이닉스선물단일종목레버리지",
}

ticker = "0197X0"   # 기본 종목

# ==================== 날짜 관련 함수 ====================
def get_recent_dates(days: int = 60) -> list:
    """최근 N일 달력 날짜 리스트 생성 (최신 → 과거, YYYYMMDD)"""
    dates = []
    today = datetime.now()
    for i in range(days):
        d = today - timedelta(days=i)
        dates.append(d.strftime("%Y%m%d"))
    return dates

def to_business_day(date_str: str) -> str:
    """선택한 일자를 직전 영업일로 보정"""
    return stock.get_nearest_business_day_in_a_week(date_str)

# 초기값
calendar_dates = get_recent_dates(60)          # 콤보박스에 보여줄 달력 날짜
query_date = to_business_day(datetime.now().strftime("%Y%m%d"))  # 직전 영업일
print(f"초기 조회일 (직전 영업일): {query_date}")

# ==================== 데이터 조회 함수 ====================
def get_portfolio_df(selected_ticker: str, selected_date: str) -> tuple:
    """
    selected_date를 직전 영업일로 보정한 후 구성종목 조회
    반환: (DataFrame, 실제_사용된_영업일)
    """
    safe_date = to_business_day(selected_date)   # ★ 핵심: 항상 직전 영업일 적용
    
    try:
        df = stock.get_etf_portfolio_deposit_file(selected_ticker, safe_date)
        if df is None or df.empty:
            df = stock.get_etf_portfolio_deposit_file(selected_ticker)
        
        if df is None or df.empty:
            raise ValueError(f"티커 '{selected_ticker}' / 영업일 '{safe_date}' 데이터 없음")
        
        df = df.reset_index()
        if df.columns[0] != "티커":
            df = df.rename(columns={df.columns[0]: "티커"})
        return df, safe_date
    except Exception as e:
        raise ValueError(f"조회 실패: {e}")


# ==================== 초기 데이터 로드 ====================
try:
    all_etfs = stock.get_etf_ticker_list(query_date)
    single_stock_lev_inv = []

    print("\n=== 레버리지·인버스 단일종목 ETF 목록 검색 중... ===")
    for t in all_etfs:
        try:
            name = stock.get_etf_ticker_name(t)
            if (("단일종목" in name or "선물단일종목" in name) and 
                ("레버리지" in name or "인버스" in name)):
                single_stock_lev_inv.append((t, name))
                print(f"  ✓ {t} : {name}")
        except:
            continue

    if not single_stock_lev_inv:
        print("⚠️ 자동 필터링 결과 없음 → 실제 티커 목록 사용")
        single_stock_lev_inv = [(code, name) for code, name in REAL_TICKERS.items()]

    ticker_name = REAL_TICKERS.get(ticker, stock.get_etf_ticker_name(ticker))
    df, query_date = get_portfolio_df(ticker, query_date)
    
    print(f"\n선택된 ETF: {ticker} ({ticker_name})")
    print(f"실제 조회 영업일: {query_date}")
    print(f"=== 구성종목 (총 {len(df)}개) ===")
    print(df.head(8))

except Exception as e:
    print(f"❌ 초기 오류: {e}")
    sys.exit(1)


# ==================== Tkinter UI ====================
def create_ui(initial_df: pd.DataFrame, etf_list: list, date_list: list):
    root = tk.Tk()
    root.title(f"{ticker} ({ticker_name}) - 레버리지/인버스 단일종목 ETF 구성종목")
    root.geometry("1250x850")

    # ----- 상단 정보 -----
    info_frame = ttk.Frame(root, padding="10")
    info_frame.pack(fill="x")

    title_label = ttk.Label(info_frame, text=f"ETF: {ticker} ({ticker_name})",
                            font=("나눔고딕", 13, "bold"))
    title_label.pack(anchor="w")

    date_label = ttk.Label(info_frame, 
                           text=f"조회 조건 → 선택일 기준 직전 영업일: {query_date}",
                           foreground="darkblue")
    date_label.pack(anchor="w")

    guide_label = ttk.Label(info_frame, 
                            text="※ 날짜를 선택하면 자동으로 '선택된 일자의 직전 영업일'로 보정되어 조회됩니다",
                            foreground="blue")
    guide_label.pack(anchor="w")

    # ----- 선택 영역 -----
    select_frame = ttk.Frame(root, padding="8")
    select_frame.pack(fill="x")

    # 1. ETF 콤보박스
    ttk.Label(select_frame, text="① ETF 선택:").grid(row=0, column=0, sticky="w", padx=5)
    etf_names = [f"{t} | {n}" for t, n in etf_list]
    combo_etf = ttk.Combobox(select_frame, values=etf_names, width=75, state="readonly")
    combo_etf.grid(row=0, column=1, padx=5, sticky="w")
    
    for i, (t, n) in enumerate(etf_list):
        if t == ticker:
            combo_etf.current(i)
            break
    else:
        if etf_names:
            combo_etf.current(0)

    # 2. 날짜 콤보박스
    ttk.Label(select_frame, text="② 날짜 선택:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    combo_date = ttk.Combobox(select_frame, values=date_list, width=15, state="readonly")
    combo_date.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    # 초기 날짜 표시 (현재 영업일)
    combo_date.set(query_date)

    # 현재 적용된 영업일 표시 라벨
    applied_label = ttk.Label(select_frame, text=f"→ 적용 영업일: {query_date}", foreground="green")
    applied_label.grid(row=1, column=2, sticky="w", padx=10)

    # ----- Treeview -----
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    columns = list(initial_df.columns)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=26)

    for col in columns:
        tree.heading(col, text=col)
        if col in ["티커", "종목명"]:
            tree.column(col, width=150, anchor="center")
        elif col in ["계약수", "비중"]:
            tree.column(col, width=110, anchor="e")
        else:
            tree.column(col, width=160, anchor="e")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def populate_tree(df: pd.DataFrame):
        for item in tree.get_children():
            tree.delete(item)
        for _, row in df.iterrows():
            values = [row[col] for col in df.columns]
            tree.insert("", tk.END, values=values)

    populate_tree(initial_df)

    # 현재 상태
    current = {
        "df": initial_df,
        "ticker": ticker,
        "name": ticker_name,
        "date": query_date          # 항상 직전 영업일
    }

    # ===== 공통 재조회 함수 =====
    def reload_data(new_ticker=None, selected_calendar_date=None):
        """
        new_ticker          : 변경할 ETF (None이면 현재 유지)
        selected_calendar_date : 콤보박스에서 고른 날짜 (None이면 현재 유지)
        → 항상 selected_calendar_date의 직전 영업일로 조회
        """
        if new_ticker is None:
            new_ticker = current["ticker"]
        if selected_calendar_date is None:
            selected_calendar_date = current["date"]

        try:
            title_label.config(text=f"ETF: {new_ticker}  ← 조회 중...")
            root.update()

            # ★ 핵심: 선택한 날짜 → 직전 영업일 적용
            new_df, safe_date = get_portfolio_df(new_ticker, selected_calendar_date)
            new_name = REAL_TICKERS.get(new_ticker, stock.get_etf_ticker_name(new_ticker))

            # UI 업데이트
            populate_tree(new_df)
            title_label.config(text=f"ETF: {new_ticker} ({new_name})")
            date_label.config(text=f"조회 조건 → 선택일 기준 직전 영업일: {safe_date}")
            applied_label.config(text=f"→ 적용 영업일: {safe_date}")
            root.title(f"{new_ticker} ({new_name}) - {safe_date}")

            # 콤보박스 동기화 (실제 적용된 영업일로)
            combo_date.set(safe_date)

            # 상태 저장
            current["df"] = new_df
            current["ticker"] = new_ticker
            current["name"] = new_name
            current["date"] = safe_date

            print(f"✅ 조회 완료 → ETF: {new_ticker} | 선택일: {selected_calendar_date} → 영업일: {safe_date} | 항목수: {len(new_df)}")

        except Exception as e:
            messagebox.showerror("조회 오류", str(e))
            title_label.config(text=f"ETF: {current['ticker']} ({current['name']})")

    # ===== 이벤트 바인딩 =====
    def on_etf_select(event=None):
        """ETF 변경 시 → 현재 선택된 날짜 조건으로 조회"""
        selected = combo_etf.get()
        if selected:
            new_ticker = selected.split(" | ")[0].strip()
            if new_ticker != current["ticker"]:
                # 현재 날짜 콤보박스 값을 그대로 사용 (직전 영업일 자동 적용)
                reload_data(new_ticker=new_ticker, selected_calendar_date=combo_date.get())

    def on_date_select(event=None):
        """날짜 변경 시 → 선택한 일자의 직전 영업일로 보정 후 조회"""
        selected_date = combo_date.get()
        if selected_date:
            reload_data(selected_calendar_date=selected_date)

    combo_etf.bind("<<ComboboxSelected>>", on_etf_select)
    combo_date.bind("<<ComboboxSelected>>", on_date_select)

    # ----- 하단 버튼 -----
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    def save_to_csv():
        fname = f"{current['ticker']}_단일종목레버리지인버스_구성종목_{current['date']}.csv"
        current["df"].to_csv(fname, encoding="utf-8-sig", index=False)
        print(f"✅ 저장 완료: {fname}")
        messagebox.showinfo("저장 완료", f"파일이 저장되었습니다.\n{fname}")

    ttk.Button(btn_frame, text="CSV로 저장", command=save_to_csv).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="닫기", command=root.destroy).pack(side="left", padx=8)

    root.mainloop()


# UI 실행
if __name__ == "__main__":
    create_ui(df, single_stock_lev_inv, calendar_dates)