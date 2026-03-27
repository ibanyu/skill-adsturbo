#!/usr/bin/env python3
"""
TikTok Analytics module — analyze TikTok creators and videos.

Subcommands:
  creator     Get creator info and milestones
  comments    Analyze video comments
  detect      Detect fake views on a video
  metrics     Get video metrics/performance data
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient

ENDPOINTS = {
    "creator":  "/internalapi/v1/tt/analytics/creator",
    "comments": "/internalapi/v1/tt/analytics/video/comments",
    "detect":   "/internalapi/v1/tt/analytics/video/detect",
    "metrics":  "/internalapi/v1/tt/analytics/video/metrics",
}


def cmd_generic(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.url:
        body["url"] = args.url
    if args.video_id:
        body["video_id"] = args.video_id
    if args.creator_id:
        body["creator_id"] = args.creator_id
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    result = client.post(ENDPOINTS[args.subcommand], body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo TikTok Analytics")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name, help_text in [
        ("creator", "Get creator info and milestones"),
        ("comments", "Analyze video comments"),
        ("detect", "Detect fake views"),
        ("metrics", "Get video metrics"),
    ]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--url", help="TikTok video/creator URL")
        p.add_argument("--video-id", help="TikTok video ID")
        p.add_argument("--creator-id", help="TikTok creator ID")
        p.add_argument("--params", help="Extra params as JSON string")

    args = parser.parse_args()
    cmd_generic(args, parser)


if __name__ == "__main__":
    main()
