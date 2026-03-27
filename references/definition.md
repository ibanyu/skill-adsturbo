# Definition Module

Video resolution enhancement and avatar performance data.

## When to Use

When you need to upscale a video's resolution or check avatar performance metrics.

## Subcommands

| Subcommand | When to use | Async? |
|------------|-------------|--------|
| `run` | Submit resolution enhancement and poll | Yes |
| `submit` | Submit only | No |
| `query` | Resume polling | Yes |
| `performance` | Get avatar performance data | No |

## Usage

```bash
python {baseDir}/scripts/definition.py <subcommand> [options]
```

## Examples

```bash
# Enhance resolution
python {baseDir}/scripts/definition.py run --video <video_id>

# Check avatar performance
python {baseDir}/scripts/definition.py performance
```

## Options

### `run` and `submit`

| Option | Description |
|--------|-------------|
| `--video ID` | Video file/ID |
| `--definition DEF` | Target definition/resolution |
| `--params JSON` | Extra params |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |
