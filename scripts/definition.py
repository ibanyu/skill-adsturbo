#!/usr/bin/env python3
"""
Definition module — video resolution enhancement and avatar performance.

Subcommands:
  run          Submit resolution enhancement and poll until done
  submit       Submit only
  query        Poll existing entry ID
  performance  Get avatar performance data
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
    print("Submitting resolution enhancement task...", file=sys.stderr)
    result = client.post("/internalapi/v1/definition/submit", body)
    entry_id = result.get("entry_id", result.get("id", ""))
    if entry_id:
        print(f"Task submitted. Entry ID: {entry_id}", file=sys.stderr)
        client.poll_workspace(str(entry_id), timeout=args.timeout, interval=args.interval)
        detail = client.get_workspace_result(str(entry_id))
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    result = client.post("/internalapi/v1/definition/submit", body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(entry_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    client.poll_workspace(args.entry_id, timeout=args.timeout, interval=args.interval)
    detail = client.get_workspace_result(args.entry_id)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def cmd_performance(args, _parser):
    client = AdsTurboClient()
    body = {}
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    result = client.post("/internalapi/v1/definition/performance", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def _build_body(args) -> dict:
    body = {}
    if hasattr(args, "video") and args.video:
        body["video"] = args.video
    if hasattr(args, "definition") and args.definition:
        body["definition"] = args.definition
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Definition — resolution enhancement")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name in ("run", "submit"):
        p = sub.add_parser(name, help=f"{name.capitalize()} resolution enhancement task")
        p.add_argument("--video", help="Video file/ID")
        p.add_argument("--definition", help="Target definition")
        p.add_argument("--params", help="Extra params as JSON")
        p.add_argument("--timeout", type=float, default=600)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("query", help="Poll existing entry ID")
    p.add_argument("--entry-id", required=True)
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("performance", help="Get avatar performance data")
    p.add_argument("--params", help="Extra params as JSON")

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "query": cmd_query, "performance": cmd_performance}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
