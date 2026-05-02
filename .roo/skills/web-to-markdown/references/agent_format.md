# Agent-Friendly Markdown Format

## Purpose
This document defines the markdown format specification for web content translated for AI agent consumption and RAG (Retrieval-Augmented Generation) systems.

## Structure

### Frontmatter (Required)
Every markdown file must start with YAML frontmatter containing:

```yaml
---
source_url: https://example.com/page
title: Page Title
crawled_at: 2024-01-15T10:30:00Z
word_count: 1250
depth: 2
tags: [documentation, api, reference]
---
```

### Content Sections
1. **Title (H1)**: Matches the page title
2. **Summary**: 2-3 sentence overview of page content
3. **Main Content**: Organized with proper heading hierarchy
4. **Related Links**: Links to other crawled pages

## Formatting Rules

### Headings
- Use ATX-style headings (`#`, `##`, `###`)
- Maintain logical hierarchy (no skipped levels)
- Include anchor IDs for navigation

### Code Blocks
- Always specify language: ` ```python ` not ` ``` `
- Preserve indentation exactly
- Include file paths in comments when relevant

### Tables
- Use GFM table syntax
- Include header row with column descriptions
- Align columns appropriately

### Links
- Convert absolute URLs to relative paths when targeting crawled content
- Preserve external links as-is
- Add link titles for context

## Metadata Extraction

### Required Fields
- `source_url`: Original URL
- `title`: Page title from `<title>` or H1
- `crawled_at`: ISO 8601 timestamp
- `word_count`: Total words in content

### Optional Fields
- `author`: Author name if available
- `published_date`: Publication date
- `tags`: Extracted keywords/categories
- `depth`: Crawl depth from start URL

## Quality Checks

Before integration, verify:
- [ ] Frontmatter is valid YAML
- [ ] All links resolve to crawled pages or external URLs
- [ ] Code blocks have language specified
- [ ] No broken image references
- [ ] Heading hierarchy is logical

## Integration with RAG

### Chunking Strategy
- Split at heading boundaries
- Keep related sections together
- Include frontmatter in each chunk

### Indexing Keys
- Use `source_url` as primary key
- Index by `tags` for filtering
- Use `title` for search relevance

## Example Output

```markdown
---
source_url: https://docs.example.com/api/users
title: Users API Reference
crawled_at: 2024-01-15T10:30:00Z
word_count: 850
depth: 2
tags: [api, users, reference]
---

# Users API Reference

## Summary
This document describes the REST API endpoints for user management, including creation, retrieval, update, and deletion operations.

## Endpoints

### GET /api/users

Retrieves a list of all users.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Maximum results (default: 10) |
| offset | integer | No | Pagination offset |

**Example Response:**
```json
{
  "users": [
    {"id": 1, "name": "John Doe"}
  ],
  "total": 100
}
```

## Related Pages
- [Authentication](./auth.md)
- [User Roles](./roles.md)
```
