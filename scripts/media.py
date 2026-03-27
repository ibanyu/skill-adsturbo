#!/usr/bin/env python3
"""
Media module — video cutting and batch fetch.

Subcommands:
  cut-video     Cut/trim a video
  batch-fetch   Batch fetch original videos from URLs
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient


def cmd_cut_video(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.video:
        body["video"] = args.video
    if args.start:
        body["start"] = args.start
    if args.end:
        body["end"] = args.end
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    result = client.post("/internalapi/v1/media/cut_video", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_batch_fetch(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.urls:
        body["urls"] = args.urls.split(",")
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    result = client.post("/internalapi/v1/video/batch_fetch", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Media Tools")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    p = sub.add_parser("cut-video", help="Cut/trim a video")
    p.add_argument("--video", help="Video file/ID")
    p.add_argument("--start", help="Start time")
    p.add_argument("--end", help="End time")
    p.add_argument("--params", help="Extra params as JSON")

    p = sub.add_parser("batch-fetch", help="Batch fetch videos from URLs")
    p.add_argument("--urls", help="Comma-separated video URLs")
    p.add_argument("--params", help="Extra params as JSON")

    args = parser.parse_args()
    {"cut-video": cmd_cut_video, "batch-fetch": cmd_batch_fetch}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
