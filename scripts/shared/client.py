#!/usr/bin/env python3
"""
AdsTurbo API client with Bearer token auth and workspace polling.
"""

from __future__ import annotations

import json
import os
import sys
import time

import requests

DEFAULT_BASE_URL = "https://adsturbo.ai/klian/novartapi"
DEFAULT_POLL_INTERVAL = 5
DEFAULT_POLL_TIMEOUT = 600


class AdsTurboError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class AdsTurboClient:
    """HTTP client for the AdsTurbo internal SaaS API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.environ.get("ADSTURBO_API_KEY", "")
        self.base_url = (base_url or os.environ.get("ADSTURBO_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        if not self.api_key:
            print("Error: ADSTURBO_API_KEY environment variable is not set.", file=sys.stderr)
            sys.exit(1)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def post(self, path: str, json_body: dict | None = None) -> dict:
        """POST JSON request, return parsed response data."""
        resp = self.session.post(self._url(path), json=json_body or {})
        resp.raise_for_status()
        body = resp.json()
        ret = body.get("ret", 0)
        if ret != 1:
            raise AdsTurboError(ret, body.get("msg", "unknown error"))
        data = body.get("data", {})
        return data.get("ent", data) if isinstance(data, dict) else data

    def poll_workspace(
        self,
        entry_id: str,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        interval: float = DEFAULT_POLL_INTERVAL,
        verbose: bool = True,
    ) -> dict:
        """
        Poll workspace/list until the entry reaches a terminal status.
        Returns the entry data when done.
        """
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Polling timed out after {timeout}s for entry {entry_id}")
            if verbose:
                print(f"  Polling workspace (elapsed {elapsed:.0f}s)...", file=sys.stderr)
            try:
                result = self.post("/internalapi/v1/workspace/list", {"entry_id": entry_id})
                entries = result if isinstance(result, list) else result.get("entries", [result])
                for entry in entries:
                    eid = str(entry.get("id", entry.get("entry_id", "")))
                    if eid == str(entry_id):
                        status = entry.get("status", "")
                        if status in ("success", "done", "completed"):
                            if verbose:
                                print(f"  Task completed (status={status}).", file=sys.stderr)
                            return entry
                        if status in ("failed", "error"):
                            raise AdsTurboError(-1, f"Task failed (status={status}): {entry.get('msg', '')}")
            except AdsTurboError:
                raise
            except Exception as e:
                if verbose:
                    print(f"  Poll error: {e}", file=sys.stderr)
            time.sleep(interval)

    def get_workspace_result(self, entry_id: str) -> dict:
        """Get workspace entry result details via workspace/get."""
        return self.post("/internalapi/v1/workspace/get", {"entry_id": entry_id})
