---
name: web-to-markdown
description: Recursively crawl web pages and translate content into agent-friendly markdown (.md) format for knowledge ingestion and learning
---

# Web to Markdown Translator

## When to use this skill
Use this skill when you need to:
- Convert website content into structured markdown for agent knowledge bases
- Create offline, searchable documentation from web sources
- Prepare training data from web pages for AI agent learning
- Extract and normalize content from multiple linked pages
- Build a RAG (Retrieval-Augmented Generation) knowledge corpus

## When NOT to use this skill
- **Do NOT use** for websites that explicitly prohibit crawling in robots.txt
- **Do NOT use** for authentication-required content without proper credentials
- **Do NOT use** for real-time data that changes frequently (use APIs instead)
- **Do NOT use** on high-traffic production sites without rate limiting
- **Do NOT use** if you only need raw HTML (use web-crawler skill instead)

## Inputs required
- `url`: The starting URL to crawl (e.g., `https://docs.example.com`)
- `output_dir`: Directory to store markdown output (default: `./web-content`)
- `max_depth`: Maximum crawl depth (default: 3)
- `rate_limit`: Delay between requests in seconds (default: 1)
- `include_assets`: Whether to download images/assets (default: false)

## Workflow

### Step 1: Validate the target URL
1. Check if the URL is accessible:
   ```bash
   curl -I <url>
   ```
2. Review `robots.txt` for crawl permissions:
   ```bash
   curl <url>/robots.txt
   ```
3. Verify the domain is in the allowed list

### Step 2: Execute the web-to-markdown translator
Run the translation script with appropriate parameters:

```bash
python3 scripts/translate_web_to_md.py --url <url> --output-dir <output_dir> --max-depth <depth>
```

**Example:**
```bash
python3 scripts/translate_web_to_md.py --url https://docs.example.com --output-dir ./knowledge-base --max-depth 3 --rate-limit 2
```

### Step 3: Review the markdown output
The script generates:
- `markdown/`: Directory with translated content organized by URL path
- `index.md`: Master index linking all crawled pages
- `metadata.json`: Structured metadata about the crawl (URLs, timestamps, word counts)
- `errors.log`: Log of any failed requests or parsing errors

### Step 4: Validate markdown quality
Run the validation script to check markdown structure:

```bash
python3 scripts/validate_markdown.py --output-dir ./web-content
```

### Step 5: Integrate with agent knowledge base
Read the [`references/agent_format.md`](references/agent_format.md) guide to understand how to integrate the markdown content with your agent's RAG system.

## File references
- [`scripts/translate_web_to_md.py`](scripts/translate_web_to_md.py) - Main translation script (execute to crawl and translate)
- [`scripts/validate_markdown.py`](scripts/validate_markdown.py) - Validation script (execute after translation)
- [`references/agent_format.md`](references/agent_format.md) - Agent-friendly markdown format reference (read when integrating)

## Expected output structure
```
web-content/
├── markdown/
│   ├── index.md
│   ├── docs/
│   │   ├── getting-started.md
│   │   └── api/
│   │       └── reference.md
├── metadata.json
├── index.md
└── errors.log
```

## Markdown format specification
Each generated markdown file includes:
- Frontmatter with URL, title, crawl timestamp, and word count
- Clean heading hierarchy (H1, H2, H3)
- Preserved code blocks with language detection
- Converted tables and lists
- Relative links to other crawled pages

## Troubleshooting

### Rate limiting issues
If you receive HTTP 429 errors, increase the `--rate-limit` parameter or add `--respect-robots` flag.

### JavaScript-heavy sites
This translator handles static HTML. For JavaScript-rendered content, use a headless browser mode:
```bash
python3 scripts/translate_web_to_md.py --url <url> --use-headless
```

### Encoding errors
For non-UTF8 content, specify encoding explicitly:
```bash
python3 scripts/translate_web_to_md.py --url <url> --encoding latin-1
```

### Missing content
If pages appear empty, check if the site requires authentication or uses dynamic loading.
