# 🛒 Price Tracker MCP - 네이버 쇼핑

네이버 쇼핑에서 실시간 가격을 비교하고, 가격 알림을 설정하며, 최저가를 추천하는 MCP 서버

**MCP Player 10 출품작**

---

## ✨ 주요 기능

### 🔍 **상품 검색**
- 네이버 쇼핑 실시간 검색
- 최대 100개 상품 조회
- 상세 정보 (가격, 브랜드, 이미지 등)

### 💰 **가격 비교**
- 최저가 / 최고가 / 평균가 자동 계산
- 가격 순 정렬
- 상위 10개 상품 추천

### 🔔 **가격 알림**
- 목표 가격 설정
- 자동 알림 확인
- 알림 히스토리 관리

### 📊 **가격 히스토리**
- 30일간 가격 변동 추적
- 가격 트렌드 분석
- SQLite 데이터베이스 저장

### 🎯 **상품 추적**
- 관심 상품 등록
- 자동 가격 업데이트
- 추적 목록 관리

### 🏆 **베스트 딜**
- 가격 대비 가치 분석
- 인기 상품 추천
- 실시간 최저가 발견

---

## 🚀 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/xodn-sell/price-tracker-mcp.git
cd price-tracker-mcp
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집
nano .env
```

**.env 파일 예시:**
```env
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
```

### 4. 네이버 API 키 발급

1. [네이버 개발자 센터](https://developers.naver.com/apps/#/register) 접속
2. "애플리케이션 등록" 클릭
3. 정보 입력:
   - 애플리케이션 이름: Price Tracker MCP
   - 사용 API: **검색** (필수!)
   - 웹 서비스 URL: `http://localhost`
4. Client ID와 Client Secret 복사
5. `.env` 파일에 붙여넣기

---

## 💻 사용 방법

### 서버 실행
```bash
python server.py
```

### MCP 도구 사용

#### 1️⃣ 상품 검색
```python
search_product("무선이어폰")
search_product("노트북", count=20)
```

#### 2️⃣ 가격 비교
```python
compare_prices("아이폰 15")
```

**결과 예시:**
```
✅ 성공!
최저가: 1,200,000원
최고가: 1,450,000원
평균가: 1,320,000원
총 20개 상품
```

#### 3️⃣ 가격 알림 설정
```python
set_price_alert("갤럭시 버즈", 100000)
```

#### 4️⃣ 가격 히스토리
```python
get_price_history("맥북", days=30)
```

#### 5️⃣ 상품 추적
```python
track_product("플레이스테이션 5")
list_tracked_products()
```

#### 6️⃣ 베스트 딜
```python
get_best_deals(limit=10)
```

---

## 🏗️ 프로젝트 구조

```
price-tracker-mcp/
├── server.py              # MCP 서버 (7개 도구)
├── price_tracker.py       # 가격 추적 로직
├── naver_api.py          # 네이버 쇼핑 API 클라이언트
├── database.py           # SQLite 데이터베이스
├── config.py             # 환경 변수 관리
├── requirements.txt      # 의존성 목록
├── .env.example          # 환경 변수 템플릿
├── .gitignore           # Git 제외 파일
└── README.md            # 프로젝트 문서
```

---

## 🗄️ 데이터베이스 스키마

### **price_history** (가격 기록)
```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    platform TEXT,
    price INTEGER,
    created_at TIMESTAMP
)
```

### **price_alerts** (가격 알림)
```sql
CREATE TABLE price_alerts (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    target_price INTEGER,
    platform TEXT,
    created_at TIMESTAMP
)
```

### **tracked_products** (추적 상품)
```sql
CREATE TABLE tracked_products (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    keyword TEXT,
    created_at TIMESTAMP
)
```

---

## 🛠️ 기술 스택

- **Python 3.8+**
- **FastMCP** - MCP 프레임워크
- **Requests** - HTTP 클라이언트
- **SQLite** - 데이터베이스
- **Python-dotenv** - 환경 변수 관리

---

## 🔑 API 정보

### 네이버 쇼핑 API
- **제공:** 네이버 개발자 센터
- **무료 한도:** 하루 25,000회
- **기능:** 상품 검색, 가격 조회, 상세 정보

---

## 📝 라이선스

MIT License

---

## 👨‍💻 개발자

**Kim Taewoo** (xodn-sell)
- GitHub: https://github.com/xodn-sell
- 한국기술교육대학교 기계공학부

---

## 🏆 대회 정보

**카카오 MCP Player 10**
- 마감: 2026년 1월 18일
- 상금: 2,100만원 (1등 1,000만원)
- 발표: 2026년 2월 3일

---

## 🙏 감사의 말

- **카카오** - PlayMCP 플랫폼 제공
- **Anthropic** - MCP 프로토콜 개발
- **네이버** - 쇼핑 API 제공

---

## 📞 문의

버그 리포트 및 기능 제안:
- GitHub Issues: https://github.com/xodn-sell/price-tracker-mcp/issues
