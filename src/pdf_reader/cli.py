from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import pdfplumber
import typer
from pypdf import PdfReader, PdfWriter
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="PDF reader/manager CLI")
console = Console()


def parse_page_ranges(pages: Optional[str], total_pages: int) -> List[int]:
    """Convert a 1-based range string like "1,3-5" into zero-based page indexes."""
    if not pages:
        return list(range(total_pages))

    result: List[int] = []
    for part in pages.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start < 1 or end < start:
                raise typer.BadParameter(f"Invalid page range: {part}")
            for page in range(start, end + 1):
                if page > total_pages:
                    raise typer.BadParameter(f"Page {page} exceeds total pages ({total_pages})")
                result.append(page - 1)
        else:
            page = int(part)
            if page < 1 or page > total_pages:
                raise typer.BadParameter(f"Page {page} out of bounds (1-{total_pages})")
            result.append(page - 1)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for idx in result:
        if idx not in seen:
            unique.append(idx)
            seen.add(idx)
    return unique


@app.command()
def info(pdf: Path) -> None:
    """Show metadata and basic stats for a PDF."""
    reader = PdfReader(str(pdf))
    metadata = reader.metadata or {}

    table = Table(title=str(pdf), show_lines=True)
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Pages", str(len(reader.pages)))
    table.add_row("Encrypted", str(reader.is_encrypted))

    if metadata:
        for key, value in metadata.items():
            table.add_row(key.lstrip("/"), str(value))
    else:
        table.add_row("Metadata", "<none>")

    console.print(table)


@app.command("extract-text")
def extract_text(
    pdf: Path,
    pages: Optional[str] = typer.Option(None, help="Page ranges like '1,3-5'; default all"),
    output: Optional[Path] = typer.Option(None, help="Write extracted text to file"),
) -> None:
    """Extract text from selected pages."""
    with pdfplumber.open(str(pdf)) as doc:
        indexes = parse_page_ranges(pages, len(doc.pages))
        texts = []
        for idx in indexes:
            text = doc.pages[idx].extract_text() or ""
            texts.append(text)

    combined = "\n\n".join(texts)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(combined, encoding="utf-8")
        console.print(f"Wrote text to {output}")
    else:
        console.print(combined)


@app.command()
def split(
    pdf: Path,
    pages: str = typer.Argument(..., help="Page ranges like '1,3-5'"),
    output: Path = typer.Option(..., help="Output PDF path"),
) -> None:
    """Split selected pages into a new PDF."""
    reader = PdfReader(str(pdf))
    indexes = parse_page_ranges(pages, len(reader.pages))

    writer = PdfWriter()
    for idx in indexes:
        writer.add_page(reader.pages[idx])

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as f:
        writer.write(f)
    console.print(f"Wrote split PDF to {output}")


@app.command()
def merge(
    output: Path = typer.Argument(..., help="Output PDF path"),
    pdfs: List[Path] = typer.Argument(..., help="PDF files to merge"),
) -> None:
    """Merge multiple PDFs into one."""
    writer = PdfWriter()
    for pdf in pdfs:
        reader = PdfReader(str(pdf))
        for page in reader.pages:
            writer.add_page(page)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as f:
        writer.write(f)
    console.print(f"Wrote merged PDF to {output}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
