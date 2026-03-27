#!/usr/bin/env python3
"""
Ads Data module — browse ad performance data.

Subcommands:
  list    List ads
  get     Get ad details
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
    if args.page:
        body["page"] = args.page
    if args.page_size:
        body["page_size"] = args.page_size
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    result = client.post("/internalapi/v1/ads/list", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_get(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/ads/get", {"ad_id": args.ad_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Ads Data")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    p = sub.add_parser("list", help="List ads")
    p.add_argument("--page", type=int)
    p.add_argument("--page-size", type=int)
    p.add_argument("--params", help="Extra params as JSON")

    p = sub.add_parser("get", help="Get ad details")
    p.add_argument("--ad-id", required=True, help="Ad ID")

    args = parser.parse_args()
    {"list": cmd_list, "get": cmd_get}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
