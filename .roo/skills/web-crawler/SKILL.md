---
name: web-crawler
description: Recursively crawl websites to extract links, content, and structured data for agent consumption and knowledge base creation
---

# Web Crawler Skill

## When to use this skill
Use this skill when you need to:
- Extract all links and content from a website for agent knowledge ingestion
- Build a knowledge base from web documentation, APIs, or static sites
- Analyze website structure and content relationships
- Create offline copies of web content for reference
- Generate structured data from web pages (markdown, JSON, HTML)

## When NOT to use this skill
- **Do NOT use** for real-time data that changes frequently (use APIs instead)
- **Do NOT use** on websites that explicitly prohibit crawling in their robots.txt
- **Do NOT use** for authentication-required content unless you have proper credentials
- **Do NOT use** on high-traffic production sites without rate limiting

## Inputs required
- `url`: The starting URL to crawl (e.g., `https://example.com/docs`)
- `output_dir`: Directory to store crawled content (default: `./crawled_content`)
- `max_depth`: Maximum crawl depth (default: 3)
- `rate_limit`: Requests per second delay (default: 1 second)
- `domains`: List of allowed domains to follow (default: same domain only)

## Workflow

### Step 1: Validate the target URL
1. Check if the URL is accessible using `curl -I <url>`
2. Review `robots.txt` at `<url>/robots.txt` for crawl permissions
3. Identify the domain and any subdomains to include

### Step 2: Execute the crawler
Run the web crawler script with appropriate parameters:

```bash
python3 scripts/crawl.py --url <url> --output-dir <output_dir> --max-depth <depth> --rate-limit <delay>
```

**Example:**
```bash
python3 scripts/crawl.py --url https://docs.example.com --output-dir ./knowledge-base --max-depth 3 --rate-limit 1
```

### Step 3: Review the crawl output
The script generates:
- `content/`: Directory with extracted content organized by URL path
- `index.json`: Structured index of all crawled pages with metadata
- `links.csv`: CSV file mapping source URL to all discovered links
- `errors.log`: Log of any failed requests or parsing errors

### Step 4: Process content for agent consumption
Read the [`references/content_format.md`](references/content_format.md) guide to understand how content is structured for agent ingestion.

### Step 5: Validate completeness
Run the validation script to ensure all pages were successfully crawled:

```bash
python3 scripts/validate_crawl.py --index ./crawled_content/index.json
```

## File references
- [`scripts/crawl.py`](scripts/crawl.py) - Main crawling script (execute to crawl)
- [`scripts/validate_crawl.py`](scripts/validate_crawl.py) - Validation script (execute after crawl)
- [`references/content_format.md`](references/content_format.md) - Content structure reference (read when processing output)

## Expected output structure
```
crawled_content/
├── content/
│   ├── index.html
│   ├── docs/
│   │   ├── getting-started.html
│   │   └── api/
│   │       └── reference.html
├── index.json
├── links.csv
└── errors.log
```

## Troubleshooting

### Rate limiting issues
If you receive HTTP 429 errors, increase the `--rate-limit` parameter.

### Connection timeouts
For slow or unreliable sites, add `--timeout 30` to increase request timeout.

### JavaScript-heavy sites
This crawler only handles static HTML. For JavaScript-rendered content, use a headless browser approach instead.

### Robots.txt violations
If crawls are blocked, check if the site requires authentication or has strict robots.txt rules. Respect these restrictions.
