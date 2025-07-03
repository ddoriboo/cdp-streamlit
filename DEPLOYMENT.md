# 🚀 배포 가이드

이 문서는 CDP x LLM Test 플랫폼을 GitHub와 Streamlit Cloud에 배포하는 방법을 안내합니다.

## 📋 준비사항

1. **GitHub 계정** - 코드 저장소 호스팅
2. **OpenAI API 키** - [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급
3. **Streamlit Cloud 계정** - [Streamlit Cloud](https://share.streamlit.io/)에서 무료 가입

## 🔧 1단계: GitHub 저장소 생성

### 새 저장소 생성
1. GitHub에 로그인
2. 우상단 "+" 클릭 → "New repository"
3. Repository name: `cdp-streamlit` (또는 원하는 이름)
4. Public 선택 (Streamlit Cloud 무료 배포용)
5. "Create repository" 클릭

### 로컬 Git 설정
```bash
# 현재 디렉토리에서
git init
git add .
git commit -m "Initial commit: CDP x LLM Streamlit app"
git branch -M main
git remote add origin https://github.com/ddoriboo/cdp-streamlit.git
git push -u origin main
```

## 🌐 2단계: Streamlit Cloud 배포

### 앱 생성
1. [Streamlit Cloud](https://share.streamlit.io/)에 로그인
2. "New app" 버튼 클릭
3. 다음 정보 입력:
   - **Repository**: `ddoriboo/cdp-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: 원하는 URL (예: `cdp-llm-demo`)

### API 키 설정 (중요!)
1. 앱 생성 후 설정 페이지로 이동
2. 왼쪽 메뉴에서 "Secrets" 클릭
3. 다음 내용을 입력:

```toml
OPENAI_API_KEY = "sk-proj-YOUR-ACTUAL-API-KEY-HERE"
```

⚠️ **주의**: 실제 API 키로 교체하세요!

4. "Save" 클릭

### 배포 실행
1. "Deploy!" 버튼 클릭
2. 몇 분 후 앱이 자동으로 배포됨
3. 제공된 URL로 앱 접속 가능

## 🔒 3단계: 보안 설정

### API 키 보안
- **절대 금지**: API 키를 코드에 직접 입력
- **권장**: Streamlit Secrets 또는 환경변수 사용
- **추가 보안**: OpenAI API 키 사용량 모니터링

### 저장소 보안
```bash
# .gitignore 확인 (이미 설정됨)
cat .gitignore

# 민감한 파일들이 무시되는지 확인
git status
```

## 📊 4단계: 앱 테스트

### 기능 확인 체크리스트
- [ ] 앱이 정상적으로 로드되는가?
- [ ] API 키 설정이 올바른가?
- [ ] 쿼리 분석기가 작동하는가?
- [ ] 컬럼 브라우저가 표시되는가?
- [ ] 팀별 추천이 작동하는가?
- [ ] 모바일에서도 정상 작동하는가?

### 샘플 테스트
1. "대출 니즈가 높은 고객군 알려줘" 입력
2. AI 분석 결과 확인
3. SQL 쿼리 생성 확인
4. 컬럼 브라우저에서 검색 테스트
5. 팀별 추천 질문 클릭 테스트

## 🔄 5단계: 업데이트 배포

### 코드 수정 시
```bash
# 수정 후
git add .
git commit -m "Update: 변경사항 설명"
git push origin main
```

Streamlit Cloud가 자동으로 재배포합니다 (약 1-2분 소요).

### 의존성 변경 시
`requirements.txt` 수정 후 push하면 자동으로 재설치됩니다.

## 🎨 6단계: 커스터마이징

### 브랜딩 변경
- `app.py`의 제목과 설명 수정
- `.streamlit/config.toml`에서 색상 테마 변경
- 로고나 이미지 추가 가능

### 기능 확장
- 새로운 CDP 컬럼 추가
- 팀별 질문 템플릿 확장
- 분석 결과 시각화 개선

## 🔧 문제 해결

### 일반적인 배포 문제

#### 1. 앱이 로드되지 않음
```
Streamlit Cloud 로그 확인:
1. 앱 대시보드 → "Manage app" → "Logs"
2. 오류 메시지 확인
3. requirements.txt 의존성 확인
```

#### 2. API 키 오류
```
해결책:
1. Streamlit Secrets에서 API 키 재확인
2. OpenAI API 키 유효성 확인
3. API 사용량 한도 확인
```

#### 3. 모듈 import 오류
```bash
# requirements.txt 업데이트
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push origin main
```

### 성능 최적화

#### 캐시 활용
```python
@st.cache_data
def load_cdp_columns():
    return CDP_COLUMNS
```

#### 메모리 관리
- 큰 데이터는 세션 상태에 저장
- 불필요한 데이터 정리

## 📈 모니터링

### 사용량 추적
1. OpenAI API 사용량 모니터링
2. Streamlit Cloud 리소스 사용량 확인
3. 앱 성능 지표 관찰

### 로그 분석
```
Streamlit Cloud 대시보드에서:
- 앱 사용자 수
- 오류 발생 빈도
- 응답 시간
```

## 🤝 사용자에게 공유

### 공유 방법
1. **직접 링크**: Streamlit Cloud에서 제공하는 URL
2. **QR 코드**: 모바일 접근용
3. **임베딩**: iframe으로 웹사이트에 삽입 가능

### 사용 가이드
```markdown
## 사용법
1. 사이드바에서 OpenAI API 키 입력
2. 쿼리 분석기에서 자연어 질문 입력
3. AI 분석 결과 확인
4. SQL 쿼리 복사하여 활용
```

## 📞 지원

문제가 발생하면:
1. [GitHub Issues](https://github.com/ddoriboo/cdp-streamlit/issues)에 등록
2. Streamlit Community Forum 참조
3. OpenAI API 문서 확인

---

🎉 **축하합니다!** CDP x LLM 플랫폼이 성공적으로 배포되었습니다.