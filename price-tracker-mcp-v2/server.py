"""
Price Tracker MCP Server - 네이버 쇼핑 전용
"""
from fastmcp import FastMCP
from price_tracker import PriceTracker
from config import Config

# MCP 서버 초기화
mcp = FastMCP("Price Tracker - 네이버 쇼핑")

# PriceTracker 인스턴스
tracker = PriceTracker()


@mcp.tool()
def search_product(keyword: str, count: int = 10) -> dict:
    """
    네이버 쇼핑에서 상품 검색
    
    Args:
        keyword: 검색할 상품 키워드 (예: "무선이어폰", "노트북")
        count: 검색 결과 개수 (기본 10개, 최대 100개)
    
    Returns:
        상품 목록 및 검색 결과
    
    Example:
        search_product("에어팟 프로")
        search_product("삼성 갤럭시북", count=20)
    """
    try:
        products = tracker.search_products(keyword, count)
        
        return {
            "success": True,
            "keyword": keyword,
            "total_count": len(products),
            "products": products,
            "message": f"'{keyword}' 검색 완료: {len(products)}개 상품 발견"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"검색 실패: {str(e)}"
        }


@mcp.tool()
def compare_prices(keyword: str) -> dict:
    """
    상품 가격 비교 및 최저가 찾기
    
    Args:
        keyword: 검색할 상품 키워드
    
    Returns:
        최저가, 최고가, 평균가 및 상위 10개 상품 정보
    
    Example:
        compare_prices("아이폰 15")
        compare_prices("LG 그램")
    """
    try:
        result = tracker.compare_prices(keyword)
        
        if result['total_count'] == 0:
            return {
                "success": False,
                "message": f"'{keyword}' 상품을 찾을 수 없습니다."
            }
        
        return {
            "success": True,
            "keyword": result['keyword'],
            "statistics": {
                "total_count": result['total_count'],
                "lowest_price": result['lowest_price'],
                "highest_price": result['highest_price'],
                "average_price": result['average_price']
            },
            "top_products": result['products'],
            "message": f"최저가: {result['lowest_price']:,}원 | 평균가: {result['average_price']:,}원"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"가격 비교 실패: {str(e)}"
        }


@mcp.tool()
def set_price_alert(keyword: str, target_price: int) -> dict:
    """
    상품 가격 알림 설정
    
    Args:
        keyword: 상품 키워드
        target_price: 목표 가격 (원)
    
    Returns:
        알림 설정 결과
    
    Example:
        set_price_alert("갤럭시 버즈", 100000)
        set_price_alert("맥북", 1500000)
    """
    try:
        result = tracker.set_price_alert(keyword, target_price)
        
        return {
            "success": True,
            "alert_id": result['alert_id'],
            "keyword": result['keyword'],
            "target_price": result['target_price'],
            "message": result['message']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"알림 설정 실패: {str(e)}"
        }


@mcp.tool()
def get_price_history(keyword: str, days: int = 30) -> dict:
    """
    상품 가격 히스토리 조회
    
    Args:
        keyword: 상품 키워드
        days: 조회 기간 (일, 기본 30일)
    
    Returns:
        가격 변동 히스토리
    
    Example:
        get_price_history("아이패드")
        get_price_history("닌텐도 스위치", days=90)
    """
    try:
        history = tracker.get_price_history(keyword, days)
        
        if not history:
            return {
                "success": False,
                "message": f"'{keyword}'의 가격 히스토리가 없습니다."
            }
        
        return {
            "success": True,
            "keyword": keyword,
            "period_days": days,
            "total_records": len(history),
            "history": history,
            "message": f"{days}일간 {len(history)}개 가격 기록 조회"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"히스토리 조회 실패: {str(e)}"
        }


@mcp.tool()
def track_product(keyword: str) -> dict:
    """
    상품 추적 시작
    
    Args:
        keyword: 추적할 상품 키워드
    
    Returns:
        추적 시작 결과
    
    Example:
        track_product("플레이스테이션 5")
        track_product("다이슨 청소기")
    """
    try:
        result = tracker.track_product(keyword)
        
        return {
            "success": result['success'],
            "track_id": result.get('track_id'),
            "product": result.get('product'),
            "message": result['message']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"추적 시작 실패: {str(e)}"
        }


@mcp.tool()
def list_tracked_products() -> dict:
    """
    추적 중인 상품 목록 조회
    
    Returns:
        추적 중인 모든 상품 목록
    
    Example:
        list_tracked_products()
    """
    try:
        products = tracker.list_tracked_products()
        
        return {
            "success": True,
            "total_count": len(products),
            "tracked_products": products,
            "message": f"{len(products)}개 상품 추적 중"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"목록 조회 실패: {str(e)}"
        }


@mcp.tool()
def get_best_deals(limit: int = 10) -> dict:
    """
    베스트 딜 추천 (가격 대비 가치가 높은 상품)
    
    Args:
        limit: 추천 상품 개수 (기본 10개)
    
    Returns:
        베스트 딜 상품 목록
    
    Example:
        get_best_deals()
        get_best_deals(limit=5)
    """
    try:
        deals = tracker.get_best_deals(limit=limit)
        
        return {
            "success": True,
            "total_count": len(deals),
            "best_deals": deals,
            "message": f"{len(deals)}개 베스트 딜 추천"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"베스트 딜 조회 실패: {str(e)}"
        }

if __name__ == "__main__":
    # 설정 검증
    if Config.validate():
        print("✅ API 설정 완료")
        print(f"📊 설정 정보: {Config.get_api_info()}")
        print("\n🚀 [카카오 연동용] MCP 웹 서버 시작 중...")
        print("⚠️ 실행 후 'Uvicorn running on http://...' 메시지가 나오면 성공입니다!")
        
        # mcp.run()을 'sse' 모드로 실행해야 웹으로 연결됩니다.
        # 기본 포트는 8000번입니다.
        try:
            # 최신 FastMCP 방식
            mcp.run(transport='sse')
        except TypeError:
            # 만약 에러가 나면 수동으로 uvicorn 실행 (비상용)
            import uvicorn
            print("🔧 호환 모드로 전환합니다...")
            mcp.run() 
    else:
        print("\n❌ API 설정을 완료한 후 서버를 시작하세요.")
        print("💡 .env 파일을 확인하고 필수 API 키를 입력하세요.")
