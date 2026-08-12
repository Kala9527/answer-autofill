from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from .config import load_config
from .excel_processor import ExcelAnswerProcessor, FolderStats, SmokeResult
from .llm_client import AnswerLLMClient


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdio()
    return asyncio.run(_async_main(argv))


async def _async_main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.dry_run and args.smoke_test:
        parser.error("--dry-run and --smoke-test cannot be used together")

    config_path = Path(args.config).resolve() if args.config else _default_config_path()
    config = load_config(config_path if config_path.exists() else None)
    concurrency = args.concurrency or config.processing.concurrency

    completer = None if args.dry_run else AnswerLLMClient(config.model, max_concurrency=concurrency)
    processor = ExcelAnswerProcessor(config, completer=completer, dry_run=args.dry_run)
    try:
        if args.smoke_test:
            result = await processor.smoke_test(
                Path(args.input_folder),
                recursive=args.recursive,
                smoke_column=args.smoke_column,
            )
            _print_smoke_result(result, concurrency=concurrency)
            return 0

        stats = await processor.process_folder(
            Path(args.input_folder),
            output_folder=Path(args.output_dir) if args.output_dir else None,
            recursive=args.recursive,
        )
        _print_summary(stats, dry_run=args.dry_run, concurrency=concurrency)
        return 0 if stats.failed_cells == 0 else 2
    finally:
        if completer is not None:
            await completer.aclose()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="answer-autofill",
        description="Auto-fill invalid answers in Excel row 2 through a local DeepSeek OpenAI-compatible API.",
    )
    parser.add_argument("input_folder", help="Folder containing .xlsx/.xlsm files to process.")
    parser.add_argument("--output-dir", help="Output folder. Defaults to answer_autofill_output inside input folder.")
    parser.add_argument("--config", help="Config file path. Defaults to config.json in this tool folder.")
    parser.add_argument("--recursive", action="store_true", help="Process Excel files in subfolders.")
    parser.add_argument("--dry-run", action="store_true", help="Scan invalid cells only; no model calls or output files.")
    parser.add_argument("--smoke-test", action="store_true", help="Call the real model for the first invalid question group only.")
    parser.add_argument("--smoke-column", help="With --smoke-test, test a specific invalid column such as BR.")
    parser.add_argument("--concurrency", type=int, help="Maximum concurrent model requests. Defaults to 8.")
    return parser


def _default_config_path() -> Path:
    return Path(__file__).resolve().parents[1] / "config.json"


def _print_summary(stats: FolderStats, *, dry_run: bool, concurrency: int) -> None:
    mode = "Scan" if dry_run else "Process"
    print(f"{mode} complete: {stats.input_folder}")
    print(f"Files: {len(stats.files)}")
    print(f"Invalid answers found: {stats.invalid_cells}")
    if not dry_run:
        print(f"Async model concurrency: {concurrency}")
        print(f"Answers filled: {stats.filled_cells}")
        print(f"Failures kept unchanged: {stats.failed_cells}")
        print(f"Output folder: {stats.output_folder}")

    for file_stats in stats.files:
        output_text = "dry-run, no file generated" if file_stats.output is None else str(file_stats.output)
        print(f"\n- {file_stats.source.name} -> {output_text}")
        for sheet in file_stats.sheets:
            print(
                f"  [{sheet.sheet_name}] groups {sheet.groups_seen}, "
                f"invalid {sheet.invalid_cells}, filled {sheet.filled_cells}, failed {sheet.failed_cells}"
            )
            for warning in sheet.warnings:
                print(f"    Warning: {warning}")


def _print_smoke_result(result: SmokeResult, *, concurrency: int) -> None:
    print("Smoke test complete.")
    print(f"Async model concurrency configured: {concurrency}")
    print(f"File: {result.source}")
    print(f"Sheet: {result.sheet_name}")
    print(f"Question group: {result.group_columns}")
    if result.context_answers:
        print("\nValid answers kept as context:")
        for item in result.context_answers:
            print(f"- {item.column}: {item.answer}")
    print("\nGenerated answer:")
    print(f"- {result.target.column} | original={result.target.original_answer!r}")
    print(f"  Q: {result.target.question}")
    print(f"  A: {result.generated}")


def _ensure_utf8_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
