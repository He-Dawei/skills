#!/usr/bin/env python3
"""Submit a Pixelle-Video async task and poll it to completion."""

from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def request_json(method: str, url: str, payload: dict | None = None, timeout: float = 30) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(url, data=body, method=method)
    request.add_header("Accept", "application/json")
    if body is not None:
        request.add_header("Content-Type", "application/json")

    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Cannot reach {url}: {exc.reason}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a video with the local Pixelle-Video API")
    parser.add_argument("--text", required=True, help="Video source text")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--timeout", type=float, default=600, help="Total polling timeout in seconds")
    parser.add_argument("--poll-interval", type=float, default=5)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    payload = {
        "text": args.text,
        "mode": "generate",
        "n_scenes": 5,
        "frame_template": "1080x1920/image_default.html",
        "video_fps": 30,
        "bgm_volume": 0.3,
    }

    created = request_json("POST", f"{base_url}/api/video/generate/async", payload)
    task_id = created.get("task_id")
    if not task_id:
        raise RuntimeError(f"Pixelle-Video response has no task_id: {created}")

    print(f"task_id={task_id}", flush=True)
    deadline = time.monotonic() + args.timeout
    last_status = None

    while time.monotonic() < deadline:
        task = request_json("GET", f"{base_url}/api/tasks/{quote(str(task_id), safe='')}")
        status = str(task.get("status", "")).lower()
        if status != last_status:
            print(f"status={status or 'unknown'}", file=sys.stderr, flush=True)
            last_status = status

        if status == "completed":
            print(json.dumps(task, ensure_ascii=False, indent=2))
            return 0
        if status in {"failed", "cancelled"}:
            raise RuntimeError(f"Pixelle-Video task {status}: {task.get('error') or task}")

        time.sleep(args.poll_interval)

    raise TimeoutError(f"Pixelle-Video task {task_id} did not complete within {args.timeout:g}s")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, TimeoutError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
