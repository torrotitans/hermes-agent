#!/usr/bin/env python3
"""
FN:pdf_to_content.py
PDF to Content Conversion Script

Classes:
- PDFContentExtractor: Main class for extracting content from PDFs

Functions:
- FN:extract_text: Extract text content from PDF
- FN:extract_tables: Extract tables from PDF
- FN:extract_images: Extract embedded images from PDF
- FN:convert_to_markdown: Convert extracted content to markdown
- FN:convert_to_json: Convert extracted content to JSON
- FN:main: Main entry point with CLI argument parsing
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is required. Install with: pip install pdfplumber")
    sys.exit(1)

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class PDFContentExtractor:
    """
    Extract content from PDF files including text, tables, and images.
    Converts content into agent-readable formats (markdown, JSON, text).
    """

    def __init__(self, pdf_path: str, password: Optional[str] = None):
        """
        FN:__init__
        Initialize the PDF extractor.

        Args:
            pdf_path: Path to the PDF file
            password: Optional password for encrypted PDFs
        """
        self.pdf_path = Path(pdf_path)
        self.password = password
        self.pdf = None
        self.metadata: Dict[str, Any] = {}

    def open_pdf(self) -> bool:
        """
        FN:open_pdf
        Open and validate the PDF file.

        Returns:
            True if PDF opened successfully, False otherwise
        """
        try:
            self.pdf = pdfplumber.open(self.pdf_path, password=self.password)
            self.metadata = {
                "filename": self.pdf_path.name,
                "page_count": len(self.pdf.pages),
                "metadata": self.pdf.metadata or {}
            }
            return True
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return False

    def close_pdf(self) -> None:
        """
        FN:close_pdf
        Close the PDF file handle.
        """
        if self.pdf:
            self.pdf.close()

    def extract_text(self, page_numbers: Optional[List[int]] = None) -> List[str]:
        """
        FN:extract_text
        Extract text content from PDF pages.

        Args:
            page_numbers: Optional list of page numbers to extract (0-indexed)

        Returns:
            List of text content per page
        """
        if not self.pdf:
            return []

        texts = []
        pages_to_process = range(len(self.pdf.pages))
        if page_numbers:
            pages_to_process = [p for p in page_numbers if 0 <= p < len(self.pdf.pages)]

        for i, page in enumerate(self.pdf.pages):
            if i not in pages_to_process:
                continue
            text = page.extract_text() or ""
            texts.append(text.strip())

        return texts

    def extract_tables(self, page_numbers: Optional[List[int]] = None) -> List[List[List[str]]]:
        """
        FN:extract_tables
        Extract tables from PDF pages.

        Args:
            page_numbers: Optional list of page numbers to extract

        Returns:
            List of tables per page (each table is a list of rows)
        """
        if not self.pdf:
            return []

        all_tables = []
        pages_to_process = range(len(self.pdf.pages))
        if page_numbers:
            pages_to_process = [p for p in page_numbers if 0 <= p < len(self.pdf.pages)]

        for i, page in enumerate(self.pdf.pages):
            if i not in pages_to_process:
                continue
            tables = page.extract_tables()
            all_tables.append(tables or [])

        return all_tables

    def extract_images(self, output_dir: str, page_numbers: Optional[List[int]] = None) -> Dict[int, List[str]]:
        """
        FN:extract_images
        Extract embedded images from PDF pages.

        Args:
            output_dir: Directory to save extracted images
            page_numbers: Optional list of page numbers to extract

        Returns:
            Dict mapping page number to list of image file paths
        """
        if not self.pdf or not PILLOW_AVAILABLE:
            return {}

        os.makedirs(output_dir, exist_ok=True)
        image_map: Dict[int, List[str]] = {}

        pages_to_process = range(len(self.pdf.pages))
        if page_numbers:
            pages_to_process = [p for p in page_numbers if 0 <= p < len(self.pdf.pages)]

        for i, page in enumerate(self.pdf.pages):
            if i not in pages_to_process:
                continue

            images = []
            try:
                page_images = page.images
                for j, img in enumerate(page_images):
                    # Extract image bytes
                    xobj = page.xobjects.get(img["xobject"])
                    if xobj:
                        image_data = xobj["flatteneddata"]
                        img_path = os.path.join(output_dir, f"page{i+1}_img{j+1}.png")
                        with open(img_path, "wb") as f:
                            f.write(image_data)
                        images.append(f"images/page{i+1}_img{j+1}.png")
            except Exception as e:
                print(f"Warning: Could not extract image from page {i+1}: {e}")

            if images:
                image_map[i] = images

        return image_map

    def convert_to_markdown(self, page_numbers: Optional[List[int]] = None) -> str:
        """
        FN:convert_to_markdown
        Convert extracted content to markdown format.

        Args:
            page_numbers: Optional list of page numbers to include

        Returns:
            Markdown formatted string
        """
        if not self.pdf:
            return ""

        lines = []

        # Add metadata header
        lines.append(f"# {self.metadata.get('filename', 'Document')}")
        lines.append("")
        if self.metadata.get("metadata", {}).get("title"):
            lines.append(f"**Title:** {self.metadata['metadata']['title']}")
        if self.metadata.get("metadata", {}).get("author"):
            lines.append(f"**Author:** {self.metadata['metadata']['author']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        texts = self.extract_text(page_numbers)
        tables = self.extract_tables(page_numbers)

        for i, (text, page_tables) in enumerate(zip(texts, tables)):
            lines.append(f"## Page {i + 1}")
            lines.append("")

            # Add text content
            if text:
                # Clean up text and convert to markdown-friendly format
                cleaned_text = self._clean_text_for_markdown(text)
                lines.append(cleaned_text)
                lines.append("")

            # Add tables
            for t_idx, table in enumerate(page_tables):
                if table:
                    lines.append(f"### Table {t_idx + 1}")
                    lines.append("")
                    lines.extend(self._table_to_markdown(table))
                    lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def _clean_text_for_markdown(self, text: str) -> str:
        """
        FN:_clean_text_for_markdown
        Clean text for markdown formatting.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        # Normalize whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        # Detect and format headings
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) < 60 and not stripped.endswith(('.', '!', '?')):
                # Likely a heading
                formatted_lines.append(f"### {stripped}")
            else:
                formatted_lines.append(stripped)

        return '\n'.join(formatted_lines)

    def _table_to_markdown(self, table: List[List[str]]) -> List[str]:
        """
        FN:_table_to_markdown
        Convert a table to markdown format.

        Args:
            table: List of rows, each row is a list of cells

        Returns:
            List of markdown table lines
        """
        lines = []

        # Header row
        if table:
            header = table[0]
            lines.append("| " + " | ".join(str(cell) for cell in header) + " |")
            lines.append("| " + " | ".join(["---"] * len(header)) + " |")

            # Data rows
            for row in table[1:]:
                lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        return lines

    def convert_to_json(self, page_numbers: Optional[List[int]] = None,
                        extract_images: bool = False,
                        image_output_dir: Optional[str] = None) -> str:
        """
        FN:convert_to_json
        Convert extracted content to JSON format.

        Args:
            page_numbers: Optional list of page numbers to include
            extract_images: Whether to extract images
            image_output_dir: Directory for extracted images

        Returns:
            JSON string
        """
        if not self.pdf:
            return "{}"

        result: Dict[str, Any] = {
            "metadata": {
                "filename": self.metadata.get("filename", ""),
                "page_count": self.metadata.get("page_count", 0),
                "pdf_metadata": self.metadata.get("metadata", {})
            },
            "pages": []
        }

        texts = self.extract_text(page_numbers)
        tables = self.extract_tables(page_numbers)

        pages_to_process = range(len(self.pdf.pages))
        if page_numbers:
            pages_to_process = [p for p in page_numbers if 0 <= p < len(self.pdf.pages)]

        for i, (text, page_tables) in enumerate(zip(texts, tables)):
            page_data: Dict[str, Any] = {
                "page_number": i + 1,
                "text": text,
                "tables": []
            }

            # Add tables
            for table in page_tables:
                if table:
                    page_data["tables"].append({
                        "rows": table
                    })

            # Extract images if requested
            if extract_images and image_output_dir:
                images = self.extract_images(image_output_dir, [i])
                if i in images:
                    page_data["images"] = images[i]

            result["pages"].append(page_data)

        return json.dumps(result, indent=2, ensure_ascii=False)

    def convert_to_text(self, page_numbers: Optional[List[int]] = None) -> str:
        """
        FN:convert_to_text
        Extract plain text from PDF.

        Args:
            page_numbers: Optional list of page numbers to include

        Returns:
            Plain text string
        """
        texts = self.extract_text(page_numbers)
        return "\n\n".join(texts)


