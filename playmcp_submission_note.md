# PlayMCP 등록 메모

## 임시 등록 전 확인

1. PlayMCP in KC에서 이 폴더를 Git 소스 또는 컨테이너 이미지로 배포한다.
2. 발급된 Endpoint URL 뒤의 MCP 경로는 `/mcp`이다.
3. PlayMCP 개발자 콘솔의 MCP Endpoint에는 다음 형식으로 입력한다.

```text
https://발급된-endpoint-url/mcp
```

## 서버 정보

- MCP 이름: `AI 진로진학 상담 MCP`
- MCP 식별자: `ihm-ai-admission-mcp`
- 목적: AI 진로진학 상담 의사결정 지원
- 개인정보: 실제 학생 데이터 미사용, 공모전용 더미 데이터만 사용

## 등록 시 소개 문구

AI 진로진학 상담을 위한 MCP 서버입니다. 공모전 시연용 더미 학생 데이터를 사용하여 지원 적합도 분석, 상담 보고서 생성, 면접 예상 질문 추천, 선행학습영향평가 기반 면접 대비 기준 조회, 상담자 코멘트 생성, 최근 3년 입시결과 추세 조회 도구를 제공합니다. 실제 학생 개인정보는 사용하지 않습니다.

## 대화 예시

```text
공모전용 더미 학생 목록을 보여 주세요.
```

```text
사례학생 A의 고려대학교 경영학과 학교추천 전형 지원 적합도를 분석해 주세요.
```

```text
사례학생 B가 산업공학과 면접을 준비할 때 받을 만한 예상 질문을 추천해 주세요.
```

```text
고려대학교 학교추천 전형의 선행학습영향평가 기반 면접 대비 포인트를 알려 주세요.
```

```text
사례학생 A의 고려대학교 경영학과 학교추천 전형에 대한 상담자 코멘트를 작성해 주세요.
```

```text
고려대학교 경영학과 학교추천 전형의 최근 3년 입시결과 추세를 보여 주세요.
```

## 제공 도구

- `list_demo_students`
- `analyze_admission_fit`
- `generate_admission_report`
- `recommend_interview_questions`
- `search_prior_learning_assessment`
- `generate_counselor_comment`
- `get_admission_result_trend`

## 심사 이후 고도화 메모

심사 중인 배포본은 함부로 재배포하지 않는다.

다음 고도화 후보:

- 고려대학교 주요 모집단위 2025·2026 입결 시연 데이터 확대
- 2024 입결 공식자료 확인 후 `자료준비중` 값을 실제 공식값으로 대체
- `get_admission_result_trend`를 PlayMCP 재배포본에 반영

## 2026-07-16 심사 의견 조치

- 6개 심사 대상 Tool의 description 서비스명과 annotations는 커밋 `fabbe70`에 반영되어 있다.
- 로컬 메타데이터 검증을 통과했다.
- GitHub Actions 컨테이너 빌드도 성공했다.
- 심사 의견은 KC의 이전 이미지 응답으로 판단한다.
- 재심사 시 `ghcr.io/happyie4/ihm-ai-admission-mcp:sha-fabbe70`으로 KC 배포를 갱신한다.
- 정보 불러오기 후 6개 Tool을 확인하고 재심사를 요청한다.
