# URL2Video Module

Turn a product URL into a marketing video — full automated workflow.

## When to Use

When you need to create a marketing video from a product page URL. The workflow: scrape product info → generate video scripts → select avatars → preview → render final video.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `scrape` | Extract product info from URL |
| `get-metadata` | Get metadata |
| `gen-scripts` | Generate video scripts from product info |
| `get-avatars` | Get available avatars |
| `get-recommend-avatars` | Get recommended avatars |
| `submit-previews` | Submit preview generation |
| `get-previews` | Get preview results |
| `submit-render` | Submit single video render |
| `get-render` | Get render result |
| `submit-renders` | Submit batch renders |
| `get-renders` | Get batch render results |
| `get-render-list` | Get render task list |
| `get` | Get flow product video info |
| `update` | Update flow product video info |
| `get-step-status` | Get workflow step status |
| `update-op-meta` | Update OP metadata |
| `execute-op-task` | Execute OP task |

## Usage

```bash
python {baseDir}/scripts/url2video.py <subcommand> [options]
```

## Typical Workflow

```bash
# 1. Scrape product info
python {baseDir}/scripts/url2video.py scrape --url "https://example.com/product"

# 2. Generate video scripts
python {baseDir}/scripts/url2video.py gen-scripts --flow-id <flow_id>

# 3. Get recommended avatars
python {baseDir}/scripts/url2video.py get-recommend-avatars --flow-id <flow_id>

# 4. Submit preview
python {baseDir}/scripts/url2video.py submit-previews --flow-id <flow_id>

# 5. Check preview status
python {baseDir}/scripts/url2video.py get-previews --task-id <task_id>

# 6. Submit final render
python {baseDir}/scripts/url2video.py submit-render --flow-id <flow_id>

# 7. Get render result
python {baseDir}/scripts/url2video.py get-render --task-id <task_id>
```

## Options

| Option | Description |
|--------|-------------|
| `--url URL` | Product URL (for scrape) |
| `--flow-id ID` | Flow ID |
| `--task-id ID` | Task ID |
| `--product-id ID` | Product ID |
| `--params JSON` | Extra params as JSON string |
