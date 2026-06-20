#!/usr/bin/env python3
"""
C1 - Automated Client Acquisition System
"""
import argparse
import sys
from src.pipeline import AcquisitionPipeline
from src.utils.logger import get_logger
from src.utils.config import load_config

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="C1 - Automated Client Acquisition System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py run --source linkedin --niche "SaaS"
  python main.py run --source scrape --url "https://example.com/directory"
  python main.py schedule --interval 24
  python main.py report --last 7
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # run command
    run_parser = subparsers.add_parser("run", help="Run acquisition pipeline once")
    run_parser.add_argument("--source", choices=["linkedin", "scrape", "apollo", "all"], default="all")
    run_parser.add_argument("--niche", type=str, help="Target niche/industry")
    run_parser.add_argument("--url", type=str, help="URL to scrape (if source=scrape)")
    run_parser.add_argument("--limit", type=int, default=50, help="Max leads per run")
    run_parser.add_argument("--dry-run", action="store_true", help="Don't send messages, just collect leads")

    # schedule command
    sched_parser = subparsers.add_parser("schedule", help="Run on a schedule")
    sched_parser.add_argument("--interval", type=int, default=24, help="Hours between runs")
    sched_parser.add_argument("--niche", type=str)

    # report command
    report_parser = subparsers.add_parser("report", help="Show acquisition report")
    report_parser.add_argument("--last", type=int, default=30, help="Days to include")
    report_parser.add_argument("--format", choices=["table", "json", "csv"], default="table")

    # enrich command
    enrich_parser = subparsers.add_parser("enrich", help="Enrich existing leads with extra data")
    enrich_parser.add_argument("--input", required=True, help="CSV with leads to enrich")

    args = parser.parse_args()
    config = load_config()

    pipeline = AcquisitionPipeline(config)

    if args.command == "run":
        pipeline.run(
            source=args.source,
            niche=args.niche,
            url=getattr(args, "url", None),
            limit=args.limit,
            dry_run=args.dry_run,
        )
    elif args.command == "schedule":
        pipeline.schedule(interval_hours=args.interval, niche=args.niche)
    elif args.command == "report":
        pipeline.report(days=args.last, fmt=args.format)
    elif args.command == "enrich":
        pipeline.enrich(input_file=args.input)


if __name__ == "__main__":
    main()
