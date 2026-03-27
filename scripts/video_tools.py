#!/usr/bin/env python3
"""
Video Tools module — video processing utilities.

Subcommands:
  lipsync          Submit lip-sync task
  inpainting       Submit watermark removal task
  face-swap        Submit face swap task
  translate        Submit video translation task
  super-resolve-4k Submit 4K super resolve task
  character-swap   Submit character swap task
  motion-control   Submit motion control task

All subcommands support: run (submit + poll), submit (fire-and-forget), query (resume polling).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient

TOOLS = {
    "lipsync":          "/internalapi/v1/lipsync/submit",
    "inpainting":       "/internalapi/v1/videoinpainting/submit",
    "face-swap":        "/internalapi/v1/videofaceswap/submit",
    "translate":        "/internalapi/v1/videotranslate/submit",
    "super-resolve-4k": "/internalapi/v1/videosuperresolve4k/submit",
    "character-swap":   "/internalapi/v1/videocharacterswap/submit",
    "motion-control":   "/internalapi/v1/videomotioncontrol/submit",
}


def cmd_run(args, _parser):
    client = AdsTurboClient()
    endpoint = TOOLS[args.tool]
    body = _collect_params(args)
    print(f"Submitting {args.tool} task...", file=sys.stderr)
    result = client.post(endpoint, body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(f"Task submitted. Entry ID: {entry_id}", file=sys.stderr)
    if entry_id:
        client.poll_workspace(str(entry_id), timeout=args.timeout, interval=args.interval)
        detail = client.get_workspace_result(str(entry_id))
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_submit(args, _parser):
    client = AdsTurboClient()
    endpoint = TOOLS[args.tool]
    body = _collect_params(args)
    result = client.post(endpoint, body)
    entry_id = result.get("entry_id", result.get("id", ""))
    print(entry_id or json.dumps(result, indent=2, ensure_ascii=False))


def cmd_query(args, _parser):
    client = AdsTurboClient()
    client.poll_workspace(args.entry_id, timeout=args.timeout, interval=args.interval)
    detail = client.get_workspace_result(args.entry_id)
    print(json.dumps(detail, indent=2, ensure_ascii=False))


def _collect_params(args) -> dict:
    body = {}
    for key in ("video", "audio", "image", "text", "source_lang", "target_lang", "face_image"):
        val = getattr(args, key, None)
        if val is not None:
            body[key] = val
    if hasattr(args, "params") and args.params:
        body.update(json.loads(args.params))
    return body


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Video Tools")
    sub = parser.add_subparsers(dest="action")
    sub.required = True

    for action in ("run", "submit"):
        p = sub.add_parser(action, help=f"{action.capitalize()} a video tool task")
        p.add_argument("tool", choices=list(TOOLS.keys()), help="Which tool to use")
        p.add_argument("--video", help="Video file/ID")
        p.add_argument("--audio", help="Audio file/ID")
        p.add_argument("--image", help="Image file/ID")
        p.add_argument("--text", help="Text input")
        p.add_argument("--face-image", help="Face image for swap")
        p.add_argument("--source-lang", help="Source language (for translate)")
        p.add_argument("--target-lang", help="Target language (for translate)")
        p.add_argument("--params", help="Extra params as JSON string")
        p.add_argument("--timeout", type=float, default=600)
        p.add_argument("--interval", type=float, default=5)

    p = sub.add_parser("query", help="Poll existing entry ID")
    p.add_argument("--entry-id", required=True)
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=5)

    args = parser.parse_args()
    {"run": cmd_run, "submit": cmd_submit, "query": cmd_query}[args.action](args, parser)


if __name__ == "__main__":
    main()
