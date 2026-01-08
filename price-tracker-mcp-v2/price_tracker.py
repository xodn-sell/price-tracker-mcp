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

    def compare_prices(self, keyword: str) -> Dict:
        """
        가격 비교 및 최저가 찾기

        Args:
            keyword: 검색 키워드

        Returns:
            비교 결과 (최저가, 최고가, 평균가, 상품 목록)
        """
        logger.info(f"💰 '{keyword}' 가격 비교 중...")
        
        products = self.search_products(keyword, count=20)

        if not products:
            logger.warning(f"⚠️ '{keyword}' 상품을 찾을 수 없습니다")
            return {
                'keyword': keyword,
                'total_count': 0,
                'lowest_price': None,
                'highest_price': None,
                'average_price': None,
                'products': []
            }

        prices = [p['price'] for p in products]
        lowest_price = min(prices)
        highest_price = max(prices)
        average_price = sum(prices) // len(prices)

        # 가격 정렬 (낮은 순)
        sorted_products = sorted(products, key=lambda x: x['price'])

        logger.info(f"✅ 가격 비교 완료: 최저가 {lowest_price:,}원")

        return {
            'keyword': keyword,
            'total_count': len(products),
            'lowest_price': lowest_price,
            'highest_price': highest_price,
            'average_price': average_price,
            'products': sorted_products[:10]  # 상위 10개만
        }

    def set_price_alert(self, keyword: str, target_price: int) -> Dict:
        """
        가격 알림 설정

        Args:
            keyword: 상품 키워드
            target_price: 목표 가격

        Returns:
            알림 설정 결과
        """
        logger.info(f"🔔 가격 알림 설정: {keyword} -> {target_price:,}원")
        
        alert_id = self.db.add_price_alert(
            keyword=keyword,
            target_price=target_price,
            platform='네이버쇼핑'
        )

        return {
            'alert_id': alert_id,
            'keyword': keyword,
            'target_price': target_price,
            'platform': '네이버쇼핑',
            'created_at': datetime.now().isoformat(),
            'message': f"'{keyword}'의 목표가 {target_price:,}원 알림이 설정되었습니다."
        }

    def get_price_history(self, keyword: str, days: int = 30) -> List[Dict]:
        """
        가격 히스토리 조회

        Args:
            keyword: 상품 키워드
            days: 조회 기간 (일)

        Returns:
            가격 히스토리 목록
        """
        logger.info(f"📊 '{keyword}' 가격 히스토리 조회 ({days}일)")
        
        start_date = datetime.now() - timedelta(days=days)
        history = self.db.get_price_history(
            keyword=keyword,
            start_date=start_date.isoformat()
        )

        return history

    def track_product(self, keyword: str) -> Dict:
        """
        상품 추적 시작

        Args:
            keyword: 상품 키워드

        Returns:
            추적 시작 결과
        """
        logger.info(f"🎯 '{keyword}' 추적 시작...")
        
        # 현재 가격 검색
        products = self.search_products(keyword, count=1)

        if not products:
            return {
                'success': False,
                'message': f"'{keyword}' 상품을 찾을 수 없습니다."
            }

        product = products[0]

        # 추적 상품 등록
        track_id = self.db.add_tracked_product(
            product_name=product['title'],
            keyword=keyword
        )

        # 현재 가격 저장
        self.db.add_price_record(
            product_name=product['title'],
            platform=product['platform'],
            price=product['price']
        )

        logger.info(f"✅ 추적 시작 완료: {product['title']}")

        return {
            'success': True,
            'track_id': track_id,
            'product': product,
            'message': f"'{keyword}' 상품 추적을 시작했습니다."
        }

    def list_tracked_products(self) -> List[Dict]:
        """
        추적 중인 상품 목록 조회

        Returns:
            추적 중인 상품 목록
        """
        logger.info("📋 추적 상품 목록 조회")
        return self.db.get_tracked_products()

    def get_best_deals(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        베스트 딜 추천

        Args:
            category: 카테고리 (선택)
            limit: 결과 개수

        Returns:
            베스트 딜 목록
        """
        logger.info(f"🏆 베스트 딜 조회 (limit: {limit})")
        
        # 인기 키워드 목록 (예시)
        keywords = [
            "노트북", "무선이어폰", "스마트워치", "태블릿",
            "키보드", "마우스", "모니터", "웹캠"
        ]

        best_deals = []

        for keyword in keywords[:limit]:
            try:
                comparison = self.compare_prices(keyword)
                if comparison['total_count'] > 0:
                    best_deals.append({
                        'keyword': keyword,
                        'lowest_price': comparison['lowest_price'],
                        'average_price': comparison['average_price'],
                        'product_count': comparison['total_count'],
                        'best_product': comparison['products'][0] if comparison['products'] else None
                    })
            except Exception as e:
                logger.warning(f"⚠️ '{keyword}' 검색 실패: {e}")
                continue

        # 가격 대비 가치 순으로 정렬
        best_deals.sort(key=lambda x: x['lowest_price'] / max(x['average_price'], 1))

        logger.info(f"✅ {len(best_deals)}개 베스트 딜 발견")
        return best_deals[:limit]

    def check_price_alerts(self) -> List[Dict]:
        """
        가격 알림 확인

        Returns:
            알림이 트리거된 항목 목록
        """
        logger.info("🔔 가격 알림 확인 중...")
        
        alerts = self.db.get_price_alerts()
        triggered_alerts = []

        for alert in alerts:
            keyword = alert['keyword']
            target_price = alert['target_price']

            try:
                products = self.search_products(keyword, count=1)
                if products:
                    current_price = products[0]['price']

                    if current_price <= target_price:
                        triggered_alerts.append({
                            'alert_id': alert['id'],
                            'keyword': keyword,
                            'target_price': target_price,
                            'current_price': current_price,
                            'product': products[0],
                            'message': f"🎉 '{keyword}'이(가) 목표가 {target_price:,}원 이하입니다! (현재가: {current_price:,}원)"
                        })
            except Exception as e:
                logger.warning(f"⚠️ '{keyword}' 알림 확인 실패: {e}")
                continue

        logger.info(f"✅ {len(triggered_alerts)}개 알림 트리거됨")
        return triggered_alerts
