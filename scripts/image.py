#!/usr/bin/env python3
"""
Image module — AI image creation.

Subcommands:
  run       Submit image creation task and poll until done (DEFAULT)
  submit    Submit only, print entry ID
  query     Poll an existing entry ID
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
    print("Submitting image creation task...", file=sys.stderr)
    result = client.post("/internalapi/v1/img/create", body)
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
    result = client.post("/internalapi/v1/img/create", body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(entry_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    client.poll_workspace(args.entry_id, timeout=args.timeout, interval=args.interval)
    detail = client.get_workspace_result(args.entry_id)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _build_body(args) -> dict:
    body = {}
    for key in ("prompt", "image", "model", "aspect_ratio", "resolution", "style"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Image Creation")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name in ("run", "submit"):
        p = sub.add_parser(name, help=f"{name.capitalize()} image creation task")
        p.add_argument("--prompt", help="Image prompt")
        p.add_argument("--image", help="Reference image file/ID")
        p.add_argument("--model", help="Model name")
        p.add_argument("--aspect-ratio", help="Aspect ratio")
        p.add_argument("--resolution", help="Resolution")
        p.add_argument("--style", help="Style")
        p.add_argument("--timeout", type=float, default=300)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("query", help="Poll existing entry ID")
    p.add_argument("--entry-id", required=True)
    p.add_argument("--timeout", type=float, default=300)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
