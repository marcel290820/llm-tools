#!/usr/bin/env python3
"""
Token counter CLI tool for estimating LLM context usage.

Supports counting tokens in various document formats for LLM context estimation.
"""

import argparse
import sys
from pathlib import Path


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Count tokens in text using tiktoken."""
    import tiktoken
    
    try:
        encoding = tiktoken.get_encoding(model)
    except ValueError:
        # If model name is passed, try to get encoding for that model
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fall back to cl100k_base (used by GPT-4, GPT-3.5-turbo)
            encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def extract_text_from_pdf(filepath: Path) -> str:
    """Extract text content from a PDF file."""
    from pypdf import PdfReader
    
    reader = PdfReader(filepath)
    text_parts = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)
    
    return "\n".join(text_parts)


def process_pdf(filepath: Path, model: str, verbose: bool = False) -> dict:
    """Process a PDF file and return token statistics."""
    from pypdf import PdfReader

    text = extract_text_from_pdf(filepath)
    token_count = count_tokens(text, model)
    char_count = len(text)
    page_count = len(PdfReader(filepath).pages) if verbose else None
    
    return {
        "filepath": str(filepath),
        "tokens": token_count,
        "characters": char_count,
        "pages": page_count,
    }


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with subcommands for extensibility."""
    parser = argparse.ArgumentParser(
        prog="tokcount",
        description="Count tokens in documents for LLM context estimation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s pdf document.pdf
  %(prog)s pdf document.pdf --model gpt-4
  %(prog)s pdf *.pdf --verbose

Supported encodings:
  cl100k_base  - GPT-4, GPT-3.5-turbo, text-embedding-ada-002 (default)
  p50k_base    - Codex models
  r50k_base    - GPT-3 models (davinci, curie, etc.)
        """,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available document types",
        required=True,
    )
    
    # PDF subcommand
    pdf_parser = subparsers.add_parser(
        "pdf",
        help="Count tokens in PDF documents",
        description="Extract text from PDF files and count tokens.",
    )
    pdf_parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="PDF file(s) to process",
    )
    pdf_parser.add_argument(
        "-m", "--model",
        default="cl100k_base",
        help="Tokenizer model/encoding to use (default: cl100k_base)",
    )
    pdf_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed statistics",
    )
    pdf_parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only output the token count (useful for scripting)",
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)

    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "pdf":
        total_tokens = 0
        results = []
        
        for filepath in args.files:
            if not filepath.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
            
            if not filepath.suffix.lower() == ".pdf":
                print(f"Warning: {filepath} may not be a PDF file", file=sys.stderr)
            
            try:
                result = process_pdf(filepath, args.model, args.verbose)
                results.append(result)
                total_tokens += result["tokens"]
            except Exception as e:
                print(f"Error processing {filepath}: {e}", file=sys.stderr)
                return 1
        
        # Output results
        if args.quiet:
            print(total_tokens)
        else:
            for result in results:
                if args.verbose:
                    print(f"File: {result['filepath']}")
                    print(f"  Pages:      {result['pages']}")
                    print(f"  Characters: {result['characters']:,}")
                    print(f"  Tokens:     {result['tokens']:,}")
                    print()
                else:
                    print(f"{result['filepath']}: {result['tokens']:,} tokens")
            
            if len(results) > 1:
                print(f"Total: {total_tokens:,} tokens")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