def main():
    """
    FN:main
    Main entry point with CLI argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Convert PDF documents to agent-readable content formats"
    )
    parser.add_argument("--input", "-i", required=True, help="Path to input PDF file")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "text"],
                        default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", "-o", help="Output file path (default: auto-generated)")
    parser.add_argument("--output-dir", "-d", help="Output directory for images and related files")
    parser.add_argument("--extract-images", "-e", action="store_true",
                        help="Extract embedded images")
    parser.add_argument("--password", "-p", help="Password for encrypted PDFs")
    parser.add_argument("--page-range", help="Page range to extract (e.g., '1-5' or '1,3,5')")
    parser.add_argument("--info", "-I", action="store_true",
                        help="Show PDF metadata without extracting content")

    args = parser.parse_args()

    # Parse page range if provided
    page_numbers = None
    if args.page_range:
        page_numbers = _parse_page_range(args.page_range)

    # Initialize extractor
    extractor = PDFContentExtractor(args.input, password=args.password)

    # Open PDF
    if not extractor.open_pdf():
        sys.exit(1)

    # Show info mode
    if args.info:
        print(f"PDF: {extractor.metadata.get('filename')}")
        print(f"Pages: {extractor.metadata.get('page_count')}")
        meta = extractor.metadata.get("metadata", {})
        for key, value in meta.items():
            print(f"  {key}: {value}")
        extractor.close_pdf()
        sys.exit(0)

    # Determine output directory for images
    image_output_dir = None
    if args.extract_images:
        image_output_dir = args.output_dir or os.path.dirname(args.input) or "."
        os.makedirs(image_output_dir, exist_ok=True)

    # Convert to requested format
    if args.format == "markdown":
        content = extractor.convert_to_markdown(page_numbers)
        ext = ".md"
    elif args.format == "json":
        content = extractor.convert_to_json(page_numbers, args.extract_images, image_output_dir)
        ext = ".json"
    else:
        content = extractor.convert_to_text(page_numbers)
        ext = ".txt"

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base_name = Path(args.input).stem
        output_dir = args.output_dir or Path(args.input).parent
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{base_name}_content{ext}")

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully extracted content to: {output_path}")

    if args.extract_images and image_output_dir:
        print(f"Images extracted to: {image_output_dir}")

    extractor.close_pdf()


def _parse_page_range(range_str: str) -> List[int]:
    """
    FN:_parse_page_range
    Parse page range string into list of page numbers.

    Args:
        range_str: Range string (e.g., '1-5' or '1,3,5')

    Returns:
        List of page numbers (0-indexed)
    """
    pages = []
    parts = range_str.split(",")

    for part in parts:
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            pages.extend(range(int(start) - 1, int(end)))
        else:
            pages.append(int(part) - 1)

    return sorted(set(pages))


if __name__ == "__main__":
    main()
