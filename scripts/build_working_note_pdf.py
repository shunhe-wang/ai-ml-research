#!/usr/bin/env python3
"""Render the working-note Markdown subset to a polished, deterministic PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

INK = colors.HexColor("#172235")
MUTED = colors.HexColor("#5C6878")
TEAL = colors.HexColor("#147D83")
PALE = colors.HexColor("#EAF4F3")
GRID = colors.HexColor("#CAD3DA")
ALT = colors.HexColor("#F5F7F8")
ALERT = colors.HexColor("#F7F0E4")


def register_fonts() -> tuple[str, str, str, str]:
    candidates = [
        (
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
        ),
        (
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf",
        ),
    ]
    for regular, bold, italic, bold_italic in candidates:
        if all(Path(p).exists() for p in (regular, bold, italic, bold_italic)):
            pdfmetrics.registerFont(TTFont("Body", regular))
            pdfmetrics.registerFont(TTFont("Body-Bold", bold))
            pdfmetrics.registerFont(TTFont("Body-Italic", italic))
            pdfmetrics.registerFont(TTFont("Body-BoldItalic", bold_italic))
            pdfmetrics.registerFontFamily(
                "Body",
                normal="Body",
                bold="Body-Bold",
                italic="Body-Italic",
                boldItalic="Body-BoldItalic",
            )
            return "Body", "Body-Bold", "Body-Italic", "Body-BoldItalic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique"


REGULAR, BOLD, ITALIC, BOLD_ITALIC = register_fonts()


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName=BOLD,
            fontSize=25,
            leading=29,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["Heading2"],
            fontName=REGULAR,
            fontSize=14.5,
            leading=19,
            textColor=TEAL,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=18,
        ),
        "h2": ParagraphStyle(
            "H2Custom",
            parent=base["Heading2"],
            fontName=BOLD,
            fontSize=15,
            leading=18,
            textColor=INK,
            spaceBefore=4,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3Custom",
            parent=base["Heading3"],
            fontName=BOLD,
            fontSize=11.2,
            leading=14,
            textColor=TEAL,
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["BodyText"],
            fontName=REGULAR,
            fontSize=9.15,
            leading=12.1,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=5.2,
            allowWidows=0,
            allowOrphans=0,
        ),
        "meta": ParagraphStyle(
            "MetaCustom",
            parent=base["BodyText"],
            fontName=REGULAR,
            fontSize=9.4,
            leading=13,
            textColor=MUTED,
            spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "BulletCustom",
            parent=base["BodyText"],
            fontName=REGULAR,
            fontSize=8.95,
            leading=11.6,
            textColor=INK,
            alignment=TA_LEFT,
            leftIndent=1,
            firstLineIndent=0,
            spaceAfter=1.8,
        ),
        "quote": ParagraphStyle(
            "QuoteCustom",
            parent=base["BodyText"],
            fontName=REGULAR,
            fontSize=9.3,
            leading=12.4,
            textColor=INK,
            leftIndent=8,
            rightIndent=8,
            borderColor=TEAL,
            borderWidth=1,
            borderPadding=9,
            backColor=PALE,
            spaceBefore=12,
            spaceAfter=10,
        ),
        "table": ParagraphStyle(
            "TableCustom",
            parent=base["BodyText"],
            fontName=REGULAR,
            fontSize=7.4,
            leading=9.2,
            textColor=INK,
            alignment=TA_LEFT,
        ),
        "table_header": ParagraphStyle(
            "TableHeaderCustom",
            parent=base["BodyText"],
            fontName=BOLD,
            fontSize=7.5,
            leading=9.2,
            textColor=colors.white,
            alignment=TA_LEFT,
        ),
        "small": ParagraphStyle(
            "SmallCustom",
            parent=base["BodyText"],
            fontName=REGULAR,
            fontSize=7.5,
            leading=9.5,
            textColor=MUTED,
            spaceAfter=2,
        ),
    }


STYLES = make_styles()


def inline_markup(value: str) -> str:
    value = html.escape(value.strip(), quote=True)
    value = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#147D83">\1</link>',
        value,
    )
    value = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    value = re.sub(
        r"(?<!href=&quot;)(https?://[^\s<]+)",
        r'<link href="\1" color="#147D83">\1</link>',
        value,
    )
    return value


def table_widths(rows: list[list[str]], width: float) -> list[float]:
    count = len(rows[0])
    if count == 2:
        return [width * 0.62, width * 0.38]
    if count == 3:
        return [width * 0.38, width * 0.31, width * 0.31]
    if count == 4:
        return [width * 0.28, width * 0.17, width * 0.17, width * 0.38]
    if count == 6:
        return [width * 0.27] + [width * 0.146] * 5
    if count == 7:
        return [width * 0.29] + [width * (0.71 / 6)] * 6
    return [width / count] * count


def make_table(rows: list[list[str]], available_width: float) -> Table:
    data: list[list[Paragraph]] = []
    for row_index, row in enumerate(rows):
        style = STYLES["table_header"] if row_index == 0 else STYLES["table"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(
        data,
        colWidths=table_widths(rows, available_width),
        repeatRows=1,
        hAlign="LEFT",
    )
    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for index in range(1, len(rows)):
        if index % 2 == 0:
            commands.append(("BACKGROUND", (0, index), (-1, index), ALT))
    table.setStyle(TableStyle(commands))
    return table


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        row = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        rows.append(row)
        index += 1
    if len(rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        rows.pop(1)
    return rows, index


def parse_list(lines: list[str], start: int, ordered: bool) -> tuple[ListFlowable, int]:
    items: list[ListItem] = []
    index = start
    pattern = r"^\d+\.\s+" if ordered else r"^-\s+"
    while index < len(lines) and re.match(pattern, lines[index].strip()):
        text = re.sub(pattern, "", lines[index].strip())
        paragraph = Paragraph(inline_markup(text), STYLES["bullet"])
        items.append(ListItem(paragraph, leftIndent=10))
        index += 1
    flow = ListFlowable(
        items,
        bulletType="1" if ordered else "bullet",
        start="1" if ordered else None,
        leftIndent=16,
        bulletFontName=BOLD,
        bulletFontSize=7.5,
        bulletColor=TEAL,
        bulletChar="bullet",
        spaceAfter=5,
    )
    return flow, index


def markdown_to_story(markdown: str, available_width: float) -> list:
    lines = markdown.splitlines()
    story: list = []
    index = 0
    first_h1 = True
    first_h2 = True
    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        if not stripped:
            index += 1
            continue
        if stripped == "<!-- PAGEBREAK -->":
            story.append(PageBreak())
            index += 1
            continue
        if stripped.startswith("# "):
            story.append(Spacer(1, 23 * mm if first_h1 else 0))
            story.append(Paragraph(inline_markup(stripped[2:]), STYLES["title"]))
            first_h1 = False
            index += 1
            continue
        if stripped.startswith("## "):
            style = STYLES["subtitle"] if first_h2 else STYLES["h2"]
            story.append(Paragraph(inline_markup(stripped[3:]), style))
            first_h2 = False
            index += 1
            continue
        if stripped.startswith("### "):
            story.append(Paragraph(inline_markup(stripped[4:]), STYLES["h3"]))
            index += 1
            continue
        if stripped.startswith("> "):
            quote_parts: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("> "):
                quote_parts.append(lines[index].strip()[2:])
                index += 1
            story.append(Paragraph(inline_markup(" ".join(quote_parts)), STYLES["quote"]))
            continue
        if stripped.startswith("|"):
            rows, index = parse_table(lines, index)
            story.append(Spacer(1, 3))
            story.append(make_table(rows, available_width))
            story.append(Spacer(1, 7))
            continue
        if stripped.startswith("- "):
            flow, index = parse_list(lines, index, ordered=False)
            story.append(flow)
            continue
        if re.match(r"^\d+\.\s+", stripped):
            flow, index = parse_list(lines, index, ordered=True)
            story.append(flow)
            continue

        paragraph_parts = [stripped]
        index += 1
        while index < len(lines) and lines[index].strip():
            candidate = lines[index].strip()
            if candidate.startswith(("#", "|", "> ", "- ", "<!-- PAGEBREAK")) or re.match(
                r"^\d+\.\s+", candidate
            ):
                break
            paragraph_parts.append(candidate)
            index += 1
        text = " ".join(paragraph_parts)
        is_metadata = text.startswith(("**Working draft", "**Technical", "**Version"))
        style = STYLES["meta"] if is_metadata else STYLES["body"]
        story.append(Paragraph(inline_markup(text), style))
    return story


class NoteDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs) -> None:
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="note", frames=[frame], onPage=draw_page))


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    page = canvas.getPageNumber()
    width, height = A4
    if page == 1:
        canvas.setFillColor(TEAL)
        canvas.rect(0, height - 13 * mm, width, 13 * mm, stroke=0, fill=1)
        canvas.setFillColor(INK)
        canvas.rect(0, 0, width, 5 * mm, stroke=0, fill=1)
    else:
        canvas.setStrokeColor(GRID)
        canvas.setLineWidth(0.45)
        canvas.line(doc.leftMargin, height - 18 * mm, width - doc.rightMargin, height - 18 * mm)
        canvas.setFont(BOLD, 7.3)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, height - 14.5 * mm, "BEFORE MEASURING CONTEXT CARRYOVER")
        canvas.setFont(REGULAR, 7.3)
        canvas.drawRightString(
            width - doc.rightMargin,
            height - 14.5 * mm,
            "UNREVIEWED TECHNICAL REPORT",
        )
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.35)
    canvas.line(doc.leftMargin, 14 * mm, width - doc.rightMargin, 14 * mm)
    canvas.setFont(REGULAR, 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 9.5 * mm, "Authenticated methods/resource case study")
    canvas.drawRightString(width - doc.rightMargin, 9.5 * mm, str(page))
    canvas.restoreState()


def build(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = NoteDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title="Before Measuring Context Carryover",
        author="Independent research artifact",
        subject="Pre-confirmatory evaluation harness and negative design case",
        invariant=True,
    )
    story = markdown_to_story(source.read_text(encoding="utf-8"), doc.width)
    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
