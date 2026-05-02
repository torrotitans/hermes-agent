# PDF Content Structure Reference

This document describes how PDF content is structured for agent consumption and reasoning.

## Overview

When a PDF is converted to agent-readable content, it follows a structured format that enables:
- Easy parsing and navigation
- Preservation of document hierarchy
- Clear separation of content types (text, tables, images)
- Metadata for context and provenance

## Markdown Format Structure

### Document Header
```markdown
# Document Title

**Title:** [Document Title]
**Author:** [Author Name]
**Pages:** [Page Count]

---
```

### Page Sections
```markdown
## Page N

[Main text content with natural paragraph breaks]

### Table M
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

![Figure X](images/pageN_imgM.png)

---
```

### Heading Detection
- Lines under 60 characters without terminal punctuation are treated as headings
- Headings are formatted as `### Heading Text`
- Page numbers are always `## Page N`

### Table Formatting
- Tables are converted to markdown table syntax
- Multiple tables on a page are numbered sequentially
- Empty cells are preserved as empty markdown cells

## JSON Format Structure

```json
{
  "metadata": {
    "filename": "document.pdf",
    "page_count": 10,
    "pdf_metadata": {
      "Title": "Document Title",
      "Author": "Author Name",
      "CreationDate": "2024-01-01"
    }
  },
  "pages": [
    {
      "page_number": 1,
      "text": "Full page text content...",
      "tables": [
        {
          "rows": [
            ["Header 1", "Header 2"],
            ["Data 1", "Data 2"]
          ]
        }
      ],
      "images": ["images/page1_img1.png"]
    }
  ]
}
```

## Agent Reasoning Guidelines

### Text Content
- Text is preserved with original paragraph structure
- Line breaks within paragraphs are normalized
- Multiple consecutive blank lines are reduced to single blank lines

### Table Interpretation
- Tables maintain row/column structure
- Header rows are identified by position (first row)
- Numeric data is preserved as strings for fidelity

### Image References
- Images are referenced by relative path
- Image filenames encode page number and image sequence
- Original image format is preserved (PNG)

### Navigation
- Use page numbers for precise location references
- Tables and figures are numbered sequentially within each page
- Cross-references should use the format "Page N, Table M" or "Page N, Figure M"

## Processing Recommendations

### For Summarization
1. Read the document header for context
2. Scan page headings for structure
3. Focus on first/last paragraphs of each page for key points
4. Review tables for quantitative data

### For Question Answering
1. Identify relevant page(s) based on question topic
2. Search within page text for keywords
3. Check tables for specific data points
4. Reference images when visual context is needed

### For Knowledge Extraction
1. Extract structured data from tables
2. Identify key entities in text sections
3. Preserve relationships between concepts
4. Note page references for provenance

## Limitations

### Text Extraction
- Embedded fonts may cause character mapping issues
- Multi-column layouts may interleave text
- Footnotes may appear out of sequence

### Table Extraction
- Merged cells are flattened
- Complex nested tables may not preserve structure
- Tables spanning multiple pages are not merged

### Image Extraction
- Vector graphics may not extract properly
- Embedded fonts in images are not preserved
- Image quality depends on PDF source resolution
