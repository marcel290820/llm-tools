# tokcount

Count LLM tokens in documents before you paste them into a context window.

Ever wondered whether a PDF will fit in your model's context limit? `tokcount` extracts the text and counts the tokens using the same tokenizer your model does, so you know before you send.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.12+.

## Usage

```bash
python tokcount.py pdf document.pdf
```

Count multiple files at once:

```bash
python tokcount.py pdf report.pdf appendix.pdf
```

Use a specific model's tokenizer:

```bash
python tokcount.py pdf document.pdf --model gpt-4
```

Detailed output (pages, characters, tokens per file):

```bash
python tokcount.py pdf document.pdf --verbose
```

Script-friendly output (just the total token count):

```bash
python tokcount.py pdf document.pdf --quiet
```

## Options

| Flag | Description |
|------|-------------|
| `-m`, `--model` | Tokenizer encoding or model name (default: `cl100k_base`) |
| `-v`, `--verbose` | Show pages, characters, and tokens per file |
| `-q`, `--quiet` | Print only the total token count |

## Supported tokenizers

- `cl100k_base` — GPT-4, GPT-3.5-turbo, text-embedding-ada-002 (default)
- `p50k_base` — Codex models
- `r50k_base` — GPT-3 models (davinci, curie, etc.)

You can also pass a model name (e.g. `gpt-4`) and tokcount will look up the right encoding automatically, falling back to `cl100k_base` if unknown.
