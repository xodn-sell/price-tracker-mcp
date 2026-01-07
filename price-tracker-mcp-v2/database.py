"""
가격 히스토리 데이터베이스 관리
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class Database:
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
                product_name TEXT NOT NULL,
                platform TEXT NOT NULL,
                price INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 가격 알림 설정 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                target_price INTEGER NOT NULL,
                platform TEXT DEFAULT '네이버쇼핑',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 추적 상품 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracked_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                keyword TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def add_price_record(self, product_name: str, platform: str, price: int):
        """가격 기록 추가"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO price_history (product_name, platform, price)
            VALUES (?, ?, ?)
        ''', (product_name, platform, price))

        conn.commit()
        conn.close()

    def get_price_history(self, keyword: str, start_date: str = None) -> List[Dict]:
        """상품 가격 히스토리 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if start_date:
            cursor.execute('''
                SELECT product_name, platform, price, created_at
                FROM price_history
                WHERE product_name LIKE ?
                AND created_at >= ?
                ORDER BY created_at DESC
            ''', (f'%{keyword}%', start_date))
        else:
            cursor.execute('''
                SELECT product_name, platform, price, created_at
                FROM price_history
                WHERE product_name LIKE ?
                ORDER BY created_at DESC
            ''', (f'%{keyword}%',))

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append({
                "product_name": row[0],
                "platform": row[1],
                "price": row[2],
                "created_at": row[3]
            })

        return history

    def add_price_alert(self, keyword: str, target_price: int, platform: str = '네이버쇼핑') -> int:
        """가격 알림 설정"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO price_alerts (keyword, target_price, platform)
            VALUES (?, ?, ?)
        ''', (keyword, target_price, platform))

        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return alert_id

    def get_price_alerts(self) -> List[Dict]:
        """활성 가격 알림 목록"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, keyword, target_price, platform, created_at
            FROM price_alerts
            ORDER BY created_at DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        alerts = []
        for row in rows:
            alerts.append({
                "id": row[0],
                "keyword": row[1],
                "target_price": row[2],
                "platform": row[3],
                "created_at": row[4]
            })

        return alerts

    def add_tracked_product(self, product_name: str, keyword: str) -> int:
        """추적 상품 추가"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tracked_products (product_name, keyword)
            VALUES (?, ?)
        ''', (product_name, keyword))

        track_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return track_id

    def get_tracked_products(self) -> List[Dict]:
        """추적 중인 상품 목록"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, product_name, keyword, created_at
            FROM tracked_products
            ORDER BY created_at DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        products = []
        for row in rows:
            products.append({
                "id": row[0],
                "product_name": row[1],
                "keyword": row[2],
                "created_at": row[3]
            })

        return products