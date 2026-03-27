---
name: adsturbo-skill
description: "AI-powered video creation platform for advertising. Generate videos with AI actors, translate, face-swap, lip-sync, and more — all via simple commands."
metadata:
  tags: adsturbo, video, ai-actor, tiktok, ads, lip-sync, face-swap, translate, url2video, image
requires:
  bins: [python3]
primaryEnv: ADSTURBO_API_KEY
---

# AdsTurbo AI Skill

> Modular Python toolkit for the [AdsTurbo.ai](https://adsturbo.ai) API.

- AI Actor: Create talking-head videos with AI digital humans or your own custom avatars
- Video Generation: Generate videos from text/image/reference with the unified generate API
- URL2Video: Turn any product URL into a marketing video automatically
- Video Tools: Lip-sync, face-swap, translate, watermark removal, 4K upscale, motion control
- TikTok Analytics: Analyze creators, video comments, fake views, and metrics
- Image Creation: AI-powered image generation

## Execution Rule

> **Always use the Python scripts in `scripts/`. Do NOT use `curl` or direct HTTP calls.**

## User-Facing Reply Rules

1. **Keep replies short** — give the result or next step directly.
2. **Use plain language** — no API jargon, no terminal references, no JSON/script mentions.
3. **Never mention terminal details** — no command output, logs, exit codes, or file paths.
4. **Be result-oriented** — after task completion, give the user the result (link, video URL) directly.
5. **Explain errors simply** — one sentence about what happened, ask if they want to retry.
6. **Give time estimates** — after submitting a task, tell the user the estimated wait time.

**Estimated Generation Time**

| Task Type | Estimated Time |
|-----------|---------------|
| AI Actor Perform | ~2-5 min |
| Video Generate | ~3-10 min |
| URL2Video Render | ~5-15 min |
| Lip Sync | ~2-5 min |
| Video Face Swap | ~3-5 min |
| Video Translate | ~5-10 min |
| Video Inpainting (Watermark Removal) | ~2-5 min |
| Super Resolve / 4K | ~3-5 min |
| Image Create | ~30s-1 min |
| Frame Extractor | ~1-3 min |

## Prerequisites

- **Python 3.8+**
- **ADSTURBO_API_KEY** — Bearer token for API authentication
- Optional: **ADSTURBO_BASE_URL** (defaults to `https://adsturbo.ai/klian/novartapi`)

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## Agent Workflow Rules

> **These rules apply to ALL async task modules.**

1. **Async task pattern**: Most tasks follow submit → poll → get result.
   - Submit a task via the module's `run` or `submit` subcommand
   - Poll status via `workspace/list` (the workspace module)
   - Get result details via `workspace/get`
2. **Always start with `run`** — it submits the task and polls automatically until done.
3. **Only use `submit`** for batch jobs where you want to fire-and-forget, then poll separately.
4. **Only use `query`** when `run` timed out and you have an entry ID to resume polling.
5. **If `query` times out**, increase `--timeout` and try again. Do not resubmit unless the task actually failed.

```
Decision tree:
→ New request?       use `run`
→ run timed out?     use `query --entry-id <id>`
→ query timed out?   use `query --entry-id <id> --timeout 1200`
→ task failed?       resubmit with `run`
```

## Modules

| Module | Script | Reference | Description |
|--------|--------|-----------|-------------|
| AI Actor | `scripts/ai_actor.py` | [ai_actor.md](references/ai_actor.md) | AI digital humans: list, perform, enhance emotion, TTS, ASR, custom actor management |
| URL2Video | `scripts/url2video.py` | [url2video.md](references/url2video.md) | Product URL → marketing video: scrape, generate scripts, preview, render |
| Workspace | `scripts/workspace.py` | [workspace.md](references/workspace.md) | Task results hub: poll status (list), get result (get), delete, share, remix |
| TikTok Analytics | `scripts/tiktok_analytics.py` | [tiktok_analytics.md](references/tiktok_analytics.md) | TikTok data: creator info, comment analysis, fake view detection, video metrics |
| Video Tools | `scripts/video_tools.py` | [video_tools.md](references/video_tools.md) | Video processing: lip-sync, inpainting, face-swap, translate, 4K, character-swap, motion-control |
| Video Gen | `scripts/video_gen.py` | [video_gen.md](references/video_gen.md) | Unified video generation from text/image/reference |
| Image | `scripts/image.py` | [image.md](references/image.md) | AI image creation |
| Frame Extractor | `scripts/frame_extractor.py` | [frame_extractor.md](references/frame_extractor.md) | Video frame analysis: submit task, get result, list tasks |
| Ads Data | `scripts/ads_data.py` | [ads_data.md](references/ads_data.md) | Ad performance data: list ads, get ad details |
| Preset Template | `scripts/preset_tpl.py` | [preset_tpl.md](references/preset_tpl.md) | Preset video templates: browse and generate videos from templates |
| Definition | `scripts/definition.py` | [definition.md](references/definition.md) | Video resolution enhancement and avatar performance |
| User & Billing | `scripts/user.py` | [user.md](references/user.md) | User info, credit history, billing history |
| Media | `scripts/media.py` | [media.md](references/media.md) | Media tools: cut video, batch fetch videos |
| Storage | `scripts/storage.py` | [storage.md](references/storage.md) | File upload: general files, images, audio |
| Category | `scripts/category.py` | [category.md](references/category.md) | Browse content categories |

> **Read individual reference docs for usage, options, and examples.**

---

## Creative Guide

> **Core Principle:** Start from the user's intent, not from the API.

### Step 1 — Intent Analysis

| Dimension | Ask Yourself | Fallback |
|-----------|-------------|----------|
| **Output Type** | Video? Image? Audio? Analytics? | Must ask |
| **Purpose** | Marketing ad? Social media? Product demo? | General marketing |
| **Source Material** | Has URL? Has image/video? Has script? | Must ask |
| **Style / Tone** | Professional? Casual? Dynamic? | Professional |

### Step 2 — Tool Selection

```
What does the user need?
│
├─ Turn a product URL into a video ad?
│  → url2video (full workflow: scrape → scripts → preview → render)
│
├─ A digital human / AI actor speaking to camera?
│  → ai_actor perform (with existing actor)
│  → ai_actor user-perform (with custom actor)
│
├─ Generate a video from text/image/reference?
│  → video_gen run
│
├─ Generate an AI image?
│  → image run
│
├─ Lip-sync a video to new audio?
│  → video_tools lipsync
│
├─ Remove watermark from a video?
│  → video_tools inpainting
│
├─ Swap faces in a video?
│  → video_tools face-swap or character-swap
│
├─ Translate a video to another language?
│  → video_tools translate
│
├─ Upscale video to higher resolution / 4K?
│  → video_tools super-resolve-4k or definition submit
│
├─ Control motion in a video?
│  → video_tools motion-control
│
├─ Analyze TikTok creator or video data?
│  → tiktok_analytics (creator/comments/detect/metrics)
│
├─ Analyze video frames?
│  → frame_extractor
│
├─ Browse ad performance data?
│  → ads_data
│
├─ Use a preset template to generate video?
│  → preset_tpl
│
├─ Check task status or results?
│  → workspace list (poll) or workspace get (result)
│
├─ Upload a file?
│  → storage upload
│
├─ Check credits / billing?
│  → user credit or user billing
│
└─ Browse available categories?
   → category list
```

---

## Capability Boundaries

| Capability | Status | Script |
|---------------------------------|-----------|-----|
| AI Actor — list/perform/enhance | Available | `scripts/ai_actor.py` |
| AI Actor — custom actor CRUD | Available | `scripts/ai_actor.py` |
| AI Actor — voice clone/TTS/ASR | Available | `scripts/ai_actor.py` |
| Video Generation (unified) | Available | `scripts/video_gen.py` |
| URL-to-Video workflow | Available | `scripts/url2video.py` |
| Lip Sync | Available | `scripts/video_tools.py lipsync` |
| Video Inpainting (watermark) | Available | `scripts/video_tools.py inpainting` |
| Video Face Swap | Available | `scripts/video_tools.py face-swap` |
| Video Translate | Available | `scripts/video_tools.py translate` |
| 4K Super Resolve | Available | `scripts/video_tools.py super-resolve-4k` |
| Video Character Swap | Available | `scripts/video_tools.py character-swap` |
| Video Motion Control | Available | `scripts/video_tools.py motion-control` |
| Resolution Enhancement | Available | `scripts/definition.py` |
| Image Creation | Available | `scripts/image.py` |
| Frame Extraction/Analysis | Available | `scripts/frame_extractor.py` |
| TikTok Analytics | Available | `scripts/tiktok_analytics.py` |
| Ads Data | Available | `scripts/ads_data.py` |
| Preset Templates | Available | `scripts/preset_tpl.py` |
| Workspace Management | Available | `scripts/workspace.py` |
| File Upload | Available | `scripts/storage.py` |
| User/Billing Info | Available | `scripts/user.py` |
| Category Browsing | Available | `scripts/category.py` |

> **Never promise capabilities that don't exist as modules.**
