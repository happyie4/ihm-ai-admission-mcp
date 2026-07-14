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

AI 진로진학 상담을 위한 MCP 서버입니다. 공모전 시연용 더미 학생 데이터를 사용하여 지원 적합도 분석, 상담 보고서 생성, 면접 예상 질문 추천 도구를 제공합니다. 실제 학생 개인정보는 사용하지 않습니다.

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

## 제공 도구

- `list_demo_students`
- `analyze_admission_fit`
- `generate_admission_report`
- `recommend_interview_questions`
