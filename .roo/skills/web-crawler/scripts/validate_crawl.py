#!/usr/bin/env python3
"""
Crawl Validation Script
Validates the output of a web crawl and provides statistics.

Usage:
    python3 validate_crawl.py --index <index.json>
"""

import argparse
import json
import os
from pathlib import Path
from collections import defaultdict


def validate_crawl(index_path: str):
    """Validate crawl output and report statistics."""
    index_file = Path(index_path)

    if not index_file.exists():
        print(f"Error: Index file not found: {index_path}")
        return False

    with open(index_file, 'r') as f:
        index = json.load(f)

    print("=" * 60)
    print("CRAWL VALIDATION REPORT")
    print("=" * 60)
    print(f"Start URL:      {index.get('start_url', 'N/A')}")
    print(f"Crawled At:     {index.get('crawled_at', 'N/A')}")
    print("-" * 60)

    # Basic statistics
    total_pages = index.get('total_pages', 0)
    total_links = index.get('total_links', 0)
    errors = index.get('errors', 0)

    print(f"Total Pages:    {total_pages}")
    print(f"Total Links:    {total_links}")
    print(f"Errors:         {errors}")
    print("-" * 60)

    # Analyze pages by depth (extract from visited URLs)
    pages = index.get('pages', [])
    depth_distribution = defaultdict(int)
    domain_distribution = defaultdict(int)

    for page in pages:
        # Estimate depth from URL structure
        depth = page.count('/') - 3  # Assuming https://domain.com/
        depth_distribution[min(depth, 5)] += 1

        # Count by domain
        domain = page.split('/')[2] if '/' in page else 'unknown'
        domain_distribution[domain] += 1

    print("Depth Distribution:")
    for d in sorted(depth_distribution.keys()):
        print(f"  Depth {d}: {depth_distribution[d]} pages")

    print("\nDomain Distribution:")
    for domain, count in sorted(domain_distribution.items(), key=lambda x: -x[1]):
        print(f"  {domain}: {count} pages")

    # Check for broken links (if links.csv exists)
    links_file = index_file.parent / 'links.csv'
    if links_file.exists():
        with open(links_file, 'r') as f:
            lines = f.readlines()[1:]  # Skip header

        external_links = 0
        internal_links = 0
        base_domain = index.get('start_url', '').split('/')[2]

        for line in lines:
            parts = line.strip().strip('"').split('","')
            if len(parts) >= 2:
                target = parts[1].strip('"')
                if base_domain and base_domain in target:
                    internal_links += 1
                else:
                    external_links += 1

        print(f"\nLink Analysis:")
        print(f"  Internal links: {internal_links}")
        print(f"  External links: {external_links}")

    # Check for errors
    errors_file = index_file.parent / 'errors.log'
    if errors_file.exists():
        with open(errors_file, 'r') as f:
            error_lines = f.readlines()

        if error_lines:
            print(f"\nErrors ({len(error_lines)}):")
            for line in error_lines[:10]:  # Show first 10
                print(f"  {line.strip()}")
            if len(error_lines) > 10:
                print(f"  ... and {len(error_lines) - 10} more errors")

    # Validation status
    print("\n" + "=" * 60)
    if errors == 0:
        print("Status: SUCCESS - All pages crawled successfully")
    elif errors < total_pages * 0.1:
        print("Status: WARNING - Some errors detected but crawl completed")
    else:
        print("Status: FAILED - High error rate detected")
    print("=" * 60)

    return errors < total_pages * 0.1


def main():
    parser = argparse.ArgumentParser(description='Validate web crawl output')
    parser.add_argument('--index', required=True, help='Path to index.json file')

    args = parser.parse_args()

    success = validate_crawl(args.index)
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
