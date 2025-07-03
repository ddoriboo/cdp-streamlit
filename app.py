import streamlit as st
import openai
import json
import os
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="🚀 CDP x LLM Test",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CDP 컬럼 정의
CDP_COLUMNS = {
    "interests": {
        'fa_int_householdsingle': '1인 가구 관련 상품 결제',
        'fa_int_householdpet': '반려동물 관련 상품 결제',
        'fa_int_householdchild': '어린이 관련 상품 결제',
        'fa_int_householdbaby': '영유아 관련 상품 결제',
        'fa_int_loan1stfinancial': '1금융권 신용대출 실행',
        'fa_int_loan2ndfinancial': '2금융권 신용대출 실행',
        'fa_int_loanpersonal': '신용대출 실행',
        'fa_int_saving': '예적금 개설',
        'fa_int_homeappliance': '가전 상품 결제',
        'fa_int_luxury': '명품 관련 결제',
        'fa_int_delivery': '배달 결제',
        'fa_int_carinsurance': '자동차 보험 결제 예정',
        'fa_int_carpurchase': '차량 구매',
        'fa_int_traveloverseas': '해외여행 예정',
        'fa_int_traveldomestic': '국내여행',
        'fa_int_golf': '골프 관련 결제',
        'fa_int_gym': '피트니스/헬스장 결제',
        'fa_int_wedding': '결혼 준비 관련',
        'fa_int_highincome': '추정소득 1억 이상',
        'fa_int_homeowner': '주택 소유',
        'fa_int_business': '사업자',
        'fa_int_worker': '정기 급여 수령'
    },
    "industries": {
        'fa_ind_finance': '금융 결제',
        'fa_ind_insurance': '보험 결제',
        'fa_ind_beauty': '미용 결제',
        'fa_ind_medical': '의료 결제',
        'fa_ind_travel': '여행 결제',
        'fa_ind_foodbeverage': 'F&B 결제',
        'fa_ind_cafe': '카페 결제',
        'fa_ind_restaurant': '음식점 결제',
        'fa_ind_delivery': '배달 결제',
        'fa_ind_cosmetic': '뷰티 결제',
        'fa_ind_fashion': '패션의류 결제',
        'fa_ind_digitalappliances': '디지털가전 결제',
        'fa_ind_education': '교육 결제',
        'fa_ind_golfcourse': '골프장 결제',
        'fa_ind_fitness': '피트니스 결제'
    },
    "scores": {
        'sc_int_loan1stfinancial': '1금융권 대출 예측스코어',
        'sc_int_loan2ndfinancial': '2금융권 대출 예측스코어',
        'sc_int_luxury': '명품 구매 예측스코어',
        'sc_int_delivery': '배달 이용 예측스코어',
        'sc_int_golf': '골프 관련 예측스코어',
        'sc_int_highincome': '고소득 예측스코어',
        'sc_int_wedding': '결혼 준비 예측스코어',
        'sc_ind_beauty': '미용 서비스 예측스코어',
        'sc_ind_cosmetic': '뷰티 제품 예측스코어',
        'sc_ind_finance': '금융 서비스 예측스코어'
    },
    "flags": {
        'fi_npay_age20': '20대',
        'fi_npay_age30': '30대',
        'fi_npay_age40': '40대',
        'fi_npay_genderf': '여성',
        'fi_npay_genderm': '남성',
        'fi_npay_membershipnormal': '플러스멤버십 가입',
        'fi_npay_myassetreg': '내자산 서비스 연동',
        'fi_npay_creditcheck': '신용조회 서비스 가입'
    }
}

