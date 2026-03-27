#!/usr/bin/env python3
"""
Video Generation module — unified video generation API.

Subcommands:
  run       Submit video generation task and poll until done (DEFAULT)
  submit    Submit only, print entry ID and exit
  query     Poll an existing entry ID until done
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
    print("Submitting video generation task...", file=sys.stderr)
    result = client.post("/internalapi/v1/video/generate", body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(f"Task submitted. Entry ID: {entry_id}", file=sys.stderr)
    if entry_id:
        client.poll_workspace(str(entry_id), timeout=args.timeout, interval=args.interval)
        detail = client.get_workspace_result(str(entry_id))
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    result = client.post("/internalapi/v1/video/generate", body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(entry_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    client.poll_workspace(args.entry_id, timeout=args.timeout, interval=args.interval)
    detail = client.get_workspace_result(args.entry_id)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _build_body(args) -> dict:
    body = {}
    for key in ("prompt", "image", "video", "audio", "model", "duration", "aspect_ratio", "mode"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Video Generation")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name, help_text in [("run", "Submit + poll (DEFAULT)"), ("submit", "Submit only")]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--prompt", help="Text prompt for video generation")
        p.add_argument("--image", help="Image file/ID for image-to-video")
        p.add_argument("--video", help="Reference video file/ID")
        p.add_argument("--audio", help="Audio file/ID")
        p.add_argument("--model", help="Model name")
        p.add_argument("--duration", help="Video duration")
        p.add_argument("--aspect-ratio", help="Aspect ratio")
        p.add_argument("--mode", help="Generation mode")
        p.add_argument("--timeout", type=float, default=600, help="Polling timeout (default: 600)")
        p.add_argument("--interval", type=float, default=5, help="Polling interval (default: 5)")

    p = sub.add_parser("query", help="Poll existing entry ID")
    p.add_argument("--entry-id", required=True, help="Entry ID to poll")
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
