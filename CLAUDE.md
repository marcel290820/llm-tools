# llm-tools

A collection of CLI utilities for working with LLMs — currently a token counter (`tokcount.py`) that estimates context usage across document types.

## Project layout

```
tokcount.py      # Token counter CLI (the main tool)
requirements.txt # pypdf, tiktoken
.venv/           # Python 3.12 virtual environment
```

## Running the tool

```bash
source .venv/bin/activate
python tokcount.py pdf document.pdf
python tokcount.py pdf *.pdf --verbose
python tokcount.py pdf document.pdf --model gpt-4 --quiet
```

## Development

No build step. No test suite yet. Run directly with Python 3.12.

Install dependencies:
```bash
pip install -r requirements.txt
```

## Architecture decisions

- **Subcommand pattern** — `tokcount pdf ...` leaves room for `txt`, `html`, etc. without breaking the interface.
- **Lazy imports** — `tiktoken` and `pypdf` are imported inside functions, not at module top-level, so startup is fast and errors surface only when the relevant subcommand runs.
- **pypdf logging suppressed** — set to `ERROR` level in `main()` (line 128); pypdf is noisy about non-critical PDF quirks irrelevant to token counting.
- **No classes** — the tool is small enough that plain functions are the right abstraction level.

## Adding a new document type

1. Add a `process_<type>` function following the shape of `process_pdf`.
2. Add a subparser in `create_parser` with the same flags (`-m`, `-v`, `-q`).
3. Add the corresponding branch in `main`.

Don't build a class hierarchy until at least three formats share meaningful common logic.

## Coding guidelines

- Don't add docstrings to functions whose names and signatures are self-evident.
- Don't add error handling for things that can't happen at the call site. `process_pdf` can raise — `main` catches it.
- Don't add features that aren't asked for. Token counting is the job.
- Prefer the simplest correct implementation. A new format handler should be ~15 lines, not a class with lifecycle methods.
- No speculative abstractions. Three similar lines of code is better than a premature helper.
