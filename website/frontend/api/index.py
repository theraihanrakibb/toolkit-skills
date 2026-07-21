"""Vercel Python serverless entrypoint for Toolkit Skills.

Routes POST /api (with {"action": ...} in the body) to the skill logic in
skills.py. No external dependencies - pure standard library.
"""

import json

from skills import dispatch


def handler(request):
    # Vercel's Python Request exposes .json() (returns a dict) or .body (bytes).
    try:
        if hasattr(request, "json"):
            try:
                body = request.json()
            except Exception:  # noqa: BLE001
                body = {}
        else:
            body = json.loads((request.body or b"{}").decode("utf-8"))
    except Exception:  # noqa: BLE001
        body = {}

    if not isinstance(body, dict):
        body = {}

    action = body.get("action")
    try:
        result = dispatch(action, body)
        return 200, {"Content-Type": "application/json"}, json.dumps(result)
    except Exception as e:  # noqa: BLE001
        return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)})
