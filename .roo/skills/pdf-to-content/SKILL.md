---
name: pdf-to-content
description: Convert PDF documents into structured, agent-readable content for analysis, reasoning, and knowledge ingestion
---

# PDF to Content Conversion Skill

## When to use this skill
Use this skill when you need to:
- Extract text, tables, and images from PDF documents for agent analysis
- Convert PDFs into structured formats (markdown, JSON) for RAG/knowledge base ingestion
- Parse PDFs with complex layouts (forms, reports, academic papers)
- Extract metadata and document structure from PDF files
- Prepare PDF content for downstream processing (summarization, Q&A, indexing)

## When NOT to use this skill
- **Do NOT use** for scanned images without OCR capability (use OCR-specific tools instead)
- **Do NOT use** for password-protected PDFs without the password
- **Do NOT use** when you need to preserve exact visual formatting (use PDF rendering instead)
- **Do NOT use** for real-time PDF generation or editing tasks

## Inputs required
- `pdf_path`: Path to the PDF file (relative or absolute)
- `output_format`: Output format - `markdown`, `json`, or `text` (default: `markdown`)
- `extract_images`: Whether to extract embedded images (default: `false`)
- `output_dir`: Directory to store extracted content (default: same directory as PDF)

## Workflow

### Step 1: Validate the PDF file
1. Check if the PDF file exists and is accessible
2. Verify the PDF is not corrupted by attempting to read its metadata
3. Check if the PDF requires a password

```bash
python3 scripts/pdf_to_content.py --info <pdf_path>
```

### Step 2: Extract content from PDF
Run the PDF extraction script with your desired options:

```bash
python3 scripts/pdf_to_content.py --input <pdf_path> --format <output_format> [--extract-images] [--output-dir <dir>]
```

**Example:**
```bash
python3 scripts/pdf_to_content.py --input ./docs/report.pdf --format markdown --extract-images --output-dir ./extracted_content
```

### Step 3: Review the extraction output
The script generates:
- **Markdown output**: Structured text with headings, tables converted to markdown format, and image references
- **JSON output**: Structured data with page-by-page content, metadata, and extracted elements
- **Text output**: Plain text extraction (simplest format)
- **Images** (if enabled): Extracted images saved as PNG files

### Step 4: Process for agent consumption
Read the [`references/content_structure.md`](references/content_structure.md) guide to understand how content is structured for agent reasoning.

## File references
- [`scripts/pdf_to_content.py`](scripts/pdf_to_content.py) - Main extraction script (execute to convert PDFs)
- [`references/content_structure.md`](references/content_structure.md) - Content structure reference (read when processing output)
- [`references/known_issues.md`](references/known_issues.md) - Known limitations and edge cases (read when extraction fails)

## Expected output structure

### Markdown format
```markdown
# Document Title

## Page 1
Content text...

### Table 1
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

![Figure 1](images/page1_figure1.png)

## Page 2
...
```

### JSON format
```json
{
  "metadata": {
    "title": "...",
    "author": "...",
    "page_count": 10
  },
  "pages": [
    {
      "page_number": 1,
      "text": "...",
      "tables": [...],
      "images": ["images/page1_1.png"]
    }
  ]
}
```

## Troubleshooting

### Password-protected PDFs
If the PDF is password-protected, you must provide the password:
```bash
python3 scripts/pdf_to_content.py --input <pdf_path> --password <password> --format markdown
```

### Scanned PDFs (no text layer)
For scanned images, the script will detect this and suggest OCR. Install OCR dependencies:
```bash
pip install pytesseract
sudo apt install tesseract-ocr  # Linux
brew install tesseract          # macOS
```

### Table extraction issues
Complex tables may not extract perfectly. Check [`references/known_issues.md`](references/known_issues.md) for manual table formatting guidance.

### Large PDFs (>100 pages)
For very large PDFs, process in chunks:
```bash
python3 scripts/pdf_to_content.py --input <pdf_path> --format markdown --page-range 1-50
python3 scripts/pdf_to_content.py --input <pdf_path> --format markdown --page-range 51-100
```

## Dependencies
The following Python packages are required:
- `pypdf` or `pdfplumber` - PDF parsing
- `markdown` - Markdown formatting
- `Pillow` - Image extraction (optional)

Install with:
```bash
pip install pypdf pdfplumber markdown Pillow
```
