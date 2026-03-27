# Media Module

Media tools — video cutting and batch video fetching.

## When to Use

When you need to trim/cut a video or batch-download videos from URLs.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `cut-video` | Cut/trim a video segment |
| `batch-fetch` | Batch fetch original videos from URLs |

## Usage

```bash
python {baseDir}/scripts/media.py <subcommand> [options]
```

## Examples

```bash
# Cut video
python {baseDir}/scripts/media.py cut-video --video <video_id> --start "00:00:05" --end "00:00:15"

# Batch fetch videos
python {baseDir}/scripts/media.py batch-fetch --urls "https://example.com/v1.mp4,https://example.com/v2.mp4"
```

## Options

### `cut-video`

| Option | Description |
|--------|-------------|
| `--video ID` | Video file/ID |
| `--start TIME` | Start time |
| `--end TIME` | End time |

### `batch-fetch`

| Option | Description |
|--------|-------------|
| `--urls URLS` | Comma-separated video URLs |
