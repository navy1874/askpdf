# PDF Reader CLI

A minimal Python CLI for reading, managing, and lightly analyzing PDF files. Ships with common tasks: metadata inspection, text extraction, splitting, and merging.

## Installation

```bash
pip install --upgrade pip
pip install -e .
```

## Commands

```bash
pdfreader info <file.pdf>
# show pages, encryption status, and metadata

pdfreader extract-text <file.pdf> --pages "1,3-5" --output text.txt
# extract text from selected pages (all pages if omitted)

pdfreader split <file.pdf> "1,4-6" --output subset.pdf
# keep only selected pages

pdfreader merge output.pdf file1.pdf file2.pdf [...]
# merge multiple PDFs
```

Page ranges are 1-based and accept comma/range syntax like `1,3-5`.

## Desktop UI path (optional)

- Stack: PySide6 (Qt) for native desktop; reuse the core logic in `pdf_reader`.
- Features to add: file browser + preview (render via `pdf2image`), metadata panel, text search, drag-and-drop merge/split, task progress.
- Packaging: use `fbs`/`briefcase`/`PyInstaller` once the UI stabilizes.

## Roadmap ideas

- Indexing and search (plain text with Whoosh/Tantivy; semantic with sentence-transformers + FAISS/Chroma).
- OCR for scanned PDFs (pytesseract + pdf2image) as optional add-on.
- Summaries/keywords using HuggingFace transformers for long documents.
- Table extraction (camelot/tabula-py) when needed.
