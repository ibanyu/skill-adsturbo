# Image Module

AI-powered image creation.

## When to Use

When you need to generate an image from a text prompt or reference image.

## Subcommands

| Subcommand | When to use | Polls? |
|------------|-------------|--------|
| `run` | **Default.** Submit and wait | Yes |
| `submit` | Batch: fire task without waiting | No |
| `query` | Resume polling a known entry ID | Yes |

## Usage

```bash
python {baseDir}/scripts/image.py <subcommand> [options]
```

## Examples

```bash
# Generate image from prompt
python {baseDir}/scripts/image.py run --prompt "A futuristic cityscape at sunset"

# With specific model
python {baseDir}/scripts/image.py run --prompt "Product photo" --model "model_name" --aspect-ratio "16:9"
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt TEXT` | Image prompt |
| `--image ID` | Reference image file/ID |
| `--model NAME` | Model name |
| `--aspect-ratio RATIO` | Aspect ratio |
| `--resolution RES` | Resolution |
| `--style STYLE` | Style |
| `--timeout SECS` | Polling timeout (default: 300) |
| `--interval SECS` | Polling interval (default: 5) |
