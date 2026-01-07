"""
가격 히스토리 데이터베이스 관리
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


class PriceDatabase:
    """가격 추적 데이터베이스"""
    
    def __init__(self, db_path: str = "price_history.db"):
        """
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화 및 테이블 생성"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 가격 히스토리 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_title TEXT NOT NULL,
                platform TEXT NOT NULL,
                price INTEGER NOT NULL,
                product_link TEXT,
                mall_name TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 가격 알림 설정 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_keyword TEXT NOT NULL,
                target_price INTEGER NOT NULL,
                platform TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 추적 상품 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracked_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_title TEXT NOT NULL,
                product_keyword TEXT NOT NULL,
                platform TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_price_record(
        self, 
        product_title: str, 
        platform: str, 
        price: int,
        product_link: str = "",
        mall_name: str = ""
    ):
        """
        가격 기록 추가
        
        Args:
            product_title: 상품명
            platform: 플랫폼 (네이버쇼핑, 11번가)
            price: 가격
            product_link: 상품 링크
            mall_name: 판매처명
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO price_history 
            (product_title, platform, price, product_link, mall_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_title, platform, price, product_link, mall_name))
        
        conn.commit()
        conn.close()
    
    def get_price_history(
        self, 
        product_title: str, 
        days: int = 30
    ) -> List[Dict]:
        """
        상품 가격 히스토리 조회
        
        Args:
            product_title: 상품명
            days: 조회할 일수
        
        Returns:
            가격 히스토리 리스트
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT platform, price, recorded_at, mall_name
            FROM price_history
            WHERE product_title LIKE ?
            AND recorded_at >= datetime('now', '-' || ? || ' days')
            ORDER BY recorded_at DESC
        ''', (f'%{product_title}%', days))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "platform": row[0],
                "price": row[1],
                "recorded_at": row[2],
                "mall_name": row[3]
            })
        
        return history
    
    def add_price_alert(
        self, 
        product_keyword: str, 
        target_price: int,
        platform: str = "전체"
    ) -> int:
        """
        가격 알림 설정
        
        Args:
            product_keyword: 검색 키워드
            target_price: 목표 가격
            platform: 플랫폼
        
        Returns:
            생성된 알림 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO price_alerts 
            (product_keyword, target_price, platform)
            VALUES (?, ?, ?)
        ''', (product_keyword, target_price, platform))
        
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return alert_id
    
    def get_active_alerts(self) -> List[Dict]:
        """활성화된 가격 알림 목록"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, product_keyword, target_price, platform, created_at
            FROM price_alerts
            WHERE is_active = 1
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        alerts = []
        for row in rows:
            alerts.append({
                "id": row[0],
                "product_keyword": row[1],
                "target_price": row[2],
                "platform": row[3],
                "created_at": row[4]
            })
        
        return alerts
    
    def add_tracked_product(
        self, 
        product_title: str, 
        product_keyword: str,
        platform: str = "전체"
    ) -> int:
        """
        추적 상품 추가
        
        Args:
            product_title: 상품명
            product_keyword: 검색 키워드
            platform: 플랫폼
        
        Returns:
            추적 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tracked_products 
            (product_title, product_keyword, platform)
            VALUES (?, ?, ?)
        ''', (product_title, product_keyword, platform))
        
        track_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return track_id
    
    def get_tracked_products(self) -> List[Dict]:
        """추적 중인 상품 목록"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, product_title, product_keyword, platform, created_at
            FROM tracked_products
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            products.append({
                "id": row[0],
                "product_title": row[1],
                "product_keyword": row[2],
                "platform": row[3],
                "created_at": row[4]
            })
        
        return products
