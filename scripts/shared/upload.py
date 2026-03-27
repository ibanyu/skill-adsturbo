#!/usr/bin/env python3
"""
File upload helpers for AdsTurbo internal SaaS API.
Handles multipart file uploads for various media types.
"""

from __future__ import annotations

import os
import sys

import requests


def upload_file(base_url: str, api_key: str, file_path: str, upload_type: str = "once") -> dict:
    """
    Upload a file to AdsTurbo storage.

    Args:
        base_url: API base URL
        api_key: Bearer token
        file_path: Local file path to upload
        upload_type: "once" | "pic" | "audio"
    """
    endpoint_map = {
        "once": "/internalapi/v1/storage/upload/once",
        "pic": "/internalapi/v1/storage/upload/once/pic",
        "audio": "/internalapi/v1/storage/upload/onceaudio/notrans",
    }
    endpoint = endpoint_map.get(upload_type, endpoint_map["once"])
    url = f"{base_url.rstrip('/')}{endpoint}"

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (filename, f)},
        )
    resp.raise_for_status()
    body = resp.json()
    ret = body.get("ret", 0)
    if ret != 1:
        raise RuntimeError(f"Upload failed [{ret}]: {body.get('msg', 'unknown error')}")
    data = body.get("data", {})
    return data.get("ent", data) if isinstance(data, dict) else data


def resolve_local_file(
    file_id_or_path: str,
    upload_type: str = "once",
    api_key: str | None = None,
    base_url: str | None = None,
    quiet: bool = False,
) -> str:
    """
    If the argument looks like a local file path (exists on disk), upload it
    and return the resulting file ID. Otherwise return it as-is (assumed to
    be an existing file ID).
    """
    if not os.path.exists(file_id_or_path):
        return file_id_or_path

    _api_key = api_key or os.environ.get("ADSTURBO_API_KEY", "")
    _base_url = (base_url or os.environ.get("ADSTURBO_BASE_URL", "https://adsturbo.ai/klian/novartapi")).rstrip("/")

    if not quiet:
        print(f"Uploading {file_id_or_path}...", file=sys.stderr)

    result = upload_file(_base_url, _api_key, file_id_or_path, upload_type)
    file_id = result.get("file_id", result.get("id", ""))
    if not file_id:
        file_id = str(result)

    if not quiet:
        print(f"Uploaded. File ID: {file_id}", file=sys.stderr)
    return file_id
