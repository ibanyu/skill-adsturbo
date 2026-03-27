#!/usr/bin/env python3
"""
Workspace module — task results hub.

Subcommands:
  list              Poll task status (轮询状态)
  get               Get task result details (获取结果)
  del               Delete a workspace entry
  share             Share entry to community
  remix             Remix an entry
  prompt-analysis   Analyze entry prompts
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient

ENDPOINTS = {
    "list":            "/internalapi/v1/workspace/list",
    "get":             "/internalapi/v1/workspace/get",
    "del":             "/internalapi/v1/workspace/del",
    "share":           "/internalapi/v1/workspace/share/community",
    "remix":           "/internalapi/v1/workspace/remix",
    "prompt-analysis": "/internalapi/v1/workspace/prompt/analysis",
}


def cmd_list(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.entry_id:
        body["entry_id"] = args.entry_id
    if args.page:
        body["page"] = args.page
    if args.page_size:
        body["page_size"] = args.page_size
    result = client.post(ENDPOINTS["list"], body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_get(args, _parser):
    client = AdsTurboClient()
    result = client.post(ENDPOINTS["get"], {"entry_id": args.entry_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_del(args, _parser):
    client = AdsTurboClient()
    result = client.post(ENDPOINTS["del"], {"entry_id": args.entry_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_share(args, _parser):
    client = AdsTurboClient()
    result = client.post(ENDPOINTS["share"], {"entry_id": args.entry_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_remix(args, _parser):
    client = AdsTurboClient()
    result = client.post(ENDPOINTS["remix"], {"entry_id": args.entry_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_prompt_analysis(args, _parser):
    client = AdsTurboClient()
    body = {"entry_id": args.entry_id}
    result = client.post(ENDPOINTS["prompt-analysis"], body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Workspace — task results hub")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    p = sub.add_parser("list", help="Poll task status / list entries")
    p.add_argument("--entry-id", help="Filter by entry ID")
    p.add_argument("--page", type=int, help="Page number")
    p.add_argument("--page-size", type=int, help="Page size")

    for name in ("get", "del", "share", "remix", "prompt-analysis"):
        p = sub.add_parser(name, help=f"{name} workspace entry")
        p.add_argument("--entry-id", required=True, help="Entry ID")

    args = parser.parse_args()
    handlers = {
        "list": cmd_list, "get": cmd_get, "del": cmd_del,
        "share": cmd_share, "remix": cmd_remix, "prompt-analysis": cmd_prompt_analysis,
    }
    handlers[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