# 팀별 추천 질문 정의
TEAM_QUESTIONS = {
    'financial-content': {
        'name': '정선영님',
        'role': '금융 컨텐츠 (머니스토리)',
        'icon': '💰',
        'questions': [
            {
                'text': '고소득층 중 투자 관심도가 높은 고객 찾아줘',
                'description': '머니스토리 투자 콘텐츠에 관심을 가질 가능성이 높은 고객군 분석',
                'tags': ['투자', '고소득', '머니스토리']
            },
            {
                'text': '20-30대 여성 중 가계부 관리에 관심이 많은 고객',
                'description': '가계부 작성 및 가계 관리 콘텐츠 타겟 고객 발굴',
                'tags': ['가계부', '20-30대', '여성']
            },
            {
                'text': '대출 경험이 있으면서 금융 정보에 관심이 높은 고객',
                'description': '대출 관련 금융 교육 콘텐츠 수요층 분석',
                'tags': ['대출', '금융교육', '콘텐츠']
            },
            {
                'text': '적금/예금 개설 경험이 있는 고객 중 재테크 관심군',
                'description': '저축 상품 비교 및 재테크 콘텐츠 타겟 고객',
                'tags': ['적금', '예금', '재테크']
            }
        ]
    },
    'member-planning': {
        'name': '박지영님',
        'role': '회원 플래닝',
        'icon': '👥',
        'questions': [
            {
                'text': '플러스 멤버십 가입 가능성이 높은 고객',
                'description': '멤버십 혜택 활용도가 높을 것으로 예상되는 고객군 분석',
                'tags': ['멤버십', '가입전환', '혜택']
            },
            {
                'text': '최근 3개월 간 활동이 감소한 기존 회원',
                'description': '회원 이탈 방지 및 재활성화 대상 고객 식별',
                'tags': ['회원이탈', '재활성화', '리텐션']
            },
            {
                'text': '네이버페이 사용 빈도가 높은 고객',
                'description': '페이 서비스 충성도가 높은 핵심 고객층 분석',
                'tags': ['네이버페이', '충성도', '활성사용자']
            },
            {
                'text': '다양한 카테고리에서 결제하는 고객',
                'description': '종합적인 서비스 이용 패턴을 보이는 고객 특성 분석',
                'tags': ['다양성', '결제패턴', '종합이용']
            }
        ]
    },
    'myasset': {
        'name': '김정희님',
        'role': '내자산 플래닝 (마이데이터)',
        'icon': '🏦',
        'questions': [
            {
                'text': '내자산 서비스 연동 가능성이 높은 고객',
                'description': '마이데이터 서비스 이용 의향이 높은 고객군 발굴',
                'tags': ['마이데이터', '내자산', '연동']
            },
            {
                'text': '다수의 금융기관 이용 고객',
                'description': '자산 통합 관리 니즈가 있는 고객 식별',
                'tags': ['통합관리', '다수계좌', '자산관리']
            },
            {
                'text': '신용조회 서비스 가입 고객의 자산 관리 패턴',
                'description': '신용관리에 관심이 높은 고객의 자산 관리 행태 분석',
                'tags': ['신용조회', '자산관리', '금융관리']
            },
            {
                'text': '정기적인 투자 활동을 하는 고객',
                'description': '포트폴리오 관리 서비스 수요가 높은 고객군',
                'tags': ['투자', '포트폴리오', '정기투자']
            }
        ]
    },
    'advertising': {
        'name': '고시현님',
        'role': 'AD 서비스',
        'icon': '📢',
        'questions': [
            {
                'text': '온라인 쇼핑 빈도가 높은 고객',
                'description': '광고 노출 효과가 높을 것으로 예상되는 활성 쇼핑 고객',
                'tags': ['온라인쇼핑', '광고효과', '활성고객']
            },
            {
                'text': '20-30대 중 뷰티/패션 관심사가 높은 고객',
                'description': '뷰티/패션 광고 타겟팅에 적합한 고객군 분석',
                'tags': ['뷰티', '패션', '20-30대']
            },
            {
                'text': '브랜드 충성도가 높은 고객',
                'description': '특정 브랜드에 대한 재구매율이 높은 고객 특성',
                'tags': ['브랜드', '충성도', '재구매']
            },
            {
                'text': '계절별 소비 패턴이 뚜렷한 고객',
                'description': '시즌별 광고 캠페인 최적화를 위한 고객 분석',
                'tags': ['계절성', '소비패턴', '캠페인']
            }
        ]
    },
    'payment': {
        'name': '최동주님',
        'role': '결제 데이터',
        'icon': '💳',
        'questions': [
            {
                'text': '결제 수단 다양성이 높은 고객',
                'description': '여러 결제 수단을 활용하는 고객의 결제 패턴 분석',
                'tags': ['결제수단', '다양성', '결제패턴']
            },
            {
                'text': '고액 결제를 자주 하는 고객',
                'description': '프리미엄 결제 서비스 수요가 높은 고객군',
                'tags': ['고액결제', '프리미엄', 'VIP']
            },
            {
                'text': '해외 결제 경험이 있는 고객',
                'description': '해외 결제 서비스 개선 및 확대를 위한 고객 분석',
                'tags': ['해외결제', '글로벌', '여행']
            },
            {
                'text': '정기 결제 서비스 이용 고객',
                'description': '구독 서비스 및 정기 결제 활용도가 높은 고객',
                'tags': ['정기결제', '구독', '자동결제']
            }
        ]
    },
    'loan': {
        'name': '이승한님',
        'role': '대출 서비스',
        'icon': '🏠',
        'questions': [
            {
                'text': '대출 니즈가 높은 고객군',
                'description': '신용대출 상품 제안에 적합한 고객 발굴',
                'tags': ['대출', '신용대출', '금융상품']
            },
            {
                'text': '주택 구매 관련 활동이 있는 고객',
                'description': '주택담보대출 수요가 있는 고객 식별',
                'tags': ['주택', '부동산', '담보대출']
            },
            {
                'text': '기존 대출 고객 중 추가 대출 가능성이 높은 고객',
                'description': '대환대출 또는 한도 증액 대상 고객 분석',
                'tags': ['기존고객', '대환대출', '한도증액']
            },
            {
                'text': '신용등급이 양호하면서 소득이 안정적인 고객',
                'description': '우대 금리 대출 상품 타겟 고객 발굴',
                'tags': ['신용등급', '소득안정', '우대금리']
            }
        ]
    }
}

