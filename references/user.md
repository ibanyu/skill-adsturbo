# User & Billing Module

User information, credit history, and billing history.

## When to Use

When you need to check user account info, credit balance/history, or billing records.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `info` | Get user info |
| `credit` | Get credit history |
| `billing` | Get billing history |

## Usage

```bash
python {baseDir}/scripts/user.py <subcommand> [options]
```

## Examples

```bash
# Check user info
python {baseDir}/scripts/user.py info

# Check credit history
python {baseDir}/scripts/user.py credit

# Check billing
python {baseDir}/scripts/user.py billing --page 1
```

## Options

### `credit` and `billing`

| Option | Description |
|--------|-------------|
| `--page N` | Page number |
