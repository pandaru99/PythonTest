import requests
import json
from datetime import datetime
from typing import Dict, Optional

class ExchangeRateAPI:
    """
    환율 API와 통신하는 클래스
    """
    
    def __init__(self, api_key: str = None):
        """
        초기화 메서드
        
        Args:
            api_key (str): API 키 (필요한 경우)
        """
        self.api_key = api_key
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        
    def get_exchange_rates(self, base_currency: str = "USD") -> Optional[Dict]:
        """
        특정 기준 통화의 환율을 가져오는 메서드
        
        Args:
            base_currency (str): 기준 통화 (기본값: USD)
            
        Returns:
            dict: 환율 정보 또는 None
        """
        try:
            url = f"{self.base_url}/{base_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 오류: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            return None
        except Exception as e:
            print(f"기타 오류: {e}")
            return None
    
    def convert_currency(self, amount: float, from_currency: str, 
                        to_currency: str, base_currency: str = "USD") -> Optional[float]:
        """
        통화를 변환하는 메서드
        
        Args:
            amount (float): 변환할 금액
            from_currency (str): 원본 통화
            to_currency (str): 목적 통화
            base_currency (str): 기준 통화
            
        Returns:
            float: 변환된 금액 또는 None
        """
        rates_data = self.get_exchange_rates(base_currency)
        
        if not rates_data:
            return None
            
        # 기준 통화의 환율 가져오기
        if from_currency not in rates_data['rates']:
            print(f"지원되지 않는 통화: {from_currency}")
            return None
            
        if to_currency not in rates_data['rates']:
            print(f"지원되지 않는 통화: {to_currency}")
            return None
            
        # 환율 계산
        from_rate = rates_data['rates'][from_currency]
        to_rate = rates_data['rates'][to_currency]
        
        # USD 기준으로 변환 후 목적 통화로 변환
        usd_amount = amount / from_rate
        converted_amount = usd_amount * to_rate
        
        return converted_amount
    
    def get_supported_currencies(self) -> Optional[list]:
        """
        지원되는 통화 목록을 가져오는 메서드
        
        Returns:
            list: 지원되는 통화 목록 또는 None
        """
        rates_data = self.get_exchange_rates("USD")
        
        if not rates_data:
            return None
            
        currencies = list(rates_data['rates'].keys())
        currencies.insert(0, "USD")  # USD를 맨 앞으로 추가
        
        return currencies

def main():
    """
    메인 함수 - 예제 실행
    """
    print("환율 변환기")
    print("=" * 30)
    
    # 환율 API 인스턴스 생성
    exchange_api = ExchangeRateAPI()
    
    # 지원되는 통화 목록 출력
    currencies = exchange_api.get_supported_currencies()
    if currencies:
        print("지원되는 통화:")
        for i, currency in enumerate(currencies[:10], 1):  # 처음 10개만 표시
            print(f"  {i}. {currency}")
        if len(currencies) > 10:
            print(f"  ... 그리고 {len(currencies) - 10}개 더")
    
    print("\n환율 변환 예제:")
    
    # 예제 1: USD에서 KRW로 변환
    result = exchange_api.convert_currency(100, "USD", "KRW")
    if result:
        print(f"100 USD = {result:.2f} KRW")
    
    # 예제 2: EUR에서 JPY로 변환
    result = exchange_api.convert_currency(50, "EUR", "JPY")
    if result:
        print(f"50 EUR = {result:.2f} JPY")
    
    # 예제 3: JPY에서 USD로 변환
    result = exchange_api.convert_currency(10000, "JPY", "USD")
    if result:
        print(f"10000 JPY = {result:.2f} USD")

if __name__ == "__main__":
    main()