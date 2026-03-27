#!/usr/bin/env python3
"""
User & Billing module — user info, credits, and billing.

Subcommands:
  info       Get user info
  credit     Get credit history
  billing    Get billing history
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_info(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/user", {})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_credit(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.page:
        body["page"] = args.page
    result = client.post("/internalapi/v1/credit/history", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_billing(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.page:
        body["page"] = args.page
    result = client.post("/internalapi/v1/billing/history", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo User & Billing")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    sub.add_parser("info", help="Get user info")

    p = sub.add_parser("credit", help="Get credit history")
    p.add_argument("--page", type=int, help="Page number")

    p = sub.add_parser("billing", help="Get billing history")
    p.add_argument("--page", type=int, help="Page number")

    args = parser.parse_args()
    {"info": cmd_info, "credit": cmd_credit, "billing": cmd_billing}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
