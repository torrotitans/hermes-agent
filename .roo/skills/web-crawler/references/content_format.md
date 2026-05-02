# Content Format Reference

This document describes how crawled web content is structured and formatted for agent consumption.

## Table of Contents
1. [Output Directory Structure](#output-directory-structure)
2. [Content File Format](#content-file-format)
3. [Index File Format](#index-file-format)
4. [Links File Format](#links-file-format)
5. [Agent Consumption Patterns](#agent-consumption-patterns)

---

## Output Directory Structure

```
crawled_content/
├── content/           # Extracted HTML content organized by URL path
│   ├── index.html
│   ├── docs/
│   │   ├── getting-started.html
│   │   └── api/
│   │       └── reference.html
│   └── ...
├── index.json         # Crawl metadata and page listing
├── links.csv          # Source-to-target link mapping
└── errors.log         # Failed requests and errors
```

---

## Content File Format

Each crawled page is saved as an HTML file with embedded metadata:

```html
<!--
Source URL: https://example.com/docs/getting-started
Title: Getting Started Guide
Crawled: 2026-04-15 12:00:00
Domain: example.com
Depth: 1
-->
<!DOCTYPE html>
<html>
<head>
    <title>Getting Started Guide</title>
</head>
<body>
<!-- Extracted text content goes here -->
</body>
</html>
```

### Metadata Fields
| Field | Description |
|-------|-------------|
| `Source URL` | Original URL of the page |
| `Title` | Page title from HTML |
| `Crawled` | Timestamp of crawl |
| `Domain` | Source domain |
| `Depth` | Crawl depth from start URL |

---

## Index File Format

The `index.json` file contains crawl metadata:

```json
{
  "start_url": "https://example.com",
  "total_pages": 150,
  "total_links": 423,
  "errors": 2,
  "crawled_at": "2026-04-15 12:00:00",
  "pages": [
    "https://example.com/",
    "https://example.com/docs/getting-started",
    "https://example.com/api/reference"
  ]
}
```

---

## Links File Format

The `links.csv` file maps source URLs to discovered links:

```csv
source,target
"https://example.com/","https://example.com/docs"
"https://example.com/","https://example.com/about"
"https://example.com/docs","https://example.com/docs/getting-started"
```

---

## Agent Consumption Patterns

### Pattern 1: Knowledge Base Ingestion

```python
import json

# Load the crawl index
with open('crawled_content/index.json') as f:
    index = json.load(f)

# Process each page
for url in index['pages']:
    path = url_to_path(url)  # Convert URL to file path
    with open(f'crawled_content/content/{path}') as f:
        content = f.read()
    # Process content for vector embedding or knowledge graph
```

### Pattern 2: Link Graph Construction

```python
import csv

# Build adjacency list from links.csv
links = {}
with open('crawled_content/links.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        source = row['source']
        target = row['target']
        if source not in links:
            links[source] = []
        links[source].append(target)
```

### Pattern 3: Content Filtering

```python
# Filter pages by depth or domain
relevant_pages = [
    page for page in index['pages']
    if get_depth(page) <= 2  # Only shallow content
]
```

---

## Notes for Agents

- **Content is pre-extracted**: You don't need to re-crawl; use the saved HTML files
- **Metadata is available**: Check the HTML comments for crawl context
- **Links are mapped**: Use `links.csv` to understand site structure
- **Errors are logged**: Check `errors.log` for any missing content
