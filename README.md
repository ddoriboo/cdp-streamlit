# 🚀 CDP x LLM Test Platform

AI 기반 고객 세그먼테이션 · 컬럼 탐색 · 팀별 맞춤 추천 플랫폼

## 📋 기능

### 🔍 쿼리 분석기
- 자연어로 고객 세그먼테이션 질문 입력
- AI가 CDP 데이터를 분석하여 최적의 컬럼 조합 추천
- SQL 쿼리 자동 생성
- 비즈니스 인사이트 및 마케팅 활용 방안 제공

### 📊 컬럼 브라우저  
- CDP 데이터베이스의 모든 컬럼 탐색
- 카테고리별 필터링 (관심사, 업종별, 예측스코어, 플래그)
- 검색 기능으로 원하는 컬럼 빠르게 찾기
- 컬럼 활용법 및 데이터 타입 정보 제공

### 👥 팀별 추천
- 각 팀의 업무 영역에 특화된 질문 템플릿
- 금융 컨텐츠, 회원 플래닝, 내자산, 광고, 결제, 대출 팀별 맞춤 추천
- 원클릭으로 추천 질문을 쿼리 분석기에 적용

## 🚀 빠른 시작

### 1. 로컬 실행

```bash
# 저장소 클론
git clone https://github.com/your-username/cdp-streamlit.git
cd cdp-streamlit

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어서 OpenAI API 키를 입력하세요

# 앱 실행
streamlit run app.py
```

### 2. Streamlit Cloud 배포

1. 이 저장소를 GitHub에 푸시
2. [Streamlit Cloud](https://share.streamlit.io/)에 로그인
3. "New app" 클릭
4. GitHub 저장소 선택
5. Secrets에서 `OPENAI_API_KEY` 설정
6. Deploy 클릭

## 🔑 API 키 설정

### OpenAI API 키 발급
1. [OpenAI Platform](https://platform.openai.com/api-keys)에서 계정 생성
2. API 키 생성 (sk-proj-로 시작)
3. 아래 방법 중 하나로 설정:

### 로컬 개발
```bash
# .env 파일에 추가
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### Streamlit Cloud 배포
1. Streamlit Cloud 앱 설정 페이지
2. Secrets 탭 클릭
3. 다음 내용 추가:
```toml
OPENAI_API_KEY = "sk-proj-your-actual-api-key-here"
```

### 앱 내에서 설정
- 사이드바의 "API 키 설정" 섹션에서 직접 입력 가능
- 세션 동안만 유지됨

## 📊 CDP 데이터 구조

### 컬럼 카테고리
- **관심사 지표 (fa_int_*)**: 고객의 관심사별 행동 데이터
- **업종별 지표 (fa_ind_*)**: 업종별 결제 패턴 데이터  
- **예측 스코어 (sc_*)**: AI 예측 점수 (0-1 범위)
- **플래그 지표 (fi_npay_*)**: 고객 속성 플래그

### 데이터 타입
- **Date**: 이벤트 발생일 (fa_int_*, fa_ind_*)
- **Double**: 예측 점수 0-1 범위 (sc_*)
- **Boolean**: 참/거짓 플래그 (fi_*)

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI/LLM**: OpenAI GPT-4
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud

## 📁 프로젝트 구조

```
cdp-streamlit/
├── app.py                 # 메인 Streamlit 앱
├── requirements.txt       # Python 의존성
├── .streamlit/
│   └── secrets.toml      # Streamlit 시크릿 (로컬용)
├── .env.example          # 환경변수 예시
├── .gitignore           # Git 무시 파일
├── README.md            # 이 파일
└── aiqstream.html       # 원본 HTML 파일 (참고용)
```

## 🔒 보안

- API 키는 절대 코드에 하드코딩하지 않음
- 환경변수 또는 Streamlit Secrets 사용
- `.env` 및 `secrets.toml` 파일은 Git에서 제외

## 🤝 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🆘 문제 해결

### 일반적인 문제들

1. **API 키 오류**
   - OpenAI API 키가 올바른지 확인
   - API 키에 충분한 크레딧이 있는지 확인

2. **패키지 설치 오류**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Streamlit 실행 오류**
   ```bash
   streamlit --version
   streamlit run app.py --server.port 8501
   ```

## 📞 지원

문제가 있거나 제안사항이 있으시면 [Issues](https://github.com/your-username/cdp-streamlit/issues)에 등록해주세요.

---

**주의**: 이 앱은 데모/테스트 목적으로 제작되었습니다. 실제 운영 환경에서 사용하기 전에 보안 검토를 수행하세요.