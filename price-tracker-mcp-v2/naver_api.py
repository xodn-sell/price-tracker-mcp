"""
네이버 쇼핑 API 클라이언트
"""
import requests
from typing import List, Dict, Optional


class NaverShoppingAPI:
    """네이버 쇼핑 검색 API 클라이언트"""
    
    BASE_URL = "https://openapi.naver.com/v1/search/shop.json"
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Args:
            client_id: 네이버 API Client ID
            client_secret: 네이버 API Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
    
    def search_products(
        self, 
        query: str, 
        display: int = 10,
        start: int = 1,
        sort: str = "sim"  # sim(유사도), date(날짜), asc(가격낮은순), dsc(가격높은순)
    ) -> Dict:
        """
        상품 검색
        
        Args:
            query: 검색어
            display: 검색 결과 출력 건수 (기본 10, 최대 100)
            start: 검색 시작 위치 (기본 1, 최대 1000)
            sort: 정렬 옵션
        
        Returns:
            검색 결과 딕셔너리
        """
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }
        
        try:
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "items": []}
    
    def get_lowest_prices(self, query: str, count: int = 3) -> List[Dict]:
        """
        최저가 상품 검색
        
        Args:
            query: 검색어
            count: 반환할 상품 개수
        
        Returns:
            최저가순 상품 리스트
        """
        result = self.search_products(query, display=count, sort="asc")
        
        if "items" not in result:
            return []
        
        products = []
        for item in result["items"]:
            products.append({
                "title": self._clean_html(item.get("title", "")),
                "price": int(item.get("lprice", 0)),
                "link": item.get("link", ""),
                "image": item.get("image", ""),
                "mall_name": item.get("mallName", ""),
                "product_id": item.get("productId", ""),
                "brand": item.get("brand", ""),
                "maker": item.get("maker", ""),
                "category": item.get("category1", ""),
                "platform": "네이버쇼핑"
            })
        
        return products
    
    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        import re
        return re.sub(r'<[^>]+>', '', text)


# 테스트 코드
if __name__ == "__main__":
    # 테스트용 - 실제 사용 시 환경변수에서 가져오기
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    
    api = NaverShoppingAPI(client_id, client_secret)
    results = api.get_lowest_prices("아이패드", count=3)
    
    for idx, product in enumerate(results, 1):
        print(f"{idx}. {product['title']}")
        print(f"   가격: {product['price']:,}원")
        print(f"   판매처: {product['mall_name']}")
        print()
