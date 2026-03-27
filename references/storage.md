# Storage Module

File upload utilities for general files, images, and audio.

## When to Use

When you need to upload a local file before using it in other tasks. Most script modules auto-upload local files, but you can also upload manually.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `upload` | Upload a general file |
| `upload-pic` | Upload an image file |
| `upload-audio` | Upload an audio file (no transcoding) |

## Usage

```bash
python {baseDir}/scripts/storage.py <subcommand> [options]
```

## Examples

```bash
# Upload a video file
python {baseDir}/scripts/storage.py upload --file /path/to/video.mp4

# Upload an image
python {baseDir}/scripts/storage.py upload-pic --file /path/to/photo.jpg

# Upload audio
python {baseDir}/scripts/storage.py upload-audio --file /path/to/audio.mp3
```

## Options

| Option | Description |
|--------|-------------|
| `--file PATH` | Local file path to upload (required) |

## Output

Returns the uploaded file ID which can be used in other modules.
