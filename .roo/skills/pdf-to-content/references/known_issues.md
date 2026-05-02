# PDF to Content - Known Issues and Limitations

This document lists known issues, edge cases, and workarounds for the PDF to Content conversion skill.

## Common Issues

### 1. Scanned PDFs (Image-only)

**Symptom:** Extracted text is empty or contains garbage characters.

**Cause:** The PDF contains only images without a text layer (OCR has not been performed).

**Workaround:**
```bash
# Install OCR dependencies
pip install pytesseract
# macOS
brew install tesseract poppler
# Ubuntu/Debian
sudo apt install tesseract-ocr poppler-utils

# Then use OCR-enabled extraction (if available)
python3 scripts/pdf_to_content.py --input <pdf> --ocr --format markdown
```

### 2. Password-Protected PDFs

**Symptom:** Error message about encryption or password required.

**Cause:** The PDF is encrypted and requires a password to open.

**Workaround:**
```bash
python3 scripts/pdf_to_content.py --input <pdf> --password <your_password> --format markdown
```

### 3. Complex Table Formatting

**Symptom:** Tables appear misaligned or merged incorrectly.

**Cause:** PDF tables with merged cells, nested structures, or irregular borders.

**Manual Fix:**
1. Extract the raw table data
2. Manually reconstruct the table structure
3. Use the following pattern for complex tables:

```markdown
### Table 1 (Manual Reconstruction)

**Section A:**
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

**Section B:**
| Column A | Column B |
|----------|----------|
| Data A   | Data B   |
```

### 4. Multi-Column Layouts

**Symptom:** Text from different columns appears interleaved or out of order.

**Cause:** PDF readers may read text in a non-visual order.

**Workaround:**
- Process the PDF in smaller page ranges
- Manually reorganize text sections after extraction
- Consider using a layout-aware PDF parser for complex documents

### 5. Special Characters and Encoding

**Symptom:** Strange characters, question marks, or missing text.

**Cause:** Non-standard fonts or encoding issues in the source PDF.

**Workaround:**
- Check the PDF's font embedding status
- Try extracting with different encoding options
- Manually correct known character mappings

### 6. Large PDF Performance

**Symptom:** Script runs slowly or runs out of memory.

**Cause:** PDFs with hundreds of pages or embedded high-resolution images.

**Workaround:**
```bash
# Process in chunks
python3 scripts/pdf_to_content.py --input <pdf> --page-range 1-50 --format markdown
python3 scripts/pdf_to_content.py --input <pdf> --page-range 51-100 --format markdown
# Combine outputs manually
```

### 7. Image Extraction Failures

**Symptom:** Images are not extracted or are corrupted.

**Cause:** Vector graphics, embedded fonts, or non-standard image formats.

**Workaround:**
- Vector graphics may need to be rendered to raster first
- Check PDF for image object types
- Use alternative extraction tools for complex graphics

## PDF Type Compatibility

| PDF Type | Text Extraction | Table Extraction | Image Extraction |
|----------|-----------------|------------------|------------------|
| Text-based PDF | ✅ Excellent | ✅ Good | ✅ Good |
| Scanned PDF (no OCR) | ❌ Fails | ❌ Fails | ✅ Good |
| Scanned PDF (with OCR) | ✅ Good | ⚠️ Limited | ✅ Good |
| Form-based PDF | ✅ Good | ⚠️ Variable | ✅ Good |
| Presentation PDF | ✅ Good | ✅ Good | ✅ Excellent |
| Academic Paper | ✅ Good | ⚠️ Complex | ✅ Good |

## Error Messages and Solutions

### "PDF is encrypted"
```
Solution: Provide the password using --password flag
```

### "No text found on page"
```
Solution: Page may be image-only. Check if OCR is available or skip the page.
```

### "Table extraction returned empty"
```
Solution: Table may not be recognized as a table structure. Try manual extraction.
```

### "Image extraction failed"
```
Solution: Image may be a vector graphic. Install additional dependencies or skip extraction.
```

## Best Practices

1. **Validate PDF first:** Use `--info` flag to check PDF properties before extraction.
2. **Test with small range:** Extract a few pages first to verify quality.
3. **Review output:** Always review extracted content for accuracy.
4. **Keep originals:** Preserve original PDF files for reference.
5. **Document issues:** Note any extraction problems for future reference.

## Reporting New Issues

If you encounter an issue not listed here:
1. Note the PDF filename and characteristics
2. Record the exact error message
3. Include a sample of the problematic content
4. Report to the skill maintainer for investigation
