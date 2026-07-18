# JSON 파일 받아오기 가이드

## 개요
이 문서는 Python을 사용하여 JSON 파일을 받아오는 방법에 대해 설명합니다.

## 필요한 라이브러리
- `requests`: HTTP 요청을 위해 필요합니다.
- `json`: JSON 데이터를 파싱하기 위해 필요합니다.

## 코드 예제

```python
import json
import requests

def fetch_json_data(url):
    """
    JSON 파일을 받아오는 함수
    
    Args:
        url (str): JSON 파일이 있는 URL
        
    Returns:
        dict: 파싱된 JSON 데이터
    """
    try:
        # HTTP GET 요청
        response = requests.get(url)
        response.raise_for_status()  # 상태 코드 확인
        
        # JSON 데이터 파싱
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return None

# 예시 사용법
if __name__ == "__main__":
    # JSON 파일 URL
    json_url = "https://jsonplaceholder.typicode.com/posts/1"
    
    # JSON 데이터 받아오기
    result = fetch_json_data(json_url)
    
    if result:
        print("받은 JSON 데이터:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("데이터를 받는 데 실패했습니다.")
```

## 설치 방법

### pip를 사용한 설치
```bash
pip install requests
```

## 주요 기능

1. **HTTP GET 요청**: 지정된 URL에서 데이터를 받아옵니다.
2. **에러 처리**: HTTP 오류나 JSON 파싱 오류에 대한 예외 처리가 포함되어 있습니다.
3. **JSON 파싱**: 받은 데이터를 파이썬 딕셔너리로 변환합니다.

## 사용 방법

1. `fetch_json_data()` 함수에 JSON 파일이 있는 URL을 전달합니다.
2. 성공적으로 데이터를 받았다면, 반환된 딕셔너리를 사용하여 데이터를 처리합니다.
3. 실패 시 None을 반환하고 오류 메시지를 출력합니다.

## 참고 사항

- HTTPS와 HTTP 모두 지원됩니다.
- JSON 파일이 아닌 일반 텍스트나 다른 형식의 파일은 파싱에 실패할 수 있습니다.
- 네트워크 연결이 필요하므로 인터넷에 연결되어 있어야 합니다.


mkdir -p docs && touch docs/json_fetching_guide.md