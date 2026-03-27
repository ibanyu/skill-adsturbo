# Preset Template Module

Browse preset video templates and generate videos from them.

## When to Use

When you want to quickly generate a video using a pre-designed template instead of building from scratch.

## Subcommands

| Subcommand | When to use | Async? |
|------------|-------------|--------|
| `list` | Browse available templates | No |
| `run` | Generate video from template and poll | Yes |
| `submit` | Submit only | No |
| `query` | Resume polling | Yes |

## Usage

```bash
python {baseDir}/scripts/preset_tpl.py <subcommand> [options]
```

## Examples

```bash
# Browse templates
python {baseDir}/scripts/preset_tpl.py list

# Generate video from template
python {baseDir}/scripts/preset_tpl.py run --template-id <template_id>
```

## Options

| Option | Description |
|--------|-------------|
| `--template-id ID` | Template ID (required for run/submit) |
| `--params JSON` | Extra params |
| `--timeout SECS` | Polling timeout (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |
