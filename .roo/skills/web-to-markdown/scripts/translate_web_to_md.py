#!/usr/bin/env python3
"""
FN:translate_web_to_md.py
Web to Markdown Translator - Recursively crawls web pages and translates content into agent-friendly markdown format.

Classes:
- WebToMarkdownTranslator: Main translator class handling crawl and conversion

Functions:
- FN:parse_args: Parse command line arguments (lines 245-280)
- FN:main: Entry point (lines 283-320)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup, Tag

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('web_crawl.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)


class WebToMarkdownTranslator:
    """
    Recursively crawls web pages and converts them to agent-friendly markdown.
    
    Attributes:
        start_url: The starting URL for crawling
        output_dir: Directory to store markdown output
        max_depth: Maximum crawl depth
        rate_limit: Delay between requests in seconds
        visited_urls: Set of already visited URLs
        pages: Dictionary of URL to page data
    """
    
    def __init__(
        self,
        start_url: str,
        output_dir: str = "./web-content",
        max_depth: int = 3,
        rate_limit: float = 1.0,
        include_assets: bool = False,
        respect_robots: bool = True,
        use_headless: bool = False,
        encoding: str = "utf-8"
    ):
        """FN:__init__ Initialize the translator with configuration."""
        self.start_url = start_url
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.rate_limit = rate_limit
        self.include_assets = include_assets
        self.respect_robots = respect_robots
        self.use_headless = use_headless
        self.encoding = encoding
        
        self.visited_urls: Set[str] = set()
        self.pages: Dict[str, dict] = {}
        self.errors: List[str] = []
        self.robots_rules: Dict[str, List[str]] = {}
        
        # Create output directories
        self.markdown_dir = self.output_dir / "markdown"
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        
        # Session for efficient requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebToMarkdown/1.0; +https://github.com/example/bot)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        logger.info(f"FN:__init__ Initialized translator for {start_url}")
    
    def fetch_robots_txt(self, url: str) -> None:
        """FN:fetch_robots_txt Fetch and parse robots.txt for the domain."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                self._parse_robots_txt(response.text)
                logger.info(f"FN:fetch_robots_txt Fetched robots.txt from {robots_url}")
        except Exception as e:
            logger.warning(f"FN:fetch_robots_txt Could not fetch robots.txt: {e}")
    
    def _parse_robots_txt(self, content: str) -> None:
        """FN:_parse_robots_txt Parse robots.txt content to extract disallow rules."""
        current_agents = []
        
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.lower().startswith('user-agent:'):
                agent = line.split(':', 1)[1].strip()
                current_agents = [agent] if agent != '*' else ['*']
            elif line.lower().startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                for agent in current_agents:
                    if agent not in self.robots_rules:
                        self.robots_rules[agent] = []
                    self.robots_rules[agent].append(path)
    
    def is_allowed_by_robots(self, url: str) -> bool:
        """FN:is_allowed_by_robots Check if URL is allowed by robots.txt rules."""
        if not self.respect_robots:
            return True
        
        parsed = urlparse(url)
        path = parsed.path or '/'
        
        # Check rules for specific user agent
        for agent in ['WebToMarkdown/1.0', '*']:
            if agent in self.robots_rules:
                for disallow in self.robots_rules[agent]:
                    if disallow and path.startswith(disallow):
                        return False
        
        return True
    
    def fetch_page(self, url: str) -> Optional[str]:
        """FN:fetch_page Fetch HTML content from URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            error_msg = f"Failed to fetch {url}: {e}"
            self.errors.append(error_msg)
            logger.error(f"FN:fetch_page {error_msg}")
            return None
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """FN:extract_links Extract all links from HTML content."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Remove fragment
            href, _ = urldefrag(href)
            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)
            links.append(absolute_url)
        
        return links
    
    def html_to_markdown(self, html: str, url: str) -> str:
        """FN:html_to_markdown Convert HTML content to markdown format."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else urlparse(url).path
        
        # Extract main content (try common content containers)
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.body
        
        if not main_content:
            main_content = soup
        
        # Build markdown
        md_lines = [f"# {title}\n"]
        
        # Process headings
        for heading in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = len(heading.name)
            text = heading.get_text().strip()
            if text:
                md_lines.append(f"{'#' * level} {text}\n")
        
        # Process paragraphs
        for para in main_content.find_all('p'):
            text = para.get_text().strip()
            if text:
                md_lines.append(f"{text}\n")
        
        # Process code blocks
        for code in main_content.find_all(['pre', 'code']):
            code_text = code.get_text()
            if code_text:
                # Try to detect language
                lang_class = code.get('class', [])
                lang = ''
                for cls in lang_class:
                    if cls.startswith('language-'):
                        lang = cls.replace('language-', '')
                        break
                
                md_lines.append(f"\n```{lang}\n{code_text}\n```\n")
        
        # Process tables
        for table in main_content.find_all('table'):
            md_table = self._convert_table(table)
            if md_table:
                md_lines.append(f"\n{md_table}\n")
        
        # Process lists
        for list_elem in main_content.find_all(['ul', 'ol']):
            md_list = self._convert_list(list_elem)
            if md_list:
                md_lines.append(f"\n{md_list}\n")
        
        return '\n'.join(md_lines)
    
    def _convert_table(self, table: Tag) -> str:
        """FN:_convert_table Convert HTML table to markdown table."""
        rows = table.find_all('tr')
        if not rows:
            return ""
        
        md_lines = []
        headers = []
        
        # Extract header row
        header_row = rows[0]
        for cell in header_row.find_all(['th', 'td']):
            headers.append(cell.get_text().strip())
        
        if headers:
            md_lines.append('| ' + ' | '.join(headers) + ' |')
            md_lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
        
        # Extract data rows
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text().strip() for cell in cells]
            if row_data:
                md_lines.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(md_lines)
    
    def _convert_list(self, list_elem: Tag) -> str:
        """FN:_convert_list Convert HTML list to markdown list."""
        md_lines = []
        is_ordered = list_elem.name == 'ol'
        
        for i, item in enumerate(list_elem.find_all('li', recursive=False)):
            text = item.get_text().strip()
            if is_ordered:
                md_lines.append(f"{i + 1}. {text}")
            else:
                md_lines.append(f"- {text}")
        
        return '\n'.join(md_lines)
    
    def crawl_url(self, url: str, depth: int = 0) -> None:
        """FN:crawl_url Recursively crawl a URL and convert to markdown."""
        # Check depth limit
        if depth > self.max_depth:
            logger.debug(f"FN:crawl_url Max depth reached for {url}")
            return
        
        # Check if already visited
        if url in self.visited_urls:
            return
        
        # Check robots.txt
        if not self.is_allowed_by_robots(url):
            logger.warning(f"FN:crawl_url Blocked by robots.txt: {url}")
            return
        
        self.visited_urls.add(url)
        logger.info(f"FN:crawl_url Crawling {url} (depth {depth})")
        
        # Fetch page
        html = self.fetch_page(url)
        if not html:
            return
        
        # Extract links for recursive crawling
        links = self.extract_links(html, url)
        
        # Convert to markdown
        markdown = self.html_to_markdown(html, url)
        
        # Store page data
        self.pages[url] = {
            'url': url,
            'markdown': markdown,
            'links': links,
            'depth': depth,
            'word_count': len(markdown.split()),
            'crawled_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Save markdown file
        self._save_markdown(url, markdown)
        
        # Rate limiting
        time.sleep(self.rate_limit)
        
        # Recursively crawl links
        for link in links:
            if link not in self.visited_urls:
                self.crawl_url(link, depth + 1)
    
    def _save_markdown(self, url: str, markdown: str) -> None:
        """FN:_save_markdown Save markdown content to file."""
        # Generate filename from URL
        parsed = urlparse(url)
        path = parsed.path.rstrip('/') or 'index'
        
        # Create directory structure
        file_path = self.markdown_dir / (path + '.md')
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add frontmatter
        frontmatter = {
            'source_url': url,
            'title': parsed.path or 'Untitled',
            'crawled_at': datetime.utcnow().isoformat() + 'Z',
            'word_count': len(markdown.split()),
            'depth': self.pages.get(url, {}).get('depth', 0)
        }
        
        full_content = self._generate_frontmatter(frontmatter) + '\n' + markdown
        
        # Write file
        with open(file_path, 'w', encoding=self.encoding) as f:
            f.write(full_content)
        
        logger.info(f"FN:_save_markdown Saved {file_path}")
    
    def _generate_frontmatter(self, data: dict) -> str:
        """FN:_generate_frontmatter Generate YAML frontmatter from data."""
        lines = ['---']
        for key, value in data.items():
            lines.append(f'{key}: {value}')
        lines.append('---')
        return '\n'.join(lines)
    
    def generate_index(self) -> str:
        """FN:generate_index Generate master index of all crawled pages."""
        index_lines = ['# Web Content Index\n', f'Generated: {datetime.utcnow().isoformat()}Z\n\n']
        
        # Sort pages by URL
        sorted_pages = sorted(self.pages.items(), key=lambda x: x[0])
        
        for url, data in sorted_pages:
            parsed = urlparse(url)
            path = parsed.path or '/'
            title = data.get('title', path)
            word_count = data.get('word_count', 0)
            
            index_lines.append(f"## [{title}]({path}.md)\n")
            index_lines.append(f"- **URL**: {url}\n")
            index_lines.append(f"- **Word Count**: {word_count}\n")
            index_lines.append(f"- **Depth**: {data.get('depth', 0)}\n")
            index_lines.append(f"- **Crawled At**: {data.get('crawled_at', 'N/A')}\n\n")
        
        return '\n'.join(index_lines)
    
    def save_metadata(self) -> None:
        """FN:save_metadata Save crawl metadata to JSON file."""
        metadata = {
            'start_url': self.start_url,
            'crawled_at': datetime.utcnow().isoformat() + 'Z',
            'total_pages': len(self.pages),
            'total_errors': len(self.errors),
            'pages': {
                url: {
                    'url': data['url'],
                    'word_count': data['word_count'],
                    'depth': data['depth'],
                    'crawled_at': data['crawled_at']
                }
                for url, data in self.pages.items()
            }
        }
        
        metadata_path = self.output_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding=self.encoding) as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"FN:save_metadata Saved metadata to {metadata_path}")
    
    def save_errors(self) -> None:
        """FN:save_errors Save error log to file."""
        errors_path = self.output_dir / 'errors.log'
        with open(errors_path, 'w', encoding=self.encoding) as f:
            for error in self.errors:
                f.write(error + '\n')
        
        logger.info(f"FN:save_errors Saved errors to {errors_path}")
    
    def run(self) -> None:
        """FN:run Execute the full crawl and translation process."""
        logger.info(f"FN:run Starting crawl from {self.start_url}")
        
        # Fetch robots.txt
        self.fetch_robots_txt(self.start_url)
        
        # Crawl starting URL
        self.crawl_url(self.start_url)
        
        # Generate and save index
        index_content = self.generate_index()
        index_path = self.output_dir / 'index.md'
        with open(index_path, 'w', encoding=self.encoding) as f:
            f.write(index_content)
        
        # Save metadata
        self.save_metadata()
        
        # Save errors
        self.save_errors()
        
        logger.info(f"FN:run Crawl complete. Output in {self.output_dir}")


def parse_args() -> argparse.Namespace:
    """FN:parse_args Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Translate web pages to agent-friendly markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --url https://docs.example.com
  %(prog)s --url https://docs.example.com --output-dir ./knowledge --max-depth 2
  %(prog)s --url https://docs.example.com --rate-limit 2 --include-assets
        '''
    )
    
    parser.add_argument(
        '--url',
        required=True,
        help='Starting URL to crawl'
    )
    parser.add_argument(
        '--output-dir',
        default='./web-content',
        help='Output directory for markdown (default: ./web-content)'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum crawl depth (default: 3)'
    )
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    parser.add_argument(
        '--include-assets',
        action='store_true',
        help='Include images and other assets'
    )
    parser.add_argument(
        '--respect-robots',
        action='store_true',
        default=True,
        help='Respect robots.txt rules (default: True)'
    )
    parser.add_argument(
        '--use-headless',
        action='store_true',
        help='Use headless browser for JavaScript rendering'
    )
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Character encoding (default: utf-8)'
    )
    
    return parser.parse_args()


def main() -> None:
    """FN:main Entry point for the web-to-markdown translator."""
    args = parse_args()
    
    translator = WebToMarkdownTranslator(
        start_url=args.url,
        output_dir=args.output_dir,
        max_depth=args.max_depth,
        rate_limit=args.rate_limit,
        include_assets=args.include_assets,
        respect_robots=args.respect_robots,
        use_headless=args.use_headless,
        encoding=args.encoding
    )
    
    translator.run()
    
    # Print summary
    print(f"\n{'='*60}")
    print("CRAWL SUMMARY")
    print(f"{'='*60}")
    print(f"Start URL: {args.url}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Pages Crawled: {len(translator.pages)}")
    print(f"Total Errors: {len(translator.errors)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
