# PlayMCP 개발가이드 점검

기준일: 2026-06-12 개발가이드

## 통과 항목

- MCP protocolVersion: `2025-03-26`
- 전송: Remote Streamable HTTP `POST /mcp`
- 상태: 세션을 저장하지 않는 stateless 서버
- Tool: 7개, 이름 중복 및 금지 문자열 `kakao` 없음
- 필수 property: name, description, inputSchema, annotations
- annotations: title, readOnlyHint, destructiveHint, openWorldHint, idempotentHint
- description: 1,024자 이내, 영문·국문 서비스명 병기
- 개인정보: 실제 학생정보 없이 공모전용 더미 데이터만 사용
- 오류 응답: 정제된 text content와 `isError=true`
- 광고 응답: 없음

## 검사 결과

- 자체 검증 스크립트: Tool 7개 통과
- 공식 MCP Inspector `tools/list`: 통과
- 로컬 HTTP 응답시간
  - initialize: 2.0ms
  - tools/list: 1.6ms
  - 정상 tools/call: 3.8ms
  - 오류 tools/call: 1.4ms
- 가이드 성능 기준인 평균 100ms 이내를 로컬 환경에서 충족

## 운영 판단

현재 서버는 외부 SDK 의존성이 없는 최소 구현이다. MCP 2025-03-26 명세를 참조하고
공식 MCP Inspector로 상호운용성을 확인했다. 향후 OAuth, 세션, resource, prompt 등으로
범위가 확장되면 공식 Python SDK 기반 FastMCP로 전환한다. 공모전 재심사 시에는 기능을
확장하기보다 검증된 현재 범위를 유지한다.

## 배포 주의

이 변경은 기존 이미지 태그 `sha-fabbe70` 이후 버전이다. GitHub Actions 빌드가 성공한
새 고정 `sha-...` 태그를 PlayMCP in KC에 입력하고, Active 이후 정보 불러오기를 다시 한다.
