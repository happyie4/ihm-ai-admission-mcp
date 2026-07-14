#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IHM-02 contest MCP server.

This server intentionally uses only demo data. Do not connect it to
Data/private/ihm_02.sqlite3 for public contest deployment.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "demo_data.json"


def load_data() -> Dict[str, Any]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def jsonrpc_result(request_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def jsonrpc_error(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def text_content(text: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "list_demo_students",
        "description": "공모전용 더미 학생 목록을 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "analyze_admission_fit",
        "description": "더미 학생의 내신과 대학 입결 70%컷을 비교해 지원 수준을 판단합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "integer"},
                "university": {"type": "string"},
                "major": {"type": "string"},
                "admission_type": {"type": "string"},
            },
            "required": ["student_id", "university", "major", "admission_type"],
            "additionalProperties": False,
        },
    },
    {
        "name": "generate_admission_report",
        "description": "더미 학생 기준의 진로진학 상담 보고서 초안을 생성합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "integer"},
                "university": {"type": "string"},
                "major": {"type": "string"},
                "admission_type": {"type": "string"},
            },
            "required": ["student_id", "university", "major", "admission_type"],
            "additionalProperties": False,
        },
    },
    {
        "name": "recommend_interview_questions",
        "description": "희망 전공과 학생 활동을 바탕으로 면접 예상 질문을 추천합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "student_id": {"type": "integer"},
                "major": {"type": "string"},
            },
            "required": ["student_id", "major"],
            "additionalProperties": False,
        },
    },
]


def find_student(data: Dict[str, Any], student_id: int) -> Dict[str, Any]:
    for student in data["students"]:
        if student["student_id"] == student_id:
            return student
    raise ValueError(f"student_id={student_id} 학생을 찾을 수 없습니다.")


def find_cutline(
    data: Dict[str, Any],
    university: str,
    major: str,
    admission_type: str,
) -> Dict[str, Any]:
    for cutline in data["admission_cutlines"]:
        if (
            cutline["university"] == university
            and cutline["major"] == major
            and cutline["admission_type"] == admission_type
        ):
            return cutline
    raise ValueError("해당 대학/학과/전형 입결 더미 데이터를 찾을 수 없습니다.")


def classify_fit(student_grade: float, cut_70_grade: float) -> Dict[str, str]:
    gap = round(student_grade - cut_70_grade, 2)
    if gap <= -0.30:
        level = "안정"
    elif gap <= 0.20:
        level = "적정"
    elif gap <= 0.60:
        level = "소신"
    else:
        level = "상향"

    return {
        "support_level": level,
        "grade_gap": f"{gap:+.2f}",
        "reason": (
            f"학생 환산내신 {student_grade:.2f}, 입결 70%컷 {cut_70_grade:.2f}, "
            f"차이 {gap:+.2f}등급입니다."
        ),
    }


def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    data = load_data()

    if name == "list_demo_students":
        rows = [
            f"- {s['student_id']}: {s['display_name']} / 희망전공 {s['target_major']} / "
            f"환산내신 {s['converted_grade']}"
            for s in data["students"]
        ]
        return text_content("공모전용 더미 학생 목록\n" + "\n".join(rows))

    if name == "analyze_admission_fit":
        student = find_student(data, int(arguments["student_id"]))
        cutline = find_cutline(
            data,
            arguments["university"],
            arguments["major"],
            arguments["admission_type"],
        )
        fit = classify_fit(student["converted_grade"], cutline["cut_70_grade"])
        result = {
            "student": student["display_name"],
            "university": cutline["university"],
            "major": cutline["major"],
            "admission_type": cutline["admission_type"],
            "student_grade": student["converted_grade"],
            "cut_70_grade": cutline["cut_70_grade"],
            "competition_rate": cutline["competition_rate"],
            "support_level": fit["support_level"],
            "grade_gap": fit["grade_gap"],
            "reason": fit["reason"],
            "source": cutline["source"],
        }
        return text_content(json.dumps(result, ensure_ascii=False, indent=2))

    if name == "generate_admission_report":
        student = find_student(data, int(arguments["student_id"]))
        cutline = find_cutline(
            data,
            arguments["university"],
            arguments["major"],
            arguments["admission_type"],
        )
        fit = classify_fit(student["converted_grade"], cutline["cut_70_grade"])
        report = f"""# AI 진로진학 상담 보고서 초안

## 학생 개요
- 학생: {student['display_name']}
- 희망 진로: {student['career_goal']}
- 희망 전공: {student['target_major']}
- 주요 활동: {', '.join(student['activities'])}

## 지원 검토
- 대학/학과: {cutline['university']} {cutline['major']}
- 전형: {cutline['admission_type']}
- 학생 환산내신: {student['converted_grade']:.2f}
- 입결 70%컷: {cutline['cut_70_grade']:.2f}
- 경쟁률: {cutline['competition_rate']}
- 지원 판단: {fit['support_level']}
- 판단 근거: {fit['reason']}

## 상담 제안
- {student['next_action']}
- 수능최저, 면접, 학생부 활동의 연결성을 함께 점검해야 합니다.

## 근거
- {cutline['source']}

※ 본 보고서는 공모전 시연용 더미 데이터로 생성되었습니다.
"""
        return text_content(report)

    if name == "recommend_interview_questions":
        student = find_student(data, int(arguments["student_id"]))
        major = arguments["major"]
        questions = [
            f"{major} 지원 동기와 최근 활동을 어떻게 연결할 수 있나요?",
            f"{student['activities'][0]} 활동에서 본인이 주도적으로 해결한 문제는 무엇인가요?",
            "지원 전공에서 가장 중요하다고 생각하는 고등학교 과목과 그 이유는 무엇인가요?",
            "입학 후 1학년 때 보완하고 싶은 학업 역량은 무엇인가요?",
        ]
        return text_content("\n".join(f"{i + 1}. {q}" for i, q in enumerate(questions)))

    raise ValueError(f"지원하지 않는 도구입니다: {name}")


class MCPHandler(BaseHTTPRequestHandler):
    server_version = "IHMContestMCP/0.1"

    def _send_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/health"):
            self._send_json({
                "name": "IHM AI Admission Counseling MCP Server",
                "status": "ok",
                "endpoint": "/mcp",
                "privacy": "demo data only",
            })
            return

        self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        if self.path != "/mcp":
            self._send_json({"error": "not found"}, status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")

        try:
            request = json.loads(raw_body)
            response = self.handle_jsonrpc(request)
        except Exception as exc:
            response = jsonrpc_error(None, -32700, f"요청 파싱 실패: {exc}")

        self._send_json(response)

    def handle_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params") or {}

        if method == "initialize":
            return jsonrpc_result(request_id, {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "ihm-ai-admission-counseling",
                    "version": "0.1.0",
                },
            })

        if method == "tools/list":
            return jsonrpc_result(request_id, {"tools": TOOLS})

        if method == "resources/list":
            return jsonrpc_result(request_id, {"resources": []})

        if method == "prompts/list":
            return jsonrpc_result(request_id, {"prompts": []})

        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments") or {}
            try:
                return jsonrpc_result(request_id, call_tool(tool_name, arguments))
            except Exception as exc:
                return jsonrpc_error(request_id, -32000, str(exc))

        if method == "ping":
            return jsonrpc_result(request_id, {})

        if method == "notifications/initialized":
            return jsonrpc_result(request_id, {})

        return jsonrpc_error(request_id, -32601, f"지원하지 않는 메서드입니다: {method}")

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), MCPHandler)
    print(f"IHM contest MCP server listening on http://{host}:{port}/mcp")
    server.serve_forever()


if __name__ == "__main__":
    main()
