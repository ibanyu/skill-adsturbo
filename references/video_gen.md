# Video Gen Module

Unified video generation from text, image, or reference.

## When to Use

When you need to generate a video — from a text prompt, an image, or a reference video.

## Subcommands

| Subcommand | When to use | Polls? |
|------------|-------------|--------|
| `run` | **Default.** Submit and wait for result | Yes |
| `submit` | Batch: fire task without waiting | No |
| `query` | Resume polling a known entry ID | Yes |

## Usage

```bash
python {baseDir}/scripts/video_gen.py <subcommand> [options]
```

## Examples

### Text-to-video
```bash
python {baseDir}/scripts/video_gen.py run --prompt "A cat playing piano in a jazz bar"
```

### Image-to-video
```bash
python {baseDir}/scripts/video_gen.py run --image <image_file_id> --prompt "Animate this scene"
```

### Batch submit
```bash
ID=$(python {baseDir}/scripts/video_gen.py submit --prompt "Video 1" -q)
python {baseDir}/scripts/video_gen.py query --entry-id "$ID"
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt TEXT` | Text prompt for generation |
| `--image ID` | Image file/ID for i2v |
| `--video ID` | Reference video file/ID |
| `--audio ID` | Audio file/ID |
| `--model NAME` | Model name |
| `--duration SEC` | Video duration |
| `--aspect-ratio RATIO` | Aspect ratio |
| `--mode MODE` | Generation mode |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |

## Output

`run` and `query` print the workspace entry result with video URL.
