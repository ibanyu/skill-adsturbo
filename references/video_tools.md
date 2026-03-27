# Video Tools Module

Video processing utilities — lip-sync, watermark removal, face swap, translation, 4K upscale, character swap, motion control.

## When to Use

When you need to process an existing video: sync lip movements to new audio, remove watermarks, swap faces, translate to another language, upscale to 4K, swap characters, or control motion.

## Tools

| Tool | API Path | Description |
|------|----------|-------------|
| `lipsync` | `/internalapi/v1/lipsync/submit` | Sync lip movements to audio |
| `inpainting` | `/internalapi/v1/videoinpainting/submit` | Remove watermarks |
| `face-swap` | `/internalapi/v1/videofaceswap/submit` | Swap faces in video |
| `translate` | `/internalapi/v1/videotranslate/submit` | Translate video to another language |
| `super-resolve-4k` | `/internalapi/v1/videosuperresolve4k/submit` | Upscale to 4K |
| `character-swap` | `/internalapi/v1/videocharacterswap/submit` | Swap characters in video |
| `motion-control` | `/internalapi/v1/videomotioncontrol/submit` | Control motion in video |

## Usage

```bash
python {baseDir}/scripts/video_tools.py <run|submit|query> <tool> [options]
```

## Examples

### Lip sync
```bash
python {baseDir}/scripts/video_tools.py run lipsync --video <video_id> --audio <audio_id>
```

### Remove watermark
```bash
python {baseDir}/scripts/video_tools.py run inpainting --video <video_id>
```

### Face swap
```bash
python {baseDir}/scripts/video_tools.py run face-swap --video <video_id> --face-image <image_id>
```

### Translate video
```bash
python {baseDir}/scripts/video_tools.py run translate --video <video_id> --target-lang "zh"
```

### 4K upscale
```bash
python {baseDir}/scripts/video_tools.py run super-resolve-4k --video <video_id>
```

## Options

| Option | Description |
|--------|-------------|
| `--video ID` | Video file/ID |
| `--audio ID` | Audio file/ID (for lipsync) |
| `--image ID` | Image file/ID |
| `--face-image ID` | Face image for swap |
| `--text TEXT` | Text input |
| `--source-lang LANG` | Source language (for translate) |
| `--target-lang LANG` | Target language (for translate) |
| `--params JSON` | Extra params as JSON string |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |

## Output

All tools are async. `run` polls workspace until done and prints the result.
