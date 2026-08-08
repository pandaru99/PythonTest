# 레버리지/인버스 + KOSPI200 ETF 조회 프로그램 (최종 업데이트 - 괴리율 추가)

## 전체 코드
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
    # ==================== 인버스 2X (삼성·하이닉스) ====================
    "0193L0": "PLUS 삼성전자선물단일종목인버스2X",
    "0197X0": "SOL SK하이닉스선물단일종목인버스2X",

    # ==================== 레버리지 2X - 삼성전자 ====================
    "0193W0": "KODEX 삼성전자단일종목레버리지",
    "0195R0": "TIGER 삼성전자단일종목레버리지",
    "0193K0": "PLUS 삼성전자단일종목레버리지",
    "0192M0": "RISE 삼성전자단일종목레버리지",
    "0194N0": "KIWOOM 삼성전자선물단일종목레버리지",
    "0198B0": "1Q 삼성전자선물단일종목레버리지",
    "0194M0": "ACE 삼성전자단일종목레버리지",

    # ==================== 레버리지 2X - SK하이닉스 ====================
    "0193T0": "KODEX SK하이닉스단일종목레버리지",
    "0195S0": "TIGER SK하이닉스단일종목레버리지",
    "0197W0": "SOL SK하이닉스단일종목레버리지",
    "0192L0": "RISE SK하이닉스단일종목레버리지",
    "0194R0": "KIWOOM SK하이닉스선물단일종목레버리지",
    "0194T0": "ACE SK하이닉스단일종목레버리지",
    "0198D0": "1Q SK하이닉스선물단일종목레버리지",

    # ==================== KOSPI200 선물 레버리지 2X ====================
    "122630": "KODEX 레버리지",
    "123320": "TIGER 레버리지",
    "252400": "RISE 200선물레버리지",
    "267770": "TIGER 200선물레버리지",
    "253150": "PLUS 200선물레버리지",
    "253250": "KIWOOM 200선물레버리지",
    "304780": "HANARO 200선물레버리지",
    "152500": "ACE 레버리지",

    # ==================== KOSPI200 선물 인버스 (-1X) ====================
    "114800": "KODEX 인버스",
    "123310": "TIGER 인버스",
    "252410": "RISE 200선물인버스",
    "253240": "KIWOOM 200선물인버스",

    # ==================== KOSPI200 선물 인버스 2X ====================
    "252670": "KODEX 200선물인버스2X",
    "252710": "TIGER 200선물인버스2X",
    "253160": "PLUS 200선물인버스2X",

    # ==================== KOSPI200 현물 ETF ====================
    "069500": "KODEX 200",
    "102110": "TIGER 200",
    "148020": "RISE 200",
    "152100": "PLUS 200",
    "105190": "ACE 200",
    "069660": "KIWOOM 200",
    "293180": "HANARO 200",

    # TR 버전
    "278530": "KODEX 200TR",
    "310960": "TIGER 200TR",
    "361580": "RISE 200TR",
    "332500": "ACE 200TR",
    "332930": "HANARO 200TR",
}

REAL_FUNCTION = {
    "000001": "구성종목 (get_etf_portfolio_deposit_file)",
    "000002": "일반 OHLCV (get_market_ohlcv)",
    "000003": "ETF OHLCV by Date (get_etf_ohlcv_by_date)",
    "000004": "구성종목 최신일 (get_etf_portfolio_deposit_file)",
    "000005": "ETF 일별 OHLCV (get_etf_ohlcv_by_ticker)",
    "000006": "ETF 등락률 (get_etf_price_change_by_ticker)",
    "000007": "ETF 추적오차 (get_etf_tracking_error)",
    "000008": "ETF 괴리율 (get_etf_price_deviation)",          # ★ 신규 추가
    "000009": "ETF 월별 OHLCV (get_etf_ohlcv_by_date freq=m)",  # ★ 신규 추가
}

ticker = "0197X0"
funcNM = "000001"

# ==================== 날짜 관련 함수 ====================
def get_recent_dates(days: int = 60) -> list:
    dates = []
    today = datetime.now()
    for i in range(days):
        d = today - timedelta(days=i)
        dates.append(d.strftime("%Y%m%d"))
    return dates

def to_business_day(date_str: str) -> str:
    return stock.get_nearest_business_day_in_a_week(date_str)

calendar_dates = get_recent_dates(60)
query_date = to_business_day(datetime.now().strftime("%Y%m%d"))
print(f"초기 조회일 (직전 영업일): {query_date}")

