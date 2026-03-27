# Frame Extractor Module

Video frame analysis — submit extraction tasks, get results, list tasks.

## When to Use

When you need to analyze video frames, extract key frames, or perform frame-level analysis on a video.

## Subcommands

| Subcommand | Description | Async? |
|------------|-------------|--------|
| `run` | Submit and poll until done | Yes |
| `submit` | Submit only | No |
| `result` | Get task result by ID | No |
| `list` | List frame extractor tasks | No |

## Usage

```bash
python {baseDir}/scripts/frame_extractor.py <subcommand> [options]
```

## Examples

```bash
# Submit and wait
python {baseDir}/scripts/frame_extractor.py run --video <video_id>

# Submit from URL
python {baseDir}/scripts/frame_extractor.py run --url "https://example.com/video.mp4"

# Check result
python {baseDir}/scripts/frame_extractor.py result --task-id <task_id>

# List tasks
python {baseDir}/scripts/frame_extractor.py list
```

## Options

| Option | Description |
|--------|-------------|
| `--video ID` | Video file/ID |
| `--url URL` | Video URL |
| `--task-id ID` | Task ID (for result) |
| `--page N` | Page number (for list) |
| `--params JSON` | Extra params |
| `--timeout SECS` | Polling timeout (default: 300) |
| `--interval SECS` | Polling interval (default: 5) |
