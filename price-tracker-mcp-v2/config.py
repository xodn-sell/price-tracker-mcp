"""
설정 관리 - 네이버 쇼핑 전용
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """환경 설정"""
    
    # 네이버 쇼핑 API
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")
    
    # 데이터베이스
    DATABASE_PATH = os.getenv("DATABASE_PATH", "price_history.db")
    
    # 기본 설정
    DEFAULT_SEARCH_COUNT = 10  # 검색 결과 개수
    DEFAULT_HISTORY_DAYS = 30  # 히스토리 조회 기간
    
    @classmethod
    def validate(cls) -> bool:
        """
        API 키 유효성 검사
        
        Returns:
            모든 필수 키가 설정되었으면 True
        """
        if not cls.NAVER_CLIENT_ID or not cls.NAVER_CLIENT_SECRET:
            print("❌ 네이버 API 키가 설정되지 않았습니다!")
            print("\n📝 .env 파일에 다음 항목을 설정하세요:")
            print("NAVER_CLIENT_ID=your_client_id")
            print("NAVER_CLIENT_SECRET=your_client_secret")
            return False
        
        return True
    
    @classmethod
    def get_api_info(cls) -> dict:
        """API 키 정보 반환 (마스킹)"""
        def mask_key(key: str) -> str:
            if not key or len(key) < 8:
                return "미설정"
            return f"{key[:4]}...{key[-4:]}"
        
        return {
            "naver_client_id": mask_key(cls.NAVER_CLIENT_ID),
            "naver_client_secret": mask_key(cls.NAVER_CLIENT_SECRET),
            "database_path": cls.DATABASE_PATH
        }