# ==================== 데이터 조회 함수 ====================
def get_portfolio_df(selected_ticker: str, selected_date: str, selected_func: str) -> tuple:
    safe_date = to_business_day(selected_date)
    
    start_dt = datetime.strptime(safe_date, "%Y%m%d") - timedelta(days=30)
    start_date = start_dt.strftime("%Y%m%d")
    
    try:
        df = None
        
        match selected_func:
            # 구성종목
            case "000001" | "000004":
                df = stock.get_etf_portfolio_deposit_file(selected_ticker, safe_date)
                if df is None or df.empty:
                    df = stock.get_etf_portfolio_deposit_file(selected_ticker)
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "티커":
                    df = df.rename(columns={df.columns[0]: "티커"})

            # 일반 시장 OHLCV
            case "000002":
                df = stock.get_market_ohlcv(start_date, safe_date, selected_ticker)
                if df is None or df.empty:
                    df = stock.get_market_ohlcv(safe_date, safe_date, selected_ticker)
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "날짜":
                    df = df.rename(columns={df.columns[0]: "날짜"})

            # ETF OHLCV by Date (일별)
            case "000003":
                df = stock.get_etf_ohlcv_by_date(start_date, safe_date, selected_ticker)
                if df is None or df.empty:
                    df = stock.get_etf_ohlcv_by_date(safe_date, safe_date, selected_ticker)
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "날짜":
                    df = df.rename(columns={df.columns[0]: "날짜"})
                desired_cols = ["날짜", "NAV", "시가", "고가", "저가", "종가", "거래량", "거래대금", "기초지수"]
                existing_cols = [c for c in desired_cols if c in df.columns]
                df = df[existing_cols]

            # ETF 일별 OHLCV (특정일 전체 중 해당 티커)
            case "000005":
                df = stock.get_etf_ohlcv_by_ticker(safe_date)
                if selected_ticker in df.index:
                    df = df.loc[[selected_ticker]].reset_index()
                    df = df.rename(columns={df.columns[0]: "티커"})
                else:
                    df = pd.DataFrame()

            # ETF 등락률
            case "000006":
                df = stock.get_etf_price_change_by_ticker(start_date, safe_date)
                if selected_ticker in df.index:
                    df = df.loc[[selected_ticker]].reset_index()
                    df = df.rename(columns={df.columns[0]: "티커"})
                else:
                    df = pd.DataFrame()

            # ETF 추적오차
            case "000007":
                df = stock.get_etf_tracking_error(start_date, safe_date, selected_ticker)
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "날짜":
                    df = df.rename(columns={df.columns[0]: "날짜"})

            # ★ ETF 괴리율 (신규)
            case "000008":
                df = stock.get_etf_price_deviation(start_date, safe_date, selected_ticker)
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "날짜":
                    df = df.rename(columns={df.columns[0]: "날짜"})

            # ★ ETF 월별 OHLCV (신규)
            case "000009":
                df = stock.get_etf_ohlcv_by_date(start_date, safe_date, selected_ticker, "m")
                if df is None or df.empty:
                    df = stock.get_etf_ohlcv_by_date(safe_date, safe_date, selected_ticker, "m")
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "날짜":
                    df = df.rename(columns={df.columns[0]: "날짜"})

            # 기본값 → 구성종목
            case _:
                print(f"⚠️ 알 수 없는 함수 코드 '{selected_func}' → 구성종목으로 조회")
                df = stock.get_etf_portfolio_deposit_file(selected_ticker, safe_date)
                if df is None or df.empty:
                    df = stock.get_etf_portfolio_deposit_file(selected_ticker)
                df = df.reset_index()
                if len(df.columns) > 0 and df.columns[0] != "티커":
                    df = df.rename(columns={df.columns[0]: "티커"})
        
        if df is None or df.empty:
            raise ValueError(f"티커 '{selected_ticker}' / 영업일 '{safe_date}' / 함수 '{selected_func}' 데이터 없음")
        
        return df, safe_date
    
    except Exception as e:
        raise ValueError(f"조회 실패 (티커={selected_ticker}, 날짜={safe_date}, 함수={selected_func}): {e}")


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

    # REAL_TICKERS 전체를 etf_list로 사용
    etf_list = [(code, name) for code, name in REAL_TICKERS.items()]

    ticker_name = REAL_TICKERS.get(ticker, stock.get_etf_ticker_name(ticker))
    df, query_date = get_portfolio_df(ticker, query_date, funcNM)
    
    print(f"\n선택된 ETF: {ticker} ({ticker_name})")
    print(f"실제 조회 영업일: {query_date}")
    print(f"=== 데이터 (총 {len(df)}개) ===")
    print(df.head(8))

except Exception as e:
    print(f"❌ 초기 오류: {e}")
    sys.exit(1)


