#!/usr/bin/env python3
"""
URL2Video module — turn a product URL into a marketing video.

Subcommands:
  scrape                  Scrape product info from URL
  get-metadata            Get metadata
  gen-scripts             Generate video scripts from product info
  get-avatars             Get available avatars
  get-recommend-avatars   Get recommended avatars
  submit-previews         Submit preview generation task
  get-previews            Get preview task result
  submit-render           Submit single video render task
  get-render              Get render task result
  submit-renders          Submit batch video render tasks
  get-renders             Get batch render results
  get-render-list         Get render task list
  get                     Get flow product video info
  update                  Update flow product video info
  get-step-status         Get workflow current step status
  update-op-meta          Update Novart OP metadata
  execute-op-task         Execute Novart OP task
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient

ENDPOINTS = {
    "scrape":             "/internalapi/v1/url2video/scrape",
    "get-metadata":       "/internalapi/v1/url2video/get_metadata",
    "gen-scripts":        "/internalapi/v1/url2video/gen_video_scripts",
    "get-avatars":        "/internalapi/v1/url2video/get_avatars",
    "get-recommend-avatars": "/internalapi/v1/url2video/get_recommend_avatars",
    "submit-previews":    "/internalapi/v1/url2video/submit_gen_previews_task",
    "get-previews":       "/internalapi/v1/url2video/get_gen_previews_task_result",
    "submit-render":      "/internalapi/v1/url2video/submit_render_video_task",
    "get-render":         "/internalapi/v1/url2video/get_render_video_task_result",
    "submit-renders":     "/internalapi/v1/url2video/submit_render_videos_task",
    "get-renders":        "/internalapi/v1/url2video/get_render_videos_task_results",
    "get-render-list":    "/internalapi/v1/url2video/get_render_video_task_list",
    "get":                "/internalapi/v1/url2video/get",
    "update":             "/internalapi/v1/url2video/update",
    "get-step-status":    "/internalapi/v1/url2video/get_flow_cur_step_status",
    "update-op-meta":     "/internalapi/v1/url2video/update_novart_op_meta",
    "execute-op-task":    "/internalapi/v1/url2video/execute_novart_op_task",
}


def generic_cmd(args, _parser):
    client = AdsTurboClient()
    body = {}
    if hasattr(args, "params") and args.params:
        body = json.loads(args.params)
    for key in ("url", "flow_id", "task_id", "product_id"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    result = client.post(ENDPOINTS[args.subcommand], body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo URL2Video — product URL to marketing video")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name, help_text in [
        ("scrape", "Scrape product info from URL"),
        ("get-metadata", "Get metadata"),
        ("gen-scripts", "Generate video scripts"),
        ("get-avatars", "Get available avatars"),
        ("get-recommend-avatars", "Get recommended avatars"),
        ("submit-previews", "Submit preview generation"),
        ("get-previews", "Get preview results"),
        ("submit-render", "Submit single render task"),
        ("get-render", "Get render task result"),
        ("submit-renders", "Submit batch render tasks"),
        ("get-renders", "Get batch render results"),
        ("get-render-list", "Get render task list"),
        ("get", "Get flow product video info"),
        ("update", "Update flow product video info"),
        ("get-step-status", "Get workflow step status"),
        ("update-op-meta", "Update OP metadata"),
        ("execute-op-task", "Execute OP task"),
    ]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--url", help="Product URL (for scrape)")
        p.add_argument("--flow-id", help="Flow ID")
        p.add_argument("--task-id", help="Task ID")
        p.add_argument("--product-id", help="Product ID")
        p.add_argument("--params", help="Extra params as JSON string")

    args = parser.parse_args()
    generic_cmd(args, parser)


if __name__ == "__main__":
    main()
