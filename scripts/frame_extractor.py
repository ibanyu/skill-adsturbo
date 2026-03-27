#!/usr/bin/env python3
"""
Frame Extractor module — video frame analysis tasks.

Subcommands:
  run       Submit frame extraction and poll until done
  submit    Submit only
  result    Get task result by task ID
  list      List frame extractor tasks
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_run(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    print("Submitting frame extraction task...", file=sys.stderr)
    result = client.post("/internalapi/v1/frame/submit", body)
    task_id = result.get("task_id", result.get("id", ""))
    if task_id:
        print(f"Task submitted. Task ID: {task_id}", file=sys.stderr)
        # Poll via frame/result endpoint (self-contained polling)
        import time
        start = time.time()
        while time.time() - start < args.timeout:
            res = client.post("/internalapi/v1/frame/result", {"task_id": task_id})
            status = res.get("status", "")
            if status in ("success", "done", "completed"):
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return
            if status in ("failed", "error"):
                print(f"Task failed: {res.get('msg', '')}", file=sys.stderr)
                print(json.dumps(res, indent=2, ensure_ascii=False))
                return
            print(f"  Status: {status}, polling...", file=sys.stderr)
            time.sleep(args.interval)
        print("Timeout reached.", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    result = client.post("/internalapi/v1/frame/submit", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_result(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/frame/result", {"task_id": args.task_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_list(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.page:
        body["page"] = args.page
    result = client.post("/internalapi/v1/frame/list", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def _build_body(args) -> dict:
    body = {}
    if hasattr(args, "video") and args.video:
        body["video"] = args.video
    if hasattr(args, "url") and args.url:
        body["url"] = args.url
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Frame Extractor")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name in ("run", "submit"):
        p = sub.add_parser(name, help=f"{name.capitalize()} frame extraction task")
        p.add_argument("--video", help="Video file/ID")
        p.add_argument("--url", help="Video URL")
        p.add_argument("--params", help="Extra params as JSON")
        p.add_argument("--timeout", type=float, default=300)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("result", help="Get task result")
    p.add_argument("--task-id", required=True)

    p = sub.add_parser("list", help="List tasks")
    p.add_argument("--page", type=int)

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "result": cmd_result, "list": cmd_list}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
