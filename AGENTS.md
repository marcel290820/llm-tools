# llm-tools

Single-file CLI tool (`tokcount.py`) for counting LLM tokens in documents.

## Running

```bash
source .venv/bin/activate
python tokcount.py pdf <file> [options]
```

No build step, no test suite. Python 3.12, deps in `requirements.txt`.

## Architecture

- **Subcommand pattern** (`tokcount pdf ...`) — new formats get a `process_<type>` function + subparser + branch in `main`. Don't build classes until 3+ formats share logic.
- **Lazy imports** — `tiktoken` and `pypdf` are imported inside functions, not at module top. Keep it that way.
- **pypdf logging** — suppressed to `ERROR` in `main()` (line 128). pypdf is noisy about harmless PDF quirks.

## Conventions

- No docstrings on self-evident functions. No error handling for impossible call-site conditions — let `main` catch.
- No speculative abstractions. Three similar lines > a premature helper.
- Don't add features that aren't asked for.
