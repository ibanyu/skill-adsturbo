#!/usr/bin/env python3
"""
Storage module — file upload utilities.

Subcommands:
  upload        Upload a general file
  upload-pic    Upload an image file
  upload-audio  Upload an audio file (no transcoding)
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.upload import upload_file


def cmd_upload(args, _parser):
    api_key = os.environ.get("ADSTURBO_API_KEY", "")
    base_url = os.environ.get("ADSTURBO_BASE_URL", "https://adsturbo.ai/klian/novartapi")
    result = upload_file(base_url, api_key, args.file, "once")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_upload_pic(args, _parser):
    api_key = os.environ.get("ADSTURBO_API_KEY", "")
    base_url = os.environ.get("ADSTURBO_BASE_URL", "https://adsturbo.ai/klian/novartapi")
    result = upload_file(base_url, api_key, args.file, "pic")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_upload_audio(args, _parser):
    api_key = os.environ.get("ADSTURBO_API_KEY", "")
    base_url = os.environ.get("ADSTURBO_BASE_URL", "https://adsturbo.ai/klian/novartapi")
    result = upload_file(base_url, api_key, args.file, "audio")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo Storage — file uploads")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    for name, help_text, handler in [
        ("upload", "Upload a general file", cmd_upload),
        ("upload-pic", "Upload an image file", cmd_upload_pic),
        ("upload-audio", "Upload an audio file", cmd_upload_audio),
    ]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--file", required=True, help="Local file path to upload")

    args = parser.parse_args()
    {"upload": cmd_upload, "upload-pic": cmd_upload_pic, "upload-audio": cmd_upload_audio}[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
