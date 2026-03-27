# TikTok Analytics Module

Analyze TikTok creators, video comments, fake views, and video metrics.

## When to Use

When you need insights on TikTok content: creator performance, comment sentiment, fake view detection, or video engagement metrics.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `creator` | Get creator info and milestones |
| `comments` | Analyze video comments |
| `detect` | Detect fake/bot views |
| `metrics` | Get video performance metrics |

## Usage

```bash
python {baseDir}/scripts/tiktok_analytics.py <subcommand> [options]
```

## Examples

```bash
# Analyze a creator
python {baseDir}/scripts/tiktok_analytics.py creator --url "https://tiktok.com/@creator"

# Analyze video comments
python {baseDir}/scripts/tiktok_analytics.py comments --url "https://tiktok.com/@creator/video/123"

# Detect fake views
python {baseDir}/scripts/tiktok_analytics.py detect --video-id "123456"

# Get video metrics
python {baseDir}/scripts/tiktok_analytics.py metrics --video-id "123456"
```

## Options

| Option | Description |
|--------|-------------|
| `--url URL` | TikTok video or creator URL |
| `--video-id ID` | TikTok video ID |
| `--creator-id ID` | TikTok creator ID |
| `--params JSON` | Extra params as JSON string |
