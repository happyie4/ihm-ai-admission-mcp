#!/usr/bin/env python3
"""Validate metadata against the 2026-06-12 PlayMCP development guide."""

import re
import sys

from server import PROTOCOL_VERSION, SERVICE_NAME, TOOLS

REQUIRED_ANNOTATIONS = {
    "title", "readOnlyHint", "destructiveHint", "openWorldHint", "idempotentHint"
}
NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


def main():
    errors = []
    names = []
    if PROTOCOL_VERSION not in {"2025-03-26", "2025-06-18", "2025-11-25"}:
        errors.append(f"지원 범위 밖 protocolVersion: {PROTOCOL_VERSION}")
    if not 3 <= len(TOOLS) <= 10:
        errors.append(f"권장 Tool 개수(3~10) 위반: {len(TOOLS)}")

    for tool in TOOLS:
        name = tool.get("name", "")
        names.append(name)
        if not NAME_PATTERN.fullmatch(name):
            errors.append(f"잘못된 Tool 이름: {name}")
        if "kakao" in name.lower():
            errors.append(f"금지 문자열 kakao 포함: {name}")
        for field in ("name", "description", "inputSchema", "annotations"):
            if field not in tool:
                errors.append(f"{name}: 필수 property 누락: {field}")
        description = tool.get("description", "")
        if SERVICE_NAME not in description:
            errors.append(f"{name}: 영문·국문 서비스명 누락")
        if len(description) > 1024:
            errors.append(f"{name}: description 1,024자 초과")
        missing = REQUIRED_ANNOTATIONS - set(tool.get("annotations", {}))
        if missing:
            errors.append(f"{name}: annotations 누락: {sorted(missing)}")

    if len(names) != len(set(names)):
        errors.append("중복 Tool 이름 존재")
    if errors:
        print("PlayMCP 가이드 검증 실패")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PlayMCP 가이드 메타데이터 검증 통과: Tool {len(TOOLS)}개")
    print(f"protocolVersion={PROTOCOL_VERSION}, stateless HTTP endpoint=/mcp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
