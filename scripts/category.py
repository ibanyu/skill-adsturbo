#!/usr/bin/env python3
"""
Category module — browse content categories.

Subcommands:
  list    List available categories
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
    result = client.post("/internalapi/v1/category/list", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Category — browse categories")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    p = sub.add_parser("list", help="List categories")
    p.add_argument("--params", help="Extra params as JSON")

    args = parser.parse_args()
    {"list": cmd_list}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
