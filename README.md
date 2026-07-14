# IHM AI Admission Counseling MCP Server

Agentic Player 10 공모전 예선용 MCP 서버 프로토타입입니다.

## 목적

학생 성적, 전공 희망, 대학 입결, 면접 질문을 연결해 진로진학 상담을 돕는 MCP 도구를 제공합니다.

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