def get_openai_client():
    """OpenAI 클라이언트 초기화"""
    api_key = None
    
    # 1. Streamlit secrets에서 시도
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    
    # 2. 환경변수에서 시도
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    # 3. 사용자 입력에서 시도
    if not api_key and 'api_key' in st.session_state:
        api_key = st.session_state.api_key
    
    if api_key:
        return openai.OpenAI(api_key=api_key)
    return None

def analyze_query_with_ai(user_query: str, client) -> Dict[str, Any]:
    """사용자 질문을 AI로 분석"""
    
    system_prompt = f"""당신은 CDP(Customer Data Platform) 전문가입니다. 사용자의 자연어 질문을 분석하여 최적의 고객 세그먼테이션 전략을 제공합니다.

다음 CDP 컬럼들을 활용하여 분석해주세요:
{json.dumps(CDP_COLUMNS, ensure_ascii=False, indent=2)}

응답은 반드시 다음 JSON 형식으로만 제공해주세요. 다른 텍스트는 포함하지 마세요:
{{
    "query_analysis": "사용자 질문 분석 내용",
    "target_description": "타겟 고객군 설명",
    "recommended_columns": [
        {{
            "column": "컬럼명",
            "description": "컬럼 설명",
            "condition": "추천 조건 (예: > 0.7, IS NOT NULL 등)",
            "priority": "high|medium|low",
            "reasoning": "선택 이유"
        }}
    ],
    "sql_query": "SELECT 문으로 된 쿼리",
    "business_insights": [
        "비즈니스 인사이트 1",
        "비즈니스 인사이트 2"
    ],
    "estimated_target_size": "예상 타겟 규모 (%)",
    "marketing_recommendations": [
        "마케팅 추천사항 1",
        "마케팅 추천사항 2"
    ]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = response.choices[0].message.content
        return json.loads(ai_response)
    
    except json.JSONDecodeError as e:
        st.error(f"AI 응답 파싱 오류: {e}")
        return None
    except Exception as e:
        st.error(f"AI 분석 오류: {e}")
        return None

def display_results(result: Dict[str, Any]):
    """분석 결과 표시"""
    if not result:
        return
    
    # 질문 분석 결과
    st.markdown("### 🤖 AI 질문 분석 결과")
    st.info(result.get('query_analysis', ''))
    
    # 타겟 고객군 정의
    st.markdown("### 🎯 타겟 고객군 정의")
    st.success(result.get('target_description', ''))
    
    # 통계 카드
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "AI 추천 컬럼 수", 
            len(result.get('recommended_columns', []))
        )
    with col2:
        st.metric(
            "예상 타겟 규모", 
            result.get('estimated_target_size', 'N/A')
        )
    with col3:
        st.metric(
            "AI 마케팅 제안", 
            len(result.get('marketing_recommendations', []))
        )
    
    # 추천 컬럼
    st.markdown("### 🧠 AI 추천 CDP 컬럼 조합")
    columns = result.get('recommended_columns', [])
    
    # 우선순위별 그룹화
    high_priority = [c for c in columns if c.get('priority') == 'high']
    medium_priority = [c for c in columns if c.get('priority') == 'medium']
    low_priority = [c for c in columns if c.get('priority') == 'low']
    
    if high_priority:
        st.markdown("#### 🔥 핵심 지표")
        for col in high_priority:
            with st.expander(f"**{col.get('column')}** - {col.get('description')}"):
                st.write(f"**조건:** {col.get('condition')}")
                st.write(f"**선택 이유:** {col.get('reasoning')}")
    
    if medium_priority:
        st.markdown("#### ⭐ 보조 지표")
        for col in medium_priority:
            with st.expander(f"**{col.get('column')}** - {col.get('description')}"):
                st.write(f"**조건:** {col.get('condition')}")
                st.write(f"**선택 이유:** {col.get('reasoning')}")
    
    if low_priority:
        st.markdown("#### 💡 참고 지표")
        for col in low_priority:
            with st.expander(f"**{col.get('column')}** - {col.get('description')}"):
                st.write(f"**조건:** {col.get('condition')}")
                st.write(f"**선택 이유:** {col.get('reasoning')}")
    
    # SQL 쿼리
    st.markdown("### 📝 AI 생성 SQL 쿼리")
    sql_query = result.get('sql_query', '')
    st.code(sql_query, language='sql')
    
    if st.button("📋 SQL 쿼리 복사"):
        st.write("SQL 쿼리가 클립보드에 복사되었습니다!")
        st.code(sql_query)
    
    # 비즈니스 인사이트
    st.markdown("### 💡 AI 비즈니스 인사이트")
    for insight in result.get('business_insights', []):
        st.write(f"• {insight}")
    
    # 마케팅 활용 방안
    st.markdown("### 🚀 AI 마케팅 활용 방안")
    for rec in result.get('marketing_recommendations', []):
        st.write(f"• {rec}")

def show_column_browser():
    """컬럼 브라우저 페이지"""
    st.markdown("## 📊 CDP 컬럼 브라우저")
    st.markdown("CDP 데이터베이스의 모든 컬럼을 탐색하고 활용법을 확인하세요.")
    
    # 검색 기능
    search_term = st.text_input("🔍 컬럼명이나 설명으로 검색...")
    
    # 카테고리 필터
    category_filter = st.selectbox(
        "카테고리 선택",
        ["전체", "관심사 지표", "업종별 지표", "예측 스코어", "플래그 지표"],
        index=0
    )
    
    category_map = {
        "전체": "all",
        "관심사 지표": "interests",
        "업종별 지표": "industries", 
        "예측 스코어": "scores",
        "플래그 지표": "flags"
    }
    
    selected_category = category_map[category_filter]
    
    # 컬럼 표시
    for category, columns in CDP_COLUMNS.items():
        if selected_category != "all" and selected_category != category:
            continue
            
        category_labels = {
            "interests": "관심사 지표",
            "industries": "업종별 지표",
            "scores": "예측 스코어",
            "flags": "플래그 지표"
        }
        
        st.markdown(f"### {category_labels.get(category, category)}")
        
        for col_name, description in columns.items():
            # 검색 필터링
            if search_term and search_term.lower() not in col_name.lower() and search_term.lower() not in description.lower():
                continue
                
            with st.expander(f"**{col_name}**"):
                st.write(description)
                
                # 컬럼 타입 정보
                if col_name.startswith('sc_'):
                    st.write("**타입:** 📊 Double (0-1)")
                elif col_name.startswith('fi_'):
                    st.write("**타입:** 🏷️ Boolean")
                else:
                    st.write("**타입:** 📅 Date")
                
                if st.button(f"이 컬럼 사용하기", key=f"use_{col_name}"):
                    st.session_state.selected_query = f"{col_name} 컬럼을 활용한 고객 세그먼테이션 분석해줘"
                    st.success(f"쿼리가 설정되었습니다! 쿼리 분석기 탭으로 이동하세요.")

def show_team_recommendations():
    """팀별 추천 페이지"""
    st.markdown("## 👥 팀별 맞춤 추천 질문")
    st.markdown("각 담당자님의 업무 영역에 특화된 질문들을 추천드립니다.")
    
    # 팀 선택
    team_names = [f"{data['icon']} {data['name']} - {data['role']}" for data in TEAM_QUESTIONS.values()]
    team_keys = list(TEAM_QUESTIONS.keys())
    
    selected_team_idx = st.selectbox(
        "팀 선택",
        range(len(team_names)),
        format_func=lambda x: team_names[x]
    )
    
    selected_team_key = team_keys[selected_team_idx]
    team_data = TEAM_QUESTIONS[selected_team_key]
    
    st.markdown(f"### {team_data['icon']} {team_data['name']} - {team_data['role']}")
    
    # 추천 질문들
    for i, question in enumerate(team_data['questions']):
        with st.expander(f"**{question['text']}**"):
            st.write(question['description'])
            
            # 태그 표시
            tag_str = " ".join([f"`{tag}`" for tag in question['tags']])
            st.markdown(f"**태그:** {tag_str}")
            
            if st.button(f"이 질문 사용하기", key=f"team_q_{selected_team_key}_{i}"):
                st.session_state.selected_query = question['text']
                st.success(f"질문이 설정되었습니다! 쿼리 분석기 탭으로 이동하세요.")

def main():
    """메인 애플리케이션"""
    # 제목
    st.title("🚀 CDP x LLM Test")
    st.markdown("AI 기반 고객 세그먼테이션 · 컬럼 탐색 · 팀별 맞춤 추천")
    
    # 사이드바에서 API 키 설정
    with st.sidebar:
        st.markdown("### 🔑 API 키 설정")
        
        # 기존 API 키 확인
        client = get_openai_client()
        if client:
            st.success("✅ API 키가 설정되었습니다!")
        else:
            st.warning("⚠️ API 키를 설정해주세요.")
            
            api_key_input = st.text_input(
                "OpenAI API 키", 
                type="password",
                placeholder="sk-proj-로 시작하는 API 키를 입력하세요"
            )
            
            if st.button("API 키 저장"):
                if api_key_input and api_key_input.startswith('sk-'):
                    st.session_state.api_key = api_key_input
                    st.success("API 키가 저장되었습니다!")
                    st.rerun()
                else:
                    st.error("올바른 API 키 형식이 아닙니다.")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🔍 쿼리 분석기", "📊 컬럼 브라우저", "👥 팀별 추천"])
    
    with tab1:
        st.markdown("### 🔍 쿼리 분석기")
        
        # 기존 선택된 쿼리가 있다면 사용
        default_query = st.session_state.get('selected_query', '')
        
        # 쿼리 입력
        user_query = st.text_area(
            "질문을 입력하세요",
            value=default_query,
            placeholder="예: 대출 니즈가 높은 고객군 알려줘, 젊은 여성 중 뷰티 관심사가 높은 고객 찾아줘",
            height=100
        )
        
        # 예시 질문들
        st.markdown("**예시 질문:**")
        example_queries = [
            "💰 대출 니즈가 높은 고객군 알려줘",
            "💄 20-30대 여성 중 뷰티에 관심이 많은 고객",
            "📈 고소득층 중 투자 상품에 관심있는 고객",
            "✈️ 해외여행을 자주 가는 고객 중 보험 가입 가능성이 높은 사람",
            "🏠 1인 가구 중 배달음식을 자주 시키는 고객",
            "⛳ 골프를 치는 고객 중 프리미엄 서비스 이용 가능성이 높은 사람"
        ]
        
        cols = st.columns(3)
        for i, example in enumerate(example_queries):
            with cols[i % 3]:
                if st.button(example, key=f"example_{i}"):
                    st.session_state.selected_query = example.split(" ", 1)[1]  # 이모지 제거
                    st.rerun()
        
        # 분석 버튼
        if st.button("🔍 AI 분석 시작", type="primary", disabled=not bool(get_openai_client())):
            if not user_query:
                st.error("질문을 입력해주세요.")
            else:
                client = get_openai_client()
                if not client:
                    st.error("API 키를 먼저 설정해주세요.")
                else:
                    with st.spinner("🤖 실제 AI가 CDP 데이터를 분석하여 최적의 고객 세그먼테이션 전략을 생성하고 있습니다..."):
                        result = analyze_query_with_ai(user_query, client)
                        if result:
                            display_results(result)
                            # 선택된 쿼리 초기화
                            if 'selected_query' in st.session_state:
                                del st.session_state.selected_query
    
    with tab2:
        show_column_browser()
    
    with tab3:
        show_team_recommendations()

if __name__ == "__main__":
    main()