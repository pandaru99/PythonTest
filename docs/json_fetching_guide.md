# Grok + VSCode + Python 완전 종합 가이드 (v2)

**작성일**: 2026년 7월 8일  
**대상**: 초보자 ~ 중급자  
**목적**: VSCode에서 Grok을 사용하면서 Python 개발 환경을 빠르고 안정적으로 구축하기

---

## 목차
1. VSCode에서 Grok 연결 방법 (상세)
2. X Premium / SuperGrok Grok 사용량 제한
3. Python 설치 및 VSCode 설정
4. pip 설치 및 최적화 설정
5. 네이버 증권 외국인·기관 매매동향 데이터 수집
6. 한 번에 실행하는 전체 설치 명령어
7. 자주 발생하는 문제 해결 (Troubleshooting)
8. 추가 추천 확장 프로그램

---

## 1. VSCode에서 Grok 연결 방법 (상세)

### 1.1 xAI API Key 발급
1. [https://console.x.ai/](https://console.x.ai/) 접속
2. X 계정으로 로그인
3. **API Keys** → **Create API Key** 클릭
4. 키 이름 입력 후 생성 → 키 복사 (한 번만 표시됨)

### 1.2 추천 Grok 확장 프로그램

| 확장 프로그램                  | 난이도 | 주요 장점                          | 추천 대상             |
|-------------------------------|--------|------------------------------------|-----------------------|
| **Simply Grok for VSCode**    | ★☆☆    | 가장 간단, 코드베이스 질문 특화    | 초보자                |
| **Grok AI / xAI for VS Code** | ★★☆    | 사이드바 채팅 + 인라인 완성 + 코드 액션 | 중급자 (가장 균형)    |
| **Cline**                     | ★★★    | 가장 강력한 Agentic 코딩 (파일 자동 수정) | 고급 사용자           |
| **CodeGPT**                   | ★★☆    | 다중 AI 지원 (Grok 포함)           | 여러 AI 같이 쓰는 사람 |

### 1.3 설치 및 연결 단계
1. VSCode에서 **Extensions** (`Ctrl + Shift + X`) 열기
2. 위 확장 중 하나 검색 → **Install**
3. `Ctrl + Shift + P` → **`Grok: Set API Key`** 또는 **`Set API Key`** 검색
4. 복사한 API 키 붙여넣기

**주요 단축키** (Grok AI 확장 기준)
- Grok 채팅 열기: `Ctrl + Shift + G`
- 선택 코드 설명: `Ctrl + Shift + E`
- 버그 수정: `Ctrl + Shift + F`

---

## 2. X Premium / SuperGrok Grok 사용량 제한

| 구독 Tier       | 가격          | Grok 4 제한 (대략)       | SuperGrok 기능 | 추천 상황                     |
|-----------------|---------------|---------------------------|----------------|-------------------------------|
| Free            | 무료          | 10회 / 2시간             | 제한적         | 가벼운 사용                   |
| X Premium       | $8/mo         | 40~50회 / 2시간          | 일부 제한      | 일반적인 채팅                 |
| X Premium+      | $40/mo        | 80~100회+ / 2시간        | 대부분 지원    | 자주 사용하는 사용자          |
| **SuperGrok**   | **$30/mo**    | **매우 높음**            | 풀 지원        | **VSCode 코딩 작업 추천**     |

> **VSCode에서 자주 사용할 계획이라면 SuperGrok 구독을 강력 추천합니다.**

사용량 확인 방법: Grok 채팅 화면 → **Usage** 또는 **설정 → Usage**

---

## 3. Python 설치 및 VSCode 설정

### 3.1 Python 설치
1. [https://www.python.org/downloads/](https://www.python.org/downloads/) 접속
2. **Python 3.12.x** (또는 최신 안정 버전) 다운로드
3. **설치 시 반드시 체크**:
   - ✅ **Add python.exe to PATH**
4. 설치 완료 후 확인:
   ```bash
   python --version
   pip --version


---

## 3.2 VSCode Python 확장 설치

### 설치 방법
1. VSCode를 열고 왼쪽 사이드바에서 **Extensions** 아이콘 클릭 (`Ctrl + Shift + X`)
2. 검색창에 **`Python`** 입력
3. **Microsoft**에서 만든 **Python** 확장을 찾아 **Install** 클릭

### 함께 설치하면 좋은 확장 프로그램

| 확장 이름              | 설치 이유                              | 추천도 |
|------------------------|----------------------------------------|--------|
| **Python** (Microsoft) | 기본 Python 지원 (필수)                | ★★★★★ |
| **Pylance**            | 강력한 자동완성, 타입 체크, 오류 표시  | ★★★★★ |
| **Jupyter**            | Jupyter Notebook 지원                  | ★★★★☆ |
| **Python Environment Manager** | 가상환경 관리 편의성               | ★★★★☆ |
| **Black Formatter**    | 코드 자동 포맷팅 (저장 시 정리)        | ★★★★☆ |

> **Pylance**는 반드시 설치하는 것을 강력 추천합니다.

---

## 3.3 Python Interpreter 선택

### 방법
1. `Ctrl + Shift + P` 키를 눌러 Command Palette 열기
2. **`Python: Select Interpreter`** 검색 후 선택
3. 설치한 Python 버전이 목록에 나타나면 클릭

**정상적으로 선택되었는지 확인 방법**:
- VSCode 하단 상태바에 **Python 3.12.x** (또는 설치한 버전)이 표시되어야 합니다.

---

## 3.4 VSCode Python 관련 추천 설정

`Ctrl + ,` 키를 눌러 설정 열기 후 아래 항목을 검색하여 설정하세요.

### 필수 추천 설정

| 설정 이름                              | 추천 값          | 설명 |
|----------------------------------------|------------------|------|
| `Editor: Format On Save`               | 체크             | 저장할 때 자동으로 코드 정리 |
| `Python > Linting: Enabled`            | 체크             | 코드 오류 실시간 검사 |
| `Python > Formatting: Provider`        | `black`          | 가장 인기 있는 포맷터 |
| `Python > Analysis: Type Checking Mode`| `basic` 또는 `strict` | 타입 검사 강도 |
| `Python > Terminal: Activate Environment` | 체크          | 터미널에서 자동으로 가상환경 활성화 |

---

## 4. pip 설치 및 최적화 설정

### 4.1 기본 pip 명령어 정리

```bash
# 패키지 설치
pip install 패키지이름

# 여러 개 한 번에 설치
pip install pandas numpy matplotlib requests pykrx

# 업그레이드
pip install --upgrade pip
pip install --upgrade pykrx

# 설치된 패키지 확인
pip list

# requirements.txt 생성
pip freeze > requirements.txt

# requirements.txt로 설치
pip install -r requirements.txt


## 4.2 한국에서 pip 빠르게 사용하는 설정 (필수)

한국에서 pip이 느릴 때 **카카오 미러**를 적용하는 것이 가장 효과적입니다.

### 미러 설정 명령어

```bash
# 1. 카카오 미러 적용
pip config set global.index-url https://mirror.kakao.com/pypi/simple

# 2. 신뢰할 수 있는 호스트 등록
pip config set global.trusted-host mirror.kakao.com

# 3. 타임아웃 시간 증가 (다운로드가 자주 끊길 때)
pip config set global.timeout 120

설정 확인 방법bash

pip config list

정상적으로 적용되었을 때 출력 예시:

global.index-url='https://mirror.kakao.com/pypi/simple'
global.trusted-host='mirror.kakao.com'
global.timeout='120'

설정 초기화 방법bash

# 특정 설정만 제거
pip config unset global.index-url
pip config unset global.trusted-host

# 모든 global 설정 초기화
pip config unset --global index-url
pip config unset --global trusted-host
pip config unset --global timeout

4.3 가상환경 사용법 (강력 추천)가상환경 생성 및 활성화bash

# 가상환경 생성
python -m venv venv

# Windows에서 활성화
venv\Scripts\activate

# Mac / Linux에서 활성화
source venv/bin/activate

활성화 확인 방법:터미널 프롬프트 앞에 (venv)가 붙어 있어야 합니다.

가상환경에서 작업하기bash

# 가상환경 활성화 후 패키지 설치
pip install pykrx pandas requests matplotlib openpyxl

# 현재 설치된 패키지 확인
pip list

# 작업 완료 후 가상환경 종료
deactivate

VSCode 팁: 가상환경을 사용 중이라면 하단 상태바에서 Interpreter를 venv로 선택하세요.


5. 네이버 증권 외국인·기관 매매동향 수집5.1 pykrx 추천 방법 (가장 안정적)python

from pykrx import stock
import pandas as pd
from datetime import datetime

# ================== 설정 ==================
ticker = "005930"                    # 종목코드
start_date = "20250101"              # 시작일 (YYYYMMDD 형식)
end_date = datetime.now().strftime("%Y%m%d")

# ================== 데이터 조회 ==================
df = stock.get_market_trading_volume_by_investor(
    fromdate=start_date,
    todate=end_date,
    ticker=ticker
)

# 최근 데이터 확인
print(df.tail(10))

# CSV로 저장
filename = f"{ticker}_매매동향_{start_date}_to_{end_date}.csv"
df.to_csv(filename, encoding="utf-8-sig")
print(f"\n✅ 저장 완료: {filename}")

5.2 pandas + requests 방법python

import pandas as pd
import requests

def get_investor_trading(ticker: str):
    url = f"https://finance.naver.com/item/frgn.naver?code={ticker}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    tables = pd.read_html(response.text)
    
    df = tables[2]  # 투자자별 매매동향 테이블
    
    # 컬럼명 정리
    df.columns = ['날짜', '종가', '전일비', '등락률', '외국인', '기관', '개인', '외국인보유주', '외국인비율']
    
    return df

# 사용 예시
df = get_investor_trading("005930")
print(df.head(10))

6. 전체 한 번에 설치 명령어아래 내용을 터미널에 한 번에 복사해서 붙여넣기만 하면 됩니다.bash

# ==================== 1. pip 미러 설정 ====================
pip config set global.index-url https://mirror.kakao.com/pypi/simple
pip config set global.trusted-host mirror.kakao.com
pip config set global.timeout 120

echo "=== pip 설정 확인 ==="
pip config list

# ==================== 2. 주요 패키지 설치 ====================
pip install pykrx pandas requests matplotlib openpyxl jupyter

# ==================== 3. 설치 결과 확인 ====================
echo ""
echo "=== Python 버전 ==="
python --version

echo ""
echo "=== pip 버전 ==="
pip --version

echo ""
echo "=== 설치된 주요 패키지 ==="
pip list | grep -E 'pykrx|pandas|requests|matplotlib|openpyxl|jupyter'

실행 후 기대되는 결과pip 미러가 카카오로 변경됨
주요 패키지들이 정상 설치됨
Python과 pip 버전이 정상 출력됨
