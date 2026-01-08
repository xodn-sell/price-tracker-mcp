"""
가격 추적 메인 로직 - 네이버 쇼핑 전용
"""
import re
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from database import Database
from naver_api import NaverShoppingAPI
from config import Config

logger = logging.getLogger(__name__)

class PriceTracker:
    """가격 추적 메인 클래스"""

    def __init__(self):
        logger.info("🔧 PriceTracker 초기화 중...")
        self.db = Database()
        
        logger.info(f"🔑 API 키로 NaverShoppingAPI 초기화...")
        logger.info(f"   Client ID: {Config.NAVER_CLIENT_ID[:10] if Config.NAVER_CLIENT_ID else 'None'}...")
        logger.info(f"   Client Secret: {Config.NAVER_CLIENT_SECRET[:5] if Config.NAVER_CLIENT_SECRET else 'None'}...")
        
        self.naver = NaverShoppingAPI(
            client_id=Config.NAVER_CLIENT_ID,
            client_secret=Config.NAVER_CLIENT_SECRET
        )
        logger.info("✅ PriceTracker 초기화 완료")

    def search_products(self, keyword: str, count: int = 10) -> List[Dict]:
        """상품 검색"""
        logger.info(f"🔍 네이버 쇼핑에서 '{keyword}' 검색 중...")

        products = []

        try:
            # 네이버 검색 - 올바른 메서드 사용!
            result = self.naver.search_products(
                query=keyword,
                display=count,
                sort="sim"
            )
            
            logger.info(f"📦 API 응답: {len(result.get('items', []))}개 아이템")
            
            if "items" in result:
                for item in result["items"]:
                    products.append({
                        'platform': '네이버쇼핑',
                        'title': self._clean_html(item.get('title', '')),
                        'price': int(item.get('lprice', 0)),
                        'link': item.get('link', ''),
                        'image': item.get('image', ''),
                        'brand': item.get('brand', ''),
                        'maker': item.get('maker', ''),
                        'category': item.get('category1', '')
                    })
            
            logger.info(f"✅ {len(products)}개 상품 검색 완료!")
            
        except Exception as e:
            logger.error(f"❌ 검색 실패: {type(e).__name__}: {e}", exc_info=True)
            
        return products

    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        return re.sub(r'<[^>]+>', '', text)

    # 나머지 메서드들은 그대로...
    def compare_prices(self, keyword: str) -> Dict:
        # ... (기존 코드 유지)
