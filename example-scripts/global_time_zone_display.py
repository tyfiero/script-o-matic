#!/usr/bin/env python3
import argparse
import pytz
from datetime import datetime
from collections import defaultdict
import sys
import textwrap
def get_current_times():
    """
    Retrieve current times for all time zones and organize them by region.
    Returns:
        A defaultdict with regions as keys and lists of (timezone, time) tuples as values.
    """
    times = defaultdict(list)
    for tz in pytz.all_timezones:
        try:
            timezone = pytz.timezone(tz)
            current_time = datetime.now(timezone)
            region = tz.split('/')[0]
            times[region].append((tz, current_time.strftime("%Y-%m-%d %H:%M:%S %Z")))
        except pytz.exceptions.PytzError:
            print(f"Warning: Unable to process timezone {tz}", file=sys.stderr)
    return times
def display_times(times, region=None, compact=False):
    """
    Display times for all regions or a specific region.
    Args:
        times (defaultdict): Organized time data.
        region (str, optional): Specific region to display. If None, display all regions.
        compact (bool): If True, use a compact display format.
    """
    if region:
        regions = [region] if region in times else []
    else:
        regions = sorted(times.keys())
    for r in regions:
        print(f"\n{r:=^60}")
        for tz, time in sorted(times[r]):
            if compact:
                print(f"{tz:<40} {time}")
            else:
                print(f"Timezone: {tz}")
                print(f"Current time: {time}")
                print("-" * 50)
def main():
    parser = argparse.ArgumentParser(
        description="Display current times for every time zone on Earth.",
        epilog=textwrap.dedent("""
        How to use:
        1. Run without arguments to see all time zones: python global_time_zone_display.py
        2. Specify a region: python global_time_zone_display.py --region America
        3. Use compact display: python global_time_zone_display.py --compact
        4. Combine options: python global_time_zone_display.py --region Europe --compact
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--region', help='Display times for a specific region')
    parser.add_argument('--compact', action='store_true', help='Use compact display format')
    args = parser.parse_args()
    try:
        times = get_current_times()
        if args.region and args.region not in times:
            print(f"Error: Region '{args.region}' not found. Available regions: {', '.join(sorted(times.keys()))}")
            sys.exit(1)
        display_times(times, args.region, args.compact)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    main()