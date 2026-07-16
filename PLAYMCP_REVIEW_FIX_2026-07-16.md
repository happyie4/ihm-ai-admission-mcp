# PlayMCP 심사 의견 조치

## 심사 의견

6개 Tool에 대해 다음 두 항목이 지적되었다.

- `annotations` 미정의
- `description`에 서비스명 `AI 진로진학 상담 MCP` 미포함

## 코드 확인 결과

수정 커밋 `fabbe70b254dd3e53a7fc5daa438f3aaa4fba09d`에는 6개 Tool 모두 다음 사항이 반영되어 있다.

- description에 정확한 서비스명 `AI 진로진학 상담 MCP` 포함
- `annotations.title`
- `annotations.readOnlyHint=true`
- `annotations.destructiveHint=false`
- `annotations.idempotentHint=true`
- `annotations.openWorldHint=false`

GitHub Actions `Publish Docker image` 실행 `29328604013`도 성공했다.

## 원인 판단

심사 의견은 annotations 수정 전의 오래된 KC 컨테이너가 응답한 결과로 판단된다. `latest` 태그를 그대로 재사용하면 배포 환경의 이미지 캐시 때문에 수정 이미지가 반영되지 않을 수 있다.

## 재배포 절차

1. PlayMCP in KC에서 `ihm-ai-admission-mcp` 배포를 수정하거나 새 리비전을 만든다.
2. Registry는 `ghcr.io`, image name은 `happyie4/ihm-ai-admission-mcp`를 사용한다.
3. image tag는 `latest` 대신 annotations 수정 커밋의 고정 태그 `sha-fabbe70`을 사용한다.
4. 상태가 `Active`가 될 때까지 기다린다.
5. PlayMCP 개발자 콘솔에서 MCP Endpoint의 `정보 불러오기`를 다시 실행한다.
6. Tool이 6개인지 확인한다.
7. 각 Tool 상세에 annotations가 표시되고 description이 `AI 진로진학 상담 MCP`를 포함하는지 확인한다.
8. 저장 후 재심사를 요청한다.

## 주의

- 재심사 수정본에는 개발 중인 7번째 Tool `get_admission_result_trend`를 포함하지 않는다.
- 현재 심사 범위를 유지하기 위해 6개 Tool 버전 `fabbe70`을 사용한다.
- KC에서 고정 태그가 보이지 않으면 GitHub Container Registry의 `latest`가 수정 빌드인지 확인한 뒤 KC 리비전을 새로 생성한다.
