#!/usr/bin/env python3
"""
AI Actor module — manage and use AI digital humans.

Subcommands:
  list              List available AI actors
  favourite         Favourite/unfavourite an AI actor
  perform           Generate a talking-head video with an AI actor
  enhance           Enhance emotion in actor performance
  say               Generate TTS audio with an actor's voice
  asr               Speech-to-text transcription
  user-submit       Create a custom user actor
  user-voice        Generate voice for a custom actor
  user-perform      Perform with a custom actor
  user-detail       Get custom actor details
  user-clone-voice  Clone a voice for a custom actor
  user-del          Delete a custom actor
  user-img          Create custom actor image
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared.client import AdsTurboClient, AdsTurboError


def cmd_list(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/aiactor/list", {})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_favourite(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/aiactor/favourite", {"actor_id": args.actor_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_perform(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id}
    if args.text:
        body["text"] = args.text
    if args.audio:
        body["audio"] = args.audio
    result = client.post("/internalapi/v1/aiactor/perform", body)
    if not args.json:
        entry_id = result.get("entry_id", result.get("id", ""))
        print(f"Task submitted. Entry ID: {entry_id}", file=sys.stderr)
        if entry_id and not args.submit_only:
            final = client.poll_workspace(str(entry_id), timeout=args.timeout, interval=args.interval)
            detail = client.get_workspace_result(str(entry_id))
            print(json.dumps(detail, indent=2, ensure_ascii=False))
            return
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_enhance(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/aiactor/enhance", {"text": args.text})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_say(args, _parser):
    client = AdsTurboClient()
    body = {"text": args.text}
    if args.voice_id:
        body["voice_id"] = args.voice_id
    result = client.post("/internalapi/v1/aiactor/say", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_asr(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/aiactor/asr", {"audio": args.audio})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_submit(args, _parser):
    client = AdsTurboClient()
    body = {}
    if args.name:
        body["name"] = args.name
    if args.image:
        body["image"] = args.image
    result = client.post("/internalapi/v1/useractor/submit", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_voice(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id}
    result = client.post("/internalapi/v1/useractor/generate/voice", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_perform(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id}
    if args.text:
        body["text"] = args.text
    result = client.post("/internalapi/v1/useractor/perform", body)
    if not args.json:
        entry_id = result.get("entry_id", result.get("id", ""))
        if entry_id and not args.submit_only:
            print(f"Task submitted. Entry ID: {entry_id}", file=sys.stderr)
            client.poll_workspace(str(entry_id), timeout=args.timeout, interval=args.interval)
            detail = client.get_workspace_result(str(entry_id))
            print(json.dumps(detail, indent=2, ensure_ascii=False))
            return
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_detail(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/useractor/detail", {"actor_id": args.actor_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_clone_voice(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id}
    if args.audio:
        body["audio"] = args.audio
    result = client.post("/internalapi/v1/useractor/clone/voice", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_del(args, _parser):
    client = AdsTurboClient()
    result = client.post("/internalapi/v1/useractor/del", {"actor_id": args.actor_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_img(args, _parser):
    client = AdsTurboClient()
    body = {"actor_id": args.actor_id}
    result = client.post("/internalapi/v1/useractor/image/creation", body)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def add_poll_args(p):
    p.add_argument("--timeout", type=float, default=600, help="Max polling time in seconds (default: 600)")
    p.add_argument("--interval", type=float, default=5, help="Polling interval in seconds (default: 5)")


def add_output_args(p):
    p.add_argument("--json", action="store_true", help="Output full JSON response")
    p.add_argument("--submit-only", action="store_true", help="Submit only, don't poll")


def main():
    parser = argparse.ArgumentParser(description="AdsTurbo AI Actor module")
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # list
    sub.add_parser("list", help="List available AI actors")

    # favourite
    p = sub.add_parser("favourite", help="Favourite/unfavourite an AI actor")
    p.add_argument("--actor-id", required=True, help="Actor ID")

    # perform
    p = sub.add_parser("perform", help="Generate talking-head video with AI actor")
    p.add_argument("--actor-id", required=True, help="Actor ID")
    p.add_argument("--text", help="Text for the actor to speak")
    p.add_argument("--audio", help="Audio file/ID for audio-driven mode")
    add_poll_args(p)
    add_output_args(p)

    # enhance
    p = sub.add_parser("enhance", help="Enhance emotion in text")
    p.add_argument("--text", required=True, help="Text to enhance")

    # say
    p = sub.add_parser("say", help="Generate TTS audio")
    p.add_argument("--text", required=True, help="Text to speak")
    p.add_argument("--voice-id", help="Voice ID")

    # asr
    p = sub.add_parser("asr", help="Speech-to-text")
    p.add_argument("--audio", required=True, help="Audio file/ID")

    # user-submit
    p = sub.add_parser("user-submit", help="Create a custom user actor")
    p.add_argument("--name", help="Actor name")
    p.add_argument("--image", help="Image file/ID")

    # user-voice
    p = sub.add_parser("user-voice", help="Generate voice for custom actor")
    p.add_argument("--actor-id", required=True, help="Actor ID")

    # user-perform
    p = sub.add_parser("user-perform", help="Perform with custom actor")
    p.add_argument("--actor-id", required=True, help="Actor ID")
    p.add_argument("--text", help="Text for the actor to speak")
    add_poll_args(p)
    add_output_args(p)

    # user-detail
    p = sub.add_parser("user-detail", help="Get custom actor details")
    p.add_argument("--actor-id", required=True, help="Actor ID")

    # user-clone-voice
    p = sub.add_parser("user-clone-voice", help="Clone a voice for custom actor")
    p.add_argument("--actor-id", required=True, help="Actor ID")
    p.add_argument("--audio", help="Audio sample for cloning")

    # user-del
    p = sub.add_parser("user-del", help="Delete a custom actor")
    p.add_argument("--actor-id", required=True, help="Actor ID")

    # user-img
    p = sub.add_parser("user-img", help="Create custom actor image")
    p.add_argument("--actor-id", required=True, help="Actor ID")

    args = parser.parse_args()
    handlers = {
        "list": cmd_list, "favourite": cmd_favourite, "perform": cmd_perform,
        "enhance": cmd_enhance, "say": cmd_say, "asr": cmd_asr,
        "user-submit": cmd_user_submit, "user-voice": cmd_user_voice,
        "user-perform": cmd_user_perform, "user-detail": cmd_user_detail,
        "user-clone-voice": cmd_user_clone_voice, "user-del": cmd_user_del,
        "user-img": cmd_user_img,
    }
    handlers[args.subcommand](args, parser)


if __name__ == "__main__":
    main()
