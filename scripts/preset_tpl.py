#!/usr/bin/env python3
"""
Preset Template module — browse and use preset video templates.

Subcommands:
  list    List preset templates
  run     Submit preset template video generation and poll
  submit  Submit only
  query   Poll existing entry ID
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_list(args, _parser):
    client = AdsTurboClient()
    body = {}
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    result = client.post("/internalapi/v1/preset_tpl/list", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_run(args, _parser):
    client = AdsTurboClient()
    body = _build_body(args)
    print("Submitting preset template video task...", file=sys.stderr)
    result = client.post("/internalapi/v1/preset_tpl/gen_video/submit", body)
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
    result = client.post("/internalapi/v1/preset_tpl/gen_video/submit", body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(entry_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    client.poll_workspace(args.entry_id, timeout=args.timeout, interval=args.interval)
    detail = client.get_workspace_result(args.entry_id)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _build_body(args) -> dict:
    body = {}
    if args.template_id:
        body["template_id"] = args.template_id
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Preset Templates")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    p = sub.add_parser("list", help="List preset templates")
    p.add_argument("--params", help="Extra params as JSON")

    for name in ("run", "submit"):
        p = sub.add_parser(name, help=f"{name.capitalize()} preset template video task")
        p.add_argument("--template-id", required=True, help="Template ID")
        p.add_argument("--params", help="Extra params as JSON")
        p.add_argument("--timeout", type=float, default=600)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("query", help="Poll existing entry ID")
    p.add_argument("--entry-id", required=True)
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"list": cmd_list, "run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
