#!/usr/bin/env python3
"""
SELinux Policy Patcher CLI

Command-line interface for analyzing AVC denials and generating SELinux policy rules.
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from .parser import AVCParser
from .rules import RuleSet
from .formatters import export_rules
from .adb import capture_all_sources, pull_pstore, is_device_connected, wait_for_device
from .suggester import TypeSuggester
from .trend import init_database, store_denial, print_trend_report, get_database_stats


def print_banner():
    """Print a nice banner."""
    print("=" * 60)
    print("  Android SELinux Policy Patcher v1.0.0")
    print("  Parse AVC denials and generate policy rules")
    print("=" * 60)


def print_summary(ruleset: RuleSet) -> None:
    """Print a summary table of parsed rules."""
    rules = ruleset.get_all_rules()
    groups = defaultdict(set)
    
    for src, tgt, cls, perms in rules:
        groups[(src, tgt, cls)].update(perms)
    
    print("\n" + "=" * 60)
    print("AVC Denial Summary")
    print("=" * 60)
    
    for (src, tgt, cls), perms in sorted(groups.items()):
        perm_str = ', '.join(sorted(perms))
        print(f"  {src} -> {tgt} : {cls} [{len(perms)}] {perm_str}")
    
    print("=" * 60)
    print(f"Total: {len(rules)} rules from {len(groups)} unique combinations")
    print()


def parse_offline(args) -> RuleSet:
    """Parse AVC denials from a file."""
    ruleset = RuleSet(merge_permissions=args.merge)
    parser = AVCParser()
    
    with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            denial = parser.parse_line(line)
            if denial:
                ruleset.add_denial(denial.to_dict())
                if args.trend:
                    store_denial(denial.to_dict())
    
    print(f"Parsed {parser.get_stats()['parsed']} AVC denials from {args.input}")
    return ruleset


def run_live(args) -> RuleSet:
    """Run live capture from ADB."""
    if not is_device_connected():
        print("Waiting for ADB device...")
        if not wait_for_device(verbose=True):
            print("No device found. Exiting.")
            sys.exit(1)
    
    if args.trend:
        init_database()
    
    ruleset = RuleSet(merge_permissions=args.merge)
    
    def callback(denial):
        ruleset.add_denial(denial)
        if args.trend:
            store_denial(denial)
        if args.verbose:
            print(f"  {denial['source']} -> {denial['target']} : {denial['class']}")
    
    print(f"Starting live capture for {args.timeout} seconds...")
    count = capture_all_sources(
        callback=callback,
        duration=args.timeout,
        verbose=args.verbose
    )
    
    print(f"Captured {count} AVC denials")
    return ruleset


def main():
    parser = argparse.ArgumentParser(
        description="Android SELinux Policy Patcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse an existing log file
  %(prog)s -i avc.log -o rules.te

  # Live capture with trend tracking
  %(prog)s --live --timeout 60 --trend

  # Output as JSON
  %(prog)s -i avc.log --format json -o rules.json

  # Merge permissions into single rules
  %(prog)s -i avc.log --merge -o rules.te
        """
    )
    
    # Input options
    parser.add_argument('-i', '--input', help='Input file (offline mode)')
    parser.add_argument('--live', action='store_true', help='Live capture mode')
    parser.add_argument('--timeout', type=int, default=60, help='Live capture duration (seconds)')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--format', choices=['cil', 'te', 'json', 'csv', 'md'], default='cil',
                        help='Output format (default: cil)')
    
    # Processing options
    parser.add_argument('--merge', action='store_true', 
                        help='Merge multiple permissions into single rules')
    parser.add_argument('--exclude-domains', help='Comma-separated domains to exclude')
    parser.add_argument('--include-domains', help='Comma-separated domains to include only')
    parser.add_argument('--filter-perms', help='Comma-separated permissions to include only')
    
    # Analysis options
    parser.add_argument('--suggest-types', action='store_true',
                        help='Suggest new SELinux types based on paths')
    parser.add_argument('--trend', action='store_true',
                        help='Track denials in database for trend analysis')
    parser.add_argument('--show-trends', action='store_true',
                        help='Show trend report from database')
    
    # Other options
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--stats', action='store_true', help='Show parsing statistics')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Handle trend show mode
    if args.show_trends:
        stats = get_database_stats()
        print_trend_report()
        return
    
    # Validate arguments
    if not args.input and not args.live:
        parser.error("Please specify either --input file or --live mode")
    
    if args.trend:
        init_database()
    
    # Parse or capture
    if args.live:
        ruleset = run_live(args)
    else:
        ruleset = parse_offline(args)
    
    if ruleset.count() == 0:
        print("No AVC denials found.")
        return
    
    # Apply filters
    src_whitelist = None
    src_blacklist = None
    perm_whitelist = None
    
    if args.include_domains:
        src_whitelist = set(args.include_domains.split(','))
    if args.exclude_domains:
        src_blacklist = set(args.exclude_domains.split(','))
    if args.filter_perms:
        perm_whitelist = set(args.filter_perms.split(','))
    
    if src_whitelist or src_blacklist or perm_whitelist:
        ruleset = ruleset.filter(
            source_whitelist=src_whitelist,
            source_blacklist=src_blacklist,
            perm_whitelist=perm_whitelist,
        )
        print(f"After filtering: {ruleset.count()} rules")
    
    # Type suggestions
    if args.suggest_types:
        suggester = TypeSuggester()
        suggester.analyze(ruleset)
        suggestions = suggester.suggest_new_types()
        if suggestions:
            print("\nType Suggestions:")
            for s in suggestions:
                print(f"  {s}")
    
    # Print summary
    print_summary(ruleset)
    
    # Output
    if args.output:
        export_rules(ruleset, args.output, args.format)
        print(f"Rules written to {args.output}")
    else:
        # Print to console
        print("\nGenerated Rules:")
        for src, tgt, cls, perms in ruleset.get_all_rules()[:20]:
            if args.format == 'cil':
                for perm in perms:
                    print(f"  (allow {src} {tgt} ({cls} ({perm})))")
            else:
                print(f"  allow {src} {tgt}:{cls} {{ {' '.join(perms)} }};")
        
        if ruleset.count() > 20:
            print(f"  ... and {ruleset.count() - 20} more rules")
    
    # Show trends if enabled
    if args.trend:
        print_trend_report()


if __name__ == '__main__':
    main()
