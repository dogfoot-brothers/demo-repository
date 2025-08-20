# AutoPromptix - AI 프롬프트 최적화 시스템

AI가 자동으로 프롬프트를 최적화하여 원하는 결과를 얻을 수 있는 시스템입니다.

## 🚀 주요 기능

- **자동 프롬프트 최적화**: AI가 사용자 입력을 분석하여 최적의 프롬프트 생성
- **스마트 변이 생성**: 사용자 요청에 맞는 맞춤형 프롬프트 변이 자동 생성
- **실시간 점수 평가**: 다양한 평가 메트릭을 통한 프롬프트 품질 측정
- **사용자 정의 요구사항**: 추가 요구사항을 통한 세밀한 프롬프트 조정
- **제외 키워드 관리**: 원하지 않는 내용이 포함되지 않도록 키워드 제외

## 🏗️ 프로젝트 구조

```
demo-repository/
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 API 서버
│   ├── autopromptix_efficient.py  # 프롬프트 최적화 엔진
│   ├── scorer_simple.py    # 점수 평가 시스템
│   └── llm.py              # LLM 연동 서비스
├── frontend/               # React 프론트엔드
│   └── src/
│       └── pages/
│           └── PromptOptimizationPage.jsx  # 메인 UI
├── requirements.txt         # Python 의존성
└── README.md               # 프로젝트 설명서
```

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **OpenAI API**: GPT 모델 연동
- **rapidfuzz**: 텍스트 유사도 계산
- **rouge-score**: ROUGE 메트릭 계산

### Frontend
- **React**: 사용자 인터페이스
- **Vite**: 빌드 도구
- **Tailwind CSS**: 스타일링
- **Lucide React**: 아이콘

## 📦 설치 및 실행

### 1. 백엔드 설정

```bash
cd backend
pip install -r ../requirements.txt
```

환경 변수 설정:
```bash
# .env 파일 생성
OPENAI_API_KEY=your_api_key_here
```

### 2. 백엔드 실행

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 프론트엔드 설정

```bash
cd frontend
npm install
```

### 4. 프론트엔드 실행

```bash
cd frontend
npm run dev
```

## 🔧 사용 방법

1. **사용자 입력**: 최적화하고 싶은 프롬프트 입력
2. **기대 결과**: 원하는 결과물의 형태와 내용 설명
3. **제품명**: 관련 제품/서비스 이름 입력
4. **제외 키워드**: 포함되지 않았으면 하는 키워드 입력
5. **추가 요구사항**: 구체적인 작성 스타일이나 요구사항 입력
6. **최적화 시작**: AI가 자동으로 프롬프트를 최적화

## 📊 최적화 과정

1. **사용자 입력 분석**: AI가 요청을 분석하여 적합한 방향 결정
2. **스마트 변이 생성**: 분석 결과에 따른 맞춤형 프롬프트 변이 생성
3. **점수 평가**: 각 변이를 LLM으로 실행하고 점수 계산
4. **최적 결과 선택**: 가장 높은 점수의 프롬프트 선택
5. **결과 출력**: 최적화된 프롬프트와 생성된 출력 제공

## 🎯 평가 메트릭

- **코사인 유사도**: 텍스트 간 의미적 유사성
- **ROUGE-L**: 긴 시퀀스 매칭 정확도
- **키워드 커버리지**: 필수 키워드 포함 여부
- **구조적 품질**: 문서 구조와 가독성
- **제외 키워드 페널티**: 금지된 키워드 포함 시 점수 감점

## 🔒 환경 변수

| 변수명 | 설명 | 필수 여부 |
|--------|------|-----------|
| `OPENAI_API_KEY` | OpenAI API 키 | ✅ 필수 |

## 📝 라이선스

이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
