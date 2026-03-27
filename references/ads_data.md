# Ads Data Module

Browse ad performance data — list and inspect ad details.

## When to Use

When you need to view ad campaign data, list ads, or get specific ad details.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `list` | List ads |
| `get` | Get ad details |

## Usage

```bash
python {baseDir}/scripts/ads_data.py <subcommand> [options]
```

## Examples

```bash
# List ads
python {baseDir}/scripts/ads_data.py list

# Get specific ad
python {baseDir}/scripts/ads_data.py get --ad-id <ad_id>
```

## Options

### `list`

| Option | Description |
|--------|-------------|
| `--page N` | Page number |
| `--page-size N` | Page size |
| `--params JSON` | Extra filter params |

### `get`

| Option | Description |
|--------|-------------|
| `--ad-id ID` | Ad ID (required) |
