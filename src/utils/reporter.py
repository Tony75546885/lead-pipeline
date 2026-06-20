"""
Acquisition funnel reporter
"""
import json
from datetime import datetime, timedelta
from src.storage.lead_store import LeadStore
from src.storage.models import LeadStatus


class Reporter:
    def __init__(self, store: LeadStore):
        self.store = store

    def print_report(self, days: int = 30, fmt: str = "table"):
        since = datetime.now() - timedelta(days=days)
        stats = self.store.get_stats(since=since)

        if fmt == "json":
            print(json.dumps(stats, indent=2))
            return

        if fmt == "csv":
            print("status,count")
            for k, v in stats.items():
                print(f"{k},{v}")
            return

        # table
        total = stats.get("total", 0)
        contacted = stats.get(LeadStatus.CONTACTED.value, 0)
        qualified = stats.get(LeadStatus.QUALIFIED.value, 0)
        converted = stats.get(LeadStatus.CONVERTED.value, 0)

        conv_rate = f"{converted/contacted*100:.1f}%" if contacted else "n/a"
        qual_rate = f"{qualified/total*100:.1f}%" if total else "n/a"

        print(f"\n{'='*52}")
        print(f"  Lead Pipeline — Report (last {days} days)")
        print(f"{'='*52}")
        print(f"  {'Total leads':<28} {total:>8}")
        print(f"  {'Qualified':<28} {qualified:>8}  ({qual_rate})")
        print(f"  {'Contacted':<28} {contacted:>8}")
        print(f"  {'Replied':<28} {stats.get(LeadStatus.REPLIED.value, 0):>8}")
        print(f"  {'Converted':<28} {converted:>8}  ({conv_rate})")
        print(f"  {'Disqualified':<28} {stats.get(LeadStatus.DISQUALIFIED.value, 0):>8}")
        print(f"{'='*52}")

        print("\n  By status:")
        for status in LeadStatus:
            count = stats.get(status.value, 0)
            bar = "█" * min(count, 40)
            print(f"  {status.value:<16} {count:>4}  {bar}")
        print()
