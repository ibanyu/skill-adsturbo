# Workspace Module

Task results hub — poll status, get results, manage workspace entries.

## When to Use

When you need to check the status of an async task, get results, delete entries, share or remix content.

**Key distinction:**
- `list` = poll/check task status (轮询状态)
- `get` = get task result details (获取结果)

## Subcommands

| Subcommand | When to use |
|------------|-------------|
| `list` | Poll task status, browse entries |
| `get` | Get detailed result for an entry |
| `del` | Delete a workspace entry |
| `share` | Share entry to community |
| `remix` | Remix an entry |
| `prompt-analysis` | Analyze prompts used in an entry |

## Usage

```bash
python {baseDir}/scripts/workspace.py <subcommand> [options]
```

## Examples

### Poll task status
```bash
python {baseDir}/scripts/workspace.py list --entry-id <id>
```

### Get result
```bash
python {baseDir}/scripts/workspace.py get --entry-id <id>
```

### Delete entry
```bash
python {baseDir}/scripts/workspace.py del --entry-id <id>
```

## Options

### `list`

| Option | Description |
|--------|-------------|
| `--entry-id ID` | Filter by entry ID |
| `--page N` | Page number |
| `--page-size N` | Page size |

### `get`, `del`, `share`, `remix`, `prompt-analysis`

| Option | Description |
|--------|-------------|
| `--entry-id ID` | Entry ID (required) |
