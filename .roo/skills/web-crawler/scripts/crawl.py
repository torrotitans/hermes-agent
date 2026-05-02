#!/usr/bin/env python3
"""
Web Crawler Script
Recursively crawls a website and extracts content for agent consumption.

Usage:
    python3 crawl.py --url <start_url> [--output-dir <dir>] [--max-depth <n>] [--rate-limit <sec>]
"""

import argparse
import json
import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebCrawler:
    """Recursive web crawler for content extraction."""

    def __init__(self, start_url: str, output_dir: str, max_depth: int = 3,
                 rate_limit: float = 1.0, timeout: int = 30):
        self.start_url = self._normalize_url(start_url)
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.visited = set()
        self.links_map = []
        self.errors = []
        self.base_domain = urlparse(self.start_url).netloc

        # Create output directories
        self.content_dir = self.output_dir / 'content'
        self.content_dir.mkdir(parents=True, exist_ok=True)

        # Setup requests session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebCrawler/1.0; +https://example.com/bot)'
        })

    def _normalize_url(self, url: str) -> str:
        """Normalize URL to ensure consistent format."""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc

    def _is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain as start URL."""
        return self._get_domain(url) == self.base_domain

    def _url_to_path(self, url: str) -> str:
        """Convert URL to filesystem path."""
        parsed = urlparse(url)
        path = unquote(parsed.path)
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path = path + 'index.html'
        elif not '.' in path.split('/')[-1]:
            path = path + '/index.html'
        # Remove query strings and fragments
        path = path.split('?')[0].split('#')[0]
        # Make it relative and safe for filesystem
        safe_path = path.lstrip('/').replace('/', os.sep)
        return safe_path if safe_path else 'index.html'

    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract main text content from HTML."""
        # Remove script and style elements
        for elem in soup(['script', 'style', 'noscript']):
            elem.decompose()

        # Get text
        text = soup.get_text(separator='\n', strip=True)

        # Clean up whitespace
        lines = text.split('\n')
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                clean_lines.append(stripped)

        return '\n'.join(clean_lines)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list:
        """Extract all links from HTML."""
        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href'].strip()
            # Convert relative URLs to absolute
            full_url = urljoin(base_url, href)
            # Normalize and deduplicate
            full_url = self._normalize_url(full_url)
            links.append(full_url)
        return links

    def _save_content(self, url: str, title: str, content: str, metadata: dict):
        """Save extracted content to file."""
        path = self.content_dir / self._url_to_path(url)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save as HTML with extracted metadata
        output = f"""<!--
Source URL: {url}
Title: {title}
Crawled: {metadata.get('timestamp', 'N/A')}
Domain: {metadata.get('domain', 'N/A')}
Depth: {metadata.get('depth', 0)}
-->
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
{content}
</body>
</html>
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(output)

    def crawl(self, url: str, depth: int = 0):
        """Recursively crawl a URL."""
        # Check depth limit
        if depth > self.max_depth:
            logger.debug(f"Max depth reached for {url}")
            return

        # Check if already visited
        if url in self.visited:
            logger.debug(f"Already visited: {url}")
            return

        # Rate limiting
        time.sleep(self.rate_limit)

        try:
            logger.info(f"Crawling: {url} (depth={depth})")
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()

            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                logger.debug(f"Skipping non-HTML content: {url}")
                return

            self.visited.add(url)

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title = soup.title.string if soup.title else 'Untitled'

            # Extract main content
            content = self._extract_text(soup)

            # Create metadata
            metadata = {
                'url': url,
                'title': title,
                'depth': depth,
                'domain': self._get_domain(url),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'content_length': len(content)
            }

            # Save content
            self._save_content(url, title, content, metadata)

            # Extract and process links
            links = self._extract_links(soup, url)
            for link in links:
                self.links_map.append({'source': url, 'target': link})

                # Crawl linked pages (only same domain)
                if self._is_same_domain(link) and link not in self.visited:
                    self.crawl(link, depth + 1)

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to crawl {url}: {str(e)}"
            logger.warning(error_msg)
            self.errors.append({'url': url, 'error': str(e)})

        except Exception as e:
            error_msg = f"Error processing {url}: {str(e)}"
            logger.error(error_msg)
            self.errors.append({'url': url, 'error': str(e)})

    def save_index(self):
        """Save crawl index and metadata."""
        index = {
            'start_url': self.start_url,
            'total_pages': len(self.visited),
            'total_links': len(self.links_map),
            'errors': len(self.errors),
            'crawled_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'pages': list(self.visited)
        }

        # Save index.json
        with open(self.output_dir / 'index.json', 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)

        # Save links.csv
        with open(self.output_dir / 'links.csv', 'w', encoding='utf-8') as f:
            f.write('source,target\n')
            for link in self.links_map:
                source = link['source'].replace('"', '""')
                target = link['target'].replace('"', '""')
                f.write(f'"{source}","{target}"\n')

        # Save errors.log
        with open(self.output_dir / 'errors.log', 'w', encoding='utf-8') as f:
            for error in self.errors:
                f.write(f"{error['url']}: {error['error']}\n")

        logger.info(f"Crawl complete: {len(self.visited)} pages, {len(self.links_map)} links, {len(self.errors)} errors")


def main():
    parser = argparse.ArgumentParser(description='Recursive web crawler for agent content extraction')
    parser.add_argument('--url', required=True, help='Starting URL to crawl')
    parser.add_argument('--output-dir', default='./crawled_content', help='Output directory for crawled content')
    parser.add_argument('--max-depth', type=int, default=3, help='Maximum crawl depth')
    parser.add_argument('--rate-limit', type=float, default=1.0, help='Delay between requests in seconds')
    parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds')

    args = parser.parse_args()

    crawler = WebCrawler(
        start_url=args.url,
        output_dir=args.output_dir,
        max_depth=args.max_depth,
        rate_limit=args.rate_limit,
        timeout=args.timeout
    )

    crawler.crawl(args.url)
    crawler.save_index()

    print(f"\nCrawl complete!")
    print(f"Output directory: {args.output_dir}")
    print(f"Total pages: {len(crawler.visited)}")
    print(f"Total links: {len(crawler.links_map)}")
    print(f"Errors: {len(crawler.errors)}")


if __name__ == '__main__':
    main()
