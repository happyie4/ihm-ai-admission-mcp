# PlayMCP 등록 메모

## 임시 등록 전 확인

1. PlayMCP in KC에서 이 폴더를 Git 소스 또는 컨테이너 이미지로 배포한다.
2. 발급된 Endpoint URL 뒤의 MCP 경로는 `/mcp`이다.
3. PlayMCP 개발자 콘솔의 MCP Endpoint에는 다음 형식으로 입력한다.

```text
https://발급된-endpoint-url/mcp
```

## 서버 정보

- 서버명: `ihm-ai-admission-counseling`
- 목적: AI 진로진학 상담 의사결정 지원
- 개인정보: 실제 학생 데이터 미사용, 공모전용 더미 데이터만 사용

## 등록 시 소개 문구

AI 진로진학 상담 MCP 서버는 학생의 희망 전공, 성적, 대학 입결, 면접 준비를 연결하여 상담교사가 근거 기반 상담 보고서를 빠르게 만들 수 있도록 돕는 도구입니다. 본 예선 서버는 개인정보 보호를 위해 더미 학생 데이터만 사용합니다.

## 제공 도구

- `list_demo_students`
- `analyze_admission_fit`
- `generate_admission_report`
- `recommend_interview_questions`