# ==================== Tkinter UI ====================
def create_ui(initial_df: pd.DataFrame, etf_list: list, date_list: list):
    root = tk.Tk()
    root.title(f"{ticker} ({ticker_name}) - ETF 데이터 조회")
    root.geometry("1350x880")

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
    combo_etf = ttk.Combobox(select_frame, values=etf_names, width=80, state="readonly")
    combo_etf.grid(row=0, column=1, padx=5, sticky="w")
    
    for i, (t, n) in enumerate(etf_list):
        if t == ticker:
            combo_etf.current(i)
            break
    else:
        if etf_names:
            combo_etf.current(0)

    # 2. 함수 선택 콤보박스
    ttk.Label(select_frame, text="② 조회 함수:").grid(row=1, column=0, sticky="w", padx=5)
    func_names = [f"{code} | {desc}" for code, desc in REAL_FUNCTION.items()]
    combo_func = ttk.Combobox(select_frame, values=func_names, width=80, state="readonly")
    combo_func.grid(row=1, column=1, padx=5, sticky="w")
    
    for i, code in enumerate(REAL_FUNCTION.keys()):
        if code == funcNM:
            combo_func.current(i)
            break
    else:
        combo_func.current(0)

    # 3. 날짜 콤보박스
    ttk.Label(select_frame, text="③ 날짜 선택:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    combo_date = ttk.Combobox(select_frame, values=date_list, width=15, state="readonly")
    combo_date.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    combo_date.set(query_date)

    applied_label = ttk.Label(select_frame, text=f"→ 적용 영업일: {query_date}", foreground="green")
    applied_label.grid(row=1, column=2, sticky="w", padx=10)

    # ----- Treeview -----
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tree = ttk.Treeview(tree_frame, show="headings", height=26)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def populate_tree(df: pd.DataFrame):
        for item in tree.get_children():
            tree.delete(item)
        
        new_columns = list(df.columns)
        tree["columns"] = new_columns
        
        for col in tree["columns"]:
            tree.heading(col, text="")
            tree.column(col, width=0)
        
        for col in new_columns:
            tree.heading(col, text=col)
            
            if col in ["티커", "종목명", "구성종목명", "날짜"]:
                tree.column(col, width=140, anchor="center")
            elif col in ["계약수", "비중", "NAV", "괴리율"]:
                tree.column(col, width=100, anchor="e")
            elif col in ["시가", "고가", "저가", "종가", "거래량", "거래대금", "기초지수", "금액", "시가총액"]:
                tree.column(col, width=110, anchor="e")
            else:
                tree.column(col, width=120, anchor="e")
        
        for _, row in df.iterrows():
            values = [row[col] for col in new_columns]
            tree.insert("", tk.END, values=values)

    populate_tree(initial_df)

    current = {
        "df": initial_df,
        "ticker": ticker,
        "funcNM": funcNM,
        "name": ticker_name,
        "date": query_date
    }

    def reload_data(new_ticker=None, selected_calendar_date=None, new_func=None):
        if new_ticker is None:
            new_ticker = current["ticker"]
        if selected_calendar_date is None:
            selected_calendar_date = current["date"]
        if new_func is None:
            new_func = current["funcNM"]

        try:
            title_label.config(text=f"ETF: {new_ticker}  ← 조회 중...")
            root.update()

            new_df, safe_date = get_portfolio_df(new_ticker, selected_calendar_date, new_func)
            new_name = REAL_TICKERS.get(new_ticker, stock.get_etf_ticker_name(new_ticker))

            populate_tree(new_df)
            
            title_label.config(text=f"ETF: {new_ticker} ({new_name})")
            date_label.config(text=f"조회 조건 → 선택일 기준 직전 영업일: {safe_date}")
            applied_label.config(text=f"→ 적용 영업일: {safe_date}")
            root.title(f"{new_ticker} ({new_name}) - {safe_date}")

            combo_date.set(safe_date)

            current["df"] = new_df
            current["ticker"] = new_ticker
            current["funcNM"] = new_func
            current["name"] = new_name
            current["date"] = safe_date

            print(f"✅ 조회 완료 → ETF: {new_ticker} | 함수: {new_func} | 영업일: {safe_date} | 항목수: {len(new_df)}")
            print("컬럼:", list(new_df.columns))

        except Exception as e:
            messagebox.showerror("조회 오류", str(e))
            title_label.config(text=f"ETF: {current['ticker']} ({current['name']})")

    def on_etf_select(event=None):
        selected = combo_etf.get()
        if selected:
            new_ticker = selected.split(" | ")[0].strip()
            if new_ticker != current["ticker"]:
                reload_data(new_ticker=new_ticker, selected_calendar_date=combo_date.get())

    def on_func_select(event=None):
        selected = combo_func.get()
        if selected:
            new_func = selected.split(" | ")[0].strip()
            if new_func != current["funcNM"]:
                reload_data(new_func=new_func, selected_calendar_date=combo_date.get())

    def on_date_select(event=None):
        selected_date = combo_date.get()
        if selected_date:
            reload_data(selected_calendar_date=selected_date)

    combo_etf.bind("<<ComboboxSelected>>", on_etf_select)
    combo_func.bind("<<ComboboxSelected>>", on_func_select)
    combo_date.bind("<<ComboboxSelected>>", on_date_select)

    # ----- 하단 버튼 -----
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    def save_to_csv():
        fname = f"{current['ticker']}_{current['funcNM']}_{current['date']}.csv"
        current["df"].to_csv(fname, encoding="utf-8-sig", index=False)
        print(f"✅ 저장 완료: {fname}")
        messagebox.showinfo("저장 완료", f"파일이 저장되었습니다.\n{fname}")

    ttk.Button(btn_frame, text="CSV로 저장", command=save_to_csv).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="닫기", command=root.destroy).pack(side="left", padx=8)

    root.mainloop()


if __name__ == "__main__":
    create_ui(df, etf_list, calendar_dates)