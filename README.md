# IHM AI Admission Counseling MCP Server

Agentic Player 10 공모전 예선용 MCP 서버 프로토타입입니다.

## 목적

학생 성적, 전공 희망, 대학 입결, 면접 질문을 연결해 진로진학 상담을 돕는 MCP 도구를 제공합니다.

## 공모전 등록 정보

- MCP 이름: `AI 진로진학 상담 MCP`
- MCP 식별자: `ihm-ai-admission-mcp`
- MCP 설명:

```text
AI 진로진학 상담을 위한 MCP 서버입니다. 공모전 시연용 더미 학생 데이터를 사용하여 지원 적합도 분석, 상담 보고서 생성, 면접 예상 질문 추천 도구를 제공합니다. 실제 학생 개인정보는 사용하지 않습니다.
```

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

## 개인정보 보호

이 서버는 공모전 제출용 더미 데이터만 사용합니다.
실제 프로젝트 DB인 `Data/private/ihm_02.sqlite3`는 사용하지 않습니다.

## Endpoint

```text
POST /mcp
GET /health
```

## Tools

- `list_demo_students`: 더미 학생 목록 조회
- `analyze_admission_fit`: 학생 환산내신과 입결 70%컷 비교
- `generate_admission_report`: 상담 보고서 초안 생성
- `recommend_interview_questions`: 전공 기반 면접 질문 추천

## Local Run

```bash
python server.py
```

## Docker Run

```bash
docker build -t ihm-mcp .
docker run -p 8080:8080 ihm-mcp
```
