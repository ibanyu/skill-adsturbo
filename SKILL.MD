---
name: adsturbo-skill
description: "AI视频创作平台（AI-powered video creation）。支持：复刻视频、AI数字人、视频生成、视频翻译、换角色、对口型/口型同步、去水印、4K提升、动作控制、图片生成、TikTok数据分析、URL一键生成广告视频等。Generate videos with AI actors, translate, character-swap, lip-sync, and more — all via simple commands."
metadata:
  tags: adsturbo, video, ai-actor, tiktok, ads, lip-sync, character-swap, translate, url2video, image, 复刻视频, 数字人, 去水印, 换角色, 口型同步, 视频翻译, 4K, 生成视频, 生成图片
requires:
  bins: [python3]
primaryEnv: ADSTURBO_API_KEY
---

# AdsTurbo AI Skill

> Modular Python toolkit for the [AdsTurbo.ai](https://adsturbo.ai) API.
> AdsTurbo AI 视频创作工具包，支持中英文指令。

- AI Actor / AI数字人: Create talking-head videos with AI digital humans or your own custom avatars
- Video Generation / 视频生成: Generate videos from text/image/reference (文生视频、图生视频、复刻视频)
- URL2Video / 链接生成视频: Turn any product URL into a marketing video automatically
- Video Tools / 视频工具: Lip-sync 对口型, character-swap 换角色, translate 翻译, watermark removal 去水印, upscale 超分, motion control 动作控制, subtitle 字幕
- TikTok Analytics / TikTok分析: Analyze creators 达人分析, video comments 评论, fake views 查假量, and metrics 数据
- Image Creation / AI生成图片: AI-powered image generation

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
| Video Character Swap | ~3-5 min |
| Video Translate | ~5-10 min |
| Video Inpainting (Watermark Removal) | ~2-5 min |
| Super Resolve / 4K | ~3-5 min |
| Video Subtitle | ~2-5 min |
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
| Video Tools | `scripts/video_tools.py` | [video_tools.md](references/video_tools.md) | Video processing: analyze, lip-sync, inpaint, translate, upscale, character-swap, motion-control, subtitle |
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
> **核心原则：** 从用户意图出发，而非从 API 出发。

### Step 1 — Intent Analysis / 意图分析

| Dimension / 维度 | Ask Yourself / 判断依据 | Fallback / 兜底 |
|-----------|-------------|----------|
| **Output Type / 输出类型** | Video 视频? Image 图片? Audio 音频? Analytics 数据分析? | Must ask / 必须追问 |
| **Purpose / 用途** | Marketing ad 广告? Social media 社交媒体? Product demo 产品演示? | General marketing / 通用营销 |
| **Source Material / 素材** | Has URL 有链接? Has image/video 有图片/视频? Has script 有脚本? | Must ask / 必须追问 |
| **Style / Tone / 风格** | Professional 专业? Casual 休闲? Dynamic 动感? | Professional / 专业 |

### Step 2 — Tool Selection / 工具选择

```
用户需要什么？ / What does the user need?
│
├─ 复刻视频 / 仿制视频 / 参考视频生成新视频 / Recreate a video from reference?
│  → video_gen run --video <参考视频URL或ID>
│  → 如果有参考视频链接，先用 media batch-fetch 解析下载，再用 video_gen
│
├─ 用商品链接/产品URL生成广告视频 / Turn a product URL into a video ad?
│  → url2video (完整流程: scrape → scripts → preview → render)
│
├─ 数字人说话 / AI数字人 / 真人口播 / AI actor speaking to camera?
│  → ai_actor perform (使用平台数字人)
│  → ai_actor user-perform (使用自定义数字人)
│
├─ 文字生成视频 / 图片生成视频 / 文生视频 / 图生视频 / Generate video from text/image?
│  → video_gen run --prompt "描述" (文生视频)
│  → video_gen run --image <图片ID> (图生视频)
│
├─ 生成图片 / AI画图 / 文生图 / Generate an AI image?
│  → image run
│
├─ 对口型 / 口型同步 / 换口型 / Lip-sync a video?
│  → video_tools lipsync
│
├─ 去水印 / 去除视频水印 / Remove watermark?
│  → video_tools inpaint
│
├─ 换角色 / 替换整个人 / Swap characters?
│  → video_tools character-swap
│
├─ 视频翻译 / 多语言翻译 / Translate a video?
│  → video_tools translate
│
├─ 提升分辨率 / 4K增强 / 视频高清化 / Upscale to 4K?
│  → video_tools upscale
│  → definition run (通用分辨率增强)
│
├─ 动作控制 / 控制视频动作 / Motion control?
│  → video_tools motion-control
│
├─ 视频字幕 / 添加字幕 / 字幕翻译 / Add subtitles?
│  → video_tools subtitle
│
├─ 分析TikTok / 查达人数据 / 看评论 / 查播放量 / TikTok analytics?
│  → tiktok_analytics creator (达人分析)
│  → tiktok_analytics comments (评论分析)
│  → tiktok_analytics detect (查假量/刷量检测)
│  → tiktok_analytics metrics (视频数据)
│
├─ 拉片 / 视频逐帧分析 / 提取关键帧 / Analyze video frames?
│  → frame_extractor
│
├─ 查广告数据 / 看投放效果 / Browse ad data?
│  → ads_data
│
├─ 用模版生成视频 / 套模板 / Use a preset template?
│  → preset_tpl
│
├─ 裁剪视频 / 剪辑视频片段 / Cut video?
│  → media cut-video
│
├─ 下载视频 / 解析视频链接 / 批量获取视频 / Fetch videos from URL?
│  → media batch-fetch
│
├─ 查任务状态 / 看结果 / Check task status or results?
│  → workspace list (轮询状态) or workspace get (获取结果)
│
├─ 上传文件 / 上传图片 / 上传音频 / Upload a file?
│  → storage upload / upload-pic / upload-audio
│
├─ 查余额 / 查账单 / 查积分 / Check credits / billing?
│  → user credit or user billing
│
└─ 浏览分类 / 查类目 / Browse categories?
   → category list
```

### 中文常见表达 → 工具速查表

> 用户经常使用以下中文说法，对应的工具如下：

| 用户说法（中文） | 实际意图 | 对应工具 |
|---|---|---|
| 复刻视频、仿制视频、照着拍一个 | 基于参考视频生成相似视频 | `video_gen run --video <ref>` |
| 做一个广告视频、帮我生成广告 | 从产品链接生成营销视频 | `url2video` 全流程 |
| 数字人口播、让数字人说这段话 | AI 数字人说话视频 | `ai_actor perform` |
| 克隆我的形象、用我的照片做数字人 | 创建自定义数字人 | `ai_actor user-submit` → `user-perform` |
| 文字生成视频、文生视频 | 从文本描述生成视频 | `video_gen run --prompt` |
| 图片生成视频、图生视频、让图片动起来 | 从图片生成视频 | `video_gen run --image` |
| 生成图片、AI 画图、文生图 | 从文本生成图片 | `image run` |
| 对口型、口型同步、换音频 | 视频口型匹配新音频 | `video_tools lipsync` |
| 去水印、去 logo | 移除视频水印 | `video_tools inpaint` |
| 换角色、替换整个人 | 视频角色整体替换 | `video_tools character-swap` |
| 翻译视频、视频翻译成英文 | 视频多语言翻译 | `video_tools translate` |
| 4K、提升画质、高清化、超分 | 提升视频分辨率 | `video_tools upscale` |
| 动作控制、控制人物动作 | 视频动作引导 | `video_tools motion-control` |
| 加字幕、字幕翻译、视频字幕 | 视频字幕添加/翻译 | `video_tools subtitle` |
| 拉片、逐帧分析 | 视频帧提取分析 | `frame_extractor` |
| 裁剪、剪辑、截取片段 | 视频裁剪 | `media cut-video` |
| 下载视频、解析链接 | 从 URL 获取视频 | `media batch-fetch` |
| 查达人、分析博主 | TikTok 达人分析 | `tiktok_analytics creator` |
| 查评论、分析评论 | TikTok 评论分析 | `tiktok_analytics comments` |
| 查假量、刷量检测 | TikTok 虚假播放检测 | `tiktok_analytics detect` |
| 查播放量、视频数据 | TikTok 视频指标 | `tiktok_analytics metrics` |
| 查广告、投放效果 | 广告数据查询 | `ads_data` |
| 套模板、用模版 | 预设模板生成视频 | `preset_tpl` |
| 上传文件/图片/音频 | 上传素材 | `storage` |
| 查余额、查账单 | 账户与计费 | `user` |
| 克隆声音、声音复制 | 声音克隆 | `ai_actor user-clone-voice` |
| 语音合成、文字转语音、TTS | 文本转语音 | `ai_actor say` |
| 语音识别、语音转文字、ASR | 语音转文本 | `ai_actor asr` |

---

## Capability Boundaries / 能力边界

| Capability / 能力 | Status | Script |
|---------------------------------|-----------|-----|
| AI Actor — 数字人列表/口播/情感增强 | Available | `scripts/ai_actor.py` |
| AI Actor — 自定义数字人管理 | Available | `scripts/ai_actor.py` |
| AI Actor — 声音克隆/语音合成/语音识别 | Available | `scripts/ai_actor.py` |
| Video Generation / 视频生成（文生视频、图生视频、复刻视频） | Available | `scripts/video_gen.py` |
| URL-to-Video / 链接一键生成广告视频 | Available | `scripts/url2video.py` |
| Lip Sync / 对口型 | Available | `scripts/video_tools.py lipsync` |
| Video Inpainting / 去水印 | Available | `scripts/video_tools.py inpaint` |
| Video Character Swap / 视频换角色 | Available | `scripts/video_tools.py character-swap` |
| Video Translate / 视频翻译 | Available | `scripts/video_tools.py translate` |
| 4K Super Resolve / 4K超分 | Available | `scripts/video_tools.py upscale` |
| Video Character Swap / 角色替换 | Available | `scripts/video_tools.py character-swap` |
| Video Motion Control / 动作控制 | Available | `scripts/video_tools.py motion-control` |
| Video Analyze / 视频拉片 | Available | `scripts/video_tools.py analyze` |
| Video Subtitle / 视频字幕 | Available | `scripts/video_tools.py subtitle` |
| Resolution Enhancement / 分辨率提升 | Available | `scripts/definition.py` |
| Image Creation / AI生成图片 | Available | `scripts/image.py` |
| Frame Extraction / 拉片（逐帧分析） | Available | `scripts/frame_extractor.py` |
| TikTok Analytics / TikTok数据分析 | Available | `scripts/tiktok_analytics.py` |
| Ads Data / 广告数据 | Available | `scripts/ads_data.py` |
| Preset Templates / 预设模板 | Available | `scripts/preset_tpl.py` |
| Workspace Management / 任务管理 | Available | `scripts/workspace.py` |
| File Upload / 文件上传 | Available | `scripts/storage.py` |
| User/Billing Info / 用户与计费 | Available | `scripts/user.py` |
| Media Tools / 视频裁剪与下载 | Available | `scripts/media.py` |
| Category Browsing / 浏览分类 | Available | `scripts/category.py` |

> **Never promise capabilities that don't exist as modules.**
