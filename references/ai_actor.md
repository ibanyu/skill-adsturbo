# AI Actor Module

Manage and use AI digital humans for talking-head video generation.

## When to Use

When you need to create a talking-head video with an AI digital human, manage custom avatars, generate TTS audio, or transcribe speech.

## Subcommands

| Subcommand | When to use | Async? |
|------------|-------------|--------|
| `list` | Browse available AI actors | No |
| `favourite` | Favourite/unfavourite an actor | No |
| `perform` | Generate talking-head video with AI actor | Yes — polls workspace |
| `enhance` | Enhance emotion in text before TTS | No |
| `say` | Generate TTS audio | No |
| `asr` | Speech-to-text transcription | No |
| `user-submit` | Create a custom user actor | No |
| `user-voice` | Generate voice for custom actor | No |
| `user-perform` | Perform with custom actor | Yes — polls workspace |
| `user-detail` | Get custom actor details | No |
| `user-clone-voice` | Clone voice for custom actor | No |
| `user-del` | Delete a custom actor | No |
| `user-img` | Create custom actor image | No |

## Usage

```bash
python {baseDir}/scripts/ai_actor.py <subcommand> [options]
```

## Examples

### List actors
```bash
python {baseDir}/scripts/ai_actor.py list
```

### Perform with AI actor (submit + poll)
```bash
python {baseDir}/scripts/ai_actor.py perform --actor-id <id> --text "Hello, welcome to our product demo!"
```

### Create custom actor
```bash
python {baseDir}/scripts/ai_actor.py user-submit --name "My Avatar" --image <image_file_id>
```

### Clone voice
```bash
python {baseDir}/scripts/ai_actor.py user-clone-voice --actor-id <id> --audio <audio_file_id>
```

## Options

### `perform` and `user-perform`

| Option | Description |
|--------|-------------|
| `--actor-id ID` | Actor ID (required) |
| `--text TEXT` | Text for the actor to speak |
| `--audio ID` | Audio file/ID for audio-driven mode |
| `--timeout SECS` | Max polling time (default: 600) |
| `--interval SECS` | Polling interval (default: 5) |
| `--json` | Output full JSON response |
| `--submit-only` | Submit only, don't poll |

### `say`

| Option | Description |
|--------|-------------|
| `--text TEXT` | Text to speak (required) |
| `--voice-id ID` | Voice ID |

### `asr`

| Option | Description |
|--------|-------------|
| `--audio ID` | Audio file/ID (required) |

## Output

`perform` and `user-perform` return the workspace entry result with video URL after polling completes.
