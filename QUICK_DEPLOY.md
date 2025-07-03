# 🚀 빠른 배포 가이드

## ✅ 1단계: GitHub 저장소 (완료!)
- ✅ 저장소 생성: https://github.com/ddoriboo/cdp-streamlit
- ✅ 코드 업로드 완료

## 🌐 2단계: Streamlit Cloud 배포 (클릭만 하면 완료!)

### 배포 링크
👉 **[여기를 클릭해서 바로 배포하기](https://share.streamlit.io/new?repository=ddoriboo/cdp-streamlit&branch=main&mainModule=app.py)**

### 수동 배포 방법
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. "New app" 클릭
3. 다음 정보 입력:
   - **Repository**: `ddoriboo/cdp-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`

## 🔑 3단계: API 키 설정 (필수!)

배포 후 반드시 다음을 설정하세요:

1. 앱 대시보드에서 "Settings" → "Secrets" 클릭
2. 다음 내용 입력:
```toml
OPENAI_API_KEY = "제공해주신-API-키"
```
3. "Save" 클릭

## 🎉 완료!

배포가 완료되면 다음과 같은 URL로 접속할 수 있습니다:
- `https://your-app-name.streamlit.app`

## 📱 사용법

1. 앱 접속
2. 사이드바에서 API 키 확인 (이미 설정되어 있음)
3. 쿼리 분석기에서 질문 입력
   - 예: "대출 니즈가 높은 고객군 알려줘"
4. AI 분석 결과 확인
5. SQL 쿼리 복사해서 활용

## 🔧 문제 해결

### API 키 오류가 나는 경우
1. Streamlit Cloud에서 Secrets 설정 확인
2. OpenAI API 키가 유효한지 확인
3. API 키에 충분한 크레딧이 있는지 확인

### 앱이 로드되지 않는 경우
1. 앱 대시보드에서 "Logs" 확인
2. 오류 메시지 확인 후 수정

## 📞 지원

문제가 있으면 [GitHub Issues](https://github.com/ddoriboo/cdp-streamlit/issues)에 등록해주세요!