#!/usr/bin/env python3
"""
IfeSec Portfolio PDF Generator — HTML → Chromium → PDF

Reads source markdown from the AtlasPay GRC sandbox and produces
board-ready PDFs using HTML + CSS rendered through Chromium.

Why this exists: reportlab v2 had text-box overflow, shape overlap,
and chart legibility issues. HTML+Chromium eliminates all of those
because CSS handles layout natively.

Pipeline:
1. Read source markdown
2. Parse to HTML (simple, no external deps)
3. Apply page templates (cover / divider / content)
4. Render to PDF via Playwright Chromium

Usage:
  python3 generate_pdf_html.py <source.md> <output.pdf> <doc_type>

  doc_type: 'executive_briefing' | 'risk_register' | 'control_mapping'
"""
import os
import re
import sys
import argparse
from pathlib import Path

# Brand colors (IfeSec)
BLACK = "#0F0F10"
GOLD = "#D4AF37"
GOLD_LIGHT = "#C9A961"
CRIMSON = "#B22234"
DARK_GRAY = "#1A1A1A"
MED_GRAY = "#4A4A4A"
LIGHT_GRAY = "#6A6A6A"
PAPER_GRAY = "#FAFAFA"
RULE_GRAY = "#D0D0D0"

STATUS_COLORS = {
    'covered': {'bg': '#2E7D32', 'fg': '#FFFFFF', 'icon': '✓'},
    'partial': {'bg': '#F57C00', 'fg': '#FFFFFF', 'icon': '⚠'},
    'missing': {'bg': '#C62828', 'fg': '#FFFFFF', 'icon': '✗'},
    'lab-synthetic': {'bg': '#FBC02D', 'fg': '#1A1A1A', 'icon': '◆'},
}


def md_to_html(md_text: str) -> str:
    """Convert source markdown to HTML. Simple but adequate for our docs."""
    lines = md_text.split('\n')
    out = []
    in_code = False
    in_table = False
    in_list = False
    list_type = None  # 'ul' or 'ol'
    para_buf = []

    def flush_para():
        nonlocal para_buf
        if para_buf:
            text = ' '.join(para_buf).strip()
            if text:
                out.append(f'<p>{inline_format(text)}</p>')
            para_buf = []

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            out.append(f'</{list_type}>')
            in_list = False
            list_type = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code fence
        if stripped.startswith('```'):
            flush_para()
            flush_list()
            if not in_code:
                out.append('<pre><code>')
                in_code = True
            else:
                out.append('</code></pre>')
                in_code = False
            i += 1
            continue

        if in_code:
            # Escape HTML in code
            safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            out.append(safe)
            i += 1
            continue

        # Table detection (header row with | separators followed by |---|---|)
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|', lines[i + 1]):
            flush_para()
            flush_list()
            in_table = True
            header_cells = [c.strip() for c in line.strip().strip('|').split('|')]
            # Detect matrix tables (have "Negligible" or "Likelihood" in header)
            is_matrix = any('Negligible' in c or 'Likelihood' in c for c in header_cells)
            table_class = ' class="matrix-table"' if is_matrix else ''
            out.append(f'<table{table_class}>')
            out.append('<thead><tr>')
            for c in header_cells:
                out.append(f'<th>{c}</th>')
            out.append('</tr></thead>')
            out.append('<tbody>')
            i += 2  # skip header + separator
            continue

        if in_table and '|' in line:
            row_cells = [c.strip() for c in line.strip().strip('|').split('|')]
            out.append('<tr>')
            for c in row_cells:
                # Apply styling based on content
                cell_html = inline_format(c)

                # Treatment badges
                if c.strip() in ('Mitigate',):
                    cell_html = '<span class="treatment-mitigate">Mitigate</span>'
                elif c.strip() in ('Accept', 'Accept (with mitigation)'):
                    cell_html = '<span class="treatment-accept">Accept</span>'
                # Status badges
                elif c.startswith('✅') or c.startswith('Covered'):
                    cell_html = f'<span class="status status-covered">{cell_html}</span>'
                elif c.startswith('⚠') or c.startswith('Partial'):
                    cell_html = f'<span class="status status-partial">{cell_html}</span>'
                elif c.startswith('❌') or c.strip() == 'Missing':
                    cell_html = f'<span class="status status-missing">{cell_html}</span>'
                # Severity levels (whole-cell styling)
                elif c.strip() in ('Low', 'Low (2)'):
                    cell_html = '<span class="severity-low">Low (2)</span>' if '(2)' in c else '<span class="severity-low">Low</span>'
                elif c.strip() in ('Medium', 'Medium (3)'):
                    cell_html = '<span class="severity-medium">Medium (3)</span>' if '(3)' in c else '<span class="severity-medium">Medium</span>'
                elif c.strip() in ('High', 'High (4)'):
                    cell_html = '<span class="severity-high">High (4)</span>' if '(4)' in c else '<span class="severity-high">High</span>'
                elif c.strip() in ('Very High', 'Very High (5)'):
                    cell_html = '<span class="severity-very-high">Very High (5)</span>' if '(5)' in c else '<span class="severity-very-high">Very High</span>'

                if '[LAB-SYNTHETIC]' in c:
                    cell_html = cell_html.replace('[LAB-SYNTHETIC]', '<span class="lab-tag">[LAB-SYNTHETIC]</span>')
                out.append(f'<td>{cell_html}</td>')
            out.append('</tr>')
            i += 1
            continue

        if in_table and not '|' in line:
            in_table = False
            out.append('</tbody></table>')

        # Headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            flush_para()
            flush_list()
            level = len(m.group(1))
            content = inline_format(m.group(2))
            out.append(f'<h{level}>{content}</h{level}>')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^\s*---\s*$', line):
            flush_para()
            flush_list()
            out.append('<hr>')
            i += 1
            continue

        # Unordered list
        if re.match(r'^\s*[-*]\s+', line):
            flush_para()
            if not in_list or list_type != 'ul':
                flush_list()
                out.append('<ul>')
                in_list = True
                list_type = 'ul'
            content = re.sub(r'^\s*[-*]\s+', '', line)
            out.append(f'<li>{inline_format(content)}</li>')
            i += 1
            continue

        # Ordered list
        if re.match(r'^\s*\d+\.\s+', line):
            flush_para()
            if not in_list or list_type != 'ol':
                flush_list()
                out.append('<ol>')
                in_list = True
                list_type = 'ol'
            content = re.sub(r'^\s*\d+\.\s+', '', line)
            out.append(f'<li>{inline_format(content)}</li>')
            i += 1
            continue

        # Empty line - paragraph break
        if not stripped:
            flush_para()
            flush_list()
            i += 1
            continue

        # HTML block (raw HTML like <div class="...">...</div>)
        if stripped.startswith('<') and '>' in stripped:
            flush_para()
            flush_list()
            # Find the matching closing tag
            tag_match = re.match(r'<(\w+)', stripped)
            if tag_match:
                tag_name = tag_match.group(1)
                close_tag = f'</{tag_name}>'
                # Single-line HTML
                if close_tag in stripped:
                    out.append(stripped)
                    i += 1
                    continue
                # Multi-line HTML — collect until close
                html_lines = [stripped]
                i += 1
                while i < len(lines):
                    if close_tag in lines[i]:
                        html_lines.append(lines[i])
                        i += 1
                        break
                    html_lines.append(lines[i])
                    i += 1
                out.append('\n'.join(html_lines))
                continue

        # Regular paragraph line
        para_buf.append(line)
        i += 1

    flush_para()
    flush_list()
    if in_table:
        out.append('</tbody></table>')

    return '\n'.join(out)


def inline_format(text: str) -> str:
    """Format inline markdown: bold, italic, code."""
    # Escape HTML first
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic *text*
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def build_css() -> str:
    """Return the master CSS for all PDF pages."""
    return f"""
@page {{
    size: letter portrait;
    margin: 0.9in 0.5in 0.7in 0.5in;
    @top-left {{
        content: "AtlasPay SOC 2 Type 1 Readiness";
        font-family: 'Helvetica', sans-serif;
        font-size: 7.5pt;
        color: {LIGHT_GRAY};
        border-bottom: 1pt solid {GOLD};
        padding-bottom: 4pt;
        width: 100%;
    }}
    @top-right {{
        content: "IfeSec Risk Advisory";
        font-family: 'Helvetica', sans-serif;
        font-size: 7.5pt;
        color: {LIGHT_GRAY};
        text-align: right;
        border-bottom: 1pt solid {GOLD};
        padding-bottom: 4pt;
        white-space: nowrap;
    }}
    @bottom-left {{
        content: "CONFIDENTIAL";
        font-family: 'Helvetica', sans-serif;
        font-size: 7pt;
        color: {CRIMSON};
        font-weight: bold;
        letter-spacing: 0.1em;
        border-top: 1pt solid {GOLD};
        padding-top: 4pt;
    }}
    @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'Helvetica', sans-serif;
        font-size: 7.5pt;
        color: {LIGHT_GRAY};
        border-top: 1pt solid {GOLD};
        padding-top: 4pt;
    }}
    @bottom-right {{
        content: "2026-06-25";
        font-family: 'Helvetica', sans-serif;
        font-size: 7.5pt;
        color: {LIGHT_GRAY};
        text-align: right;
        border-top: 1pt solid {GOLD};
        padding-top: 4pt;
    }}
}}

/* Cover page: no headers/footers, full bleed */
@page :first {{
    margin: 0;
    @top-left {{ content: none; border: none; }}
    @top-right {{ content: none; border: none; }}
    @bottom-left {{ content: none; border: none; }}
    @bottom-center {{ content: none; border: none; }}
    @bottom-right {{ content: none; border: none; }}
}}

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Helvetica', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.4;
    color: {DARK_GRAY};
    background: #FFFFFF;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

/* === Cover page === */
.cover {{
    width: 8.5in;
    height: 11in;
    background: {BLACK};
    color: #FFFFFF;
    padding: 1.5in 0.75in 1in 0.75in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    position: relative;
}}

.cover::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6pt;
    background: {GOLD};
}}

.cover-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1in;
}}

.cover-brand {{
    color: {GOLD};
    font-size: 14pt;
    font-weight: bold;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}}

.cover-version {{
    color: {LIGHT_GRAY};
    font-size: 9pt;
    border: 1px solid {LIGHT_GRAY};
    padding: 3pt 8pt;
    border-radius: 2pt;
}}

.cover-title-block {{
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.cover-title {{
    color: #FFFFFF;
    font-size: 36pt;
    font-weight: bold;
    line-height: 1.15;
    margin: 0 0 18pt 0;
}}

.cover-subtitle {{
    color: {GOLD};
    font-size: 18pt;
    font-weight: normal;
    line-height: 1.3;
    margin: 0 0 36pt 0;
}}

.cover-metadata {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24pt;
    border-top: 2pt solid {GOLD};
    padding-top: 18pt;
    margin-top: 36pt;
}}

.cover-meta-label {{
    color: {LIGHT_GRAY};
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4pt;
}}

.cover-meta-value {{
    color: #FFFFFF;
    font-size: 11pt;
    font-weight: bold;
    line-height: 1.3;
}}

.cover-footer {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1pt solid {GOLD};
    padding-top: 12pt;
    margin-top: 24pt;
}}

.cover-footer-brand {{
    color: {GOLD};
    font-size: 10pt;
    font-weight: bold;
    letter-spacing: 0.1em;
}}

.cover-footer-conf {{
    color: {CRIMSON};
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    border: 1pt solid {CRIMSON};
    padding: 3pt 8pt;
}}

/* === Content pages === */
.content {{
    page-break-before: always;
}}

h1 {{
    color: {BLACK};
    font-size: 22pt;
    font-weight: bold;
    line-height: 1.2;
    margin: 0 0 12pt 0;
    padding-bottom: 8pt;
    border-bottom: 2pt solid {GOLD};
}}

h2 {{
    color: {CRIMSON};
    font-size: 16pt;
    font-weight: bold;
    line-height: 1.2;
    margin: 18pt 0 8pt 0;
    page-break-after: avoid;
    page-break-before: auto;
}}

h3 {{
    color: {GOLD};
    font-size: 13pt;
    font-weight: bold;
    line-height: 1.2;
    margin: 14pt 0 6pt 0;
    page-break-after: avoid;
    page-break-before: auto;
}}

h4 {{
    color: {MED_GRAY};
    font-size: 11pt;
    font-weight: bold;
    font-style: italic;
    margin: 10pt 0 4pt 0;
    page-break-after: avoid;
}}

p {{
    margin: 0 0 8pt 0;
    text-align: left;
    orphans: 3;
    widows: 3;
}}

ul, ol {{
    margin: 6pt 0 8pt 0;
    padding-left: 20pt;
}}

li {{
    margin-bottom: 4pt;
    line-height: 1.35;
}}

hr {{
    border: none;
    border-top: 1pt solid {RULE_GRAY};
    margin: 14pt 0;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0 14pt 0;
    font-size: 9pt;
    page-break-inside: auto;
}}

thead {{
    display: table-header-group;
}}

th {{
    background: #2A2A2A;
    color: #FFFFFF;
    padding: 6pt 8pt;
    text-align: left;
    font-weight: bold;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border: 1px solid #2A2A2A;
}}

td {{
    padding: 5pt 8pt;
    border: 1px solid {RULE_GRAY};
    vertical-align: top;
    font-size: 9pt;
}}

tbody tr:nth-child(even) td {{
    background: {PAPER_GRAY};
}}

tbody tr:nth-child(odd) td {{
    background: #FFFFFF;
}}

/* Status badges */
.status {{
    display: inline-block;
    padding: 1pt 6pt;
    border-radius: 3pt;
    font-size: 8.5pt;
    font-weight: bold;
    white-space: nowrap;
}}

.status-covered {{
    background: #C8E6C9;
    color: #1B5E20;
}}

.status-partial {{
    background: #FFE0B2;
    color: #E65100;
}}

.status-missing {{
    background: #FFCDD2;
    color: #B71C1C;
}}

/* Treatment badges (for risk register) */
.treatment-mitigate {{
    display: inline-block;
    background: #E3F2FD;
    color: #0D47A1;
    padding: 1pt 8pt;
    border-radius: 10pt;
    font-size: 8.5pt;
    font-weight: bold;
}}

.treatment-accept {{
    display: inline-block;
    background: #FFF3E0;
    color: #E65100;
    padding: 1pt 8pt;
    border-radius: 10pt;
    font-size: 8.5pt;
    font-weight: bold;
}}

/* Severity level in risk cells */
.severity-low {{
    background: #C8E6C9 !important;
    color: #1B5E20;
    font-weight: bold;
    text-align: center;
}}

.severity-medium {{
    background: #FFE0B2 !important;
    color: #E65100;
    font-weight: bold;
    text-align: center;
}}

.severity-high {{
    background: #FFCDD2 !important;
    color: #B71C1C;
    font-weight: bold;
    text-align: center;
}}

.severity-very-high {{
    background: #C62828 !important;
    color: #FFFFFF;
    font-weight: bold;
    text-align: center;
}}

.residual-high {{
    font-weight: bold;
    color: #B71C1C;
}}

.lab-tag {{
    background: #FFF59D;
    color: #6A1B9A;
    padding: 0 4pt;
    border-radius: 2pt;
    font-size: 8pt;
    font-weight: bold;
}}

.matrix-legend {{
    font-size: 8.5pt;
    color: {LIGHT_GRAY};
    font-style: italic;
    margin: 6pt 0 12pt 0;
}}

.page-break-before {{
    page-break-before: always;
}}

.avoid-break {{
    page-break-inside: avoid;
}}

/* Matrix table - keep whole on one page */
table.matrix-table {{
    page-break-inside: avoid;
    font-size: 8.5pt;
    margin: 6pt 0;
}}

table.matrix-table th {{
    font-size: 7.5pt;
    padding: 4pt 6pt;
}}

table.matrix-table td {{
    font-size: 8pt;
    padding: 4pt 6pt;
    text-align: center;
}}

table.matrix-table td:first-child {{
    text-align: left;
    font-weight: bold;
}}

/* Code blocks */
pre {{
    background: #F5F5F5;
    border: 1pt solid {RULE_GRAY};
    border-radius: 2pt;
    padding: 8pt 10pt;
    font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    overflow-x: auto;
    page-break-inside: avoid;
    white-space: pre-wrap;
    word-wrap: break-word;
}}

code {{
    background: #F0F0F0;
    padding: 1pt 4pt;
    border-radius: 2pt;
    font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
    font-size: 0.92em;
}}

pre code {{
    background: none;
    padding: 0;
}}

/* Severity rows in risk register */
.severity-high {{ background: #FFEBEE !important; }}
.severity-medium {{ background: #FFF8E1 !important; }}
.severity-low {{ background: #E8F5E9 !important; }}

/* Heatmap matrix */
.matrix-grid {{
    display: grid;
    grid-template-columns: auto repeat(5, 1fr);
    gap: 2pt;
    margin: 12pt 0;
    font-size: 9pt;
    text-align: center;
}}

.matrix-header {{
    background: #2A2A2A;
    color: #FFFFFF;
    padding: 6pt 4pt;
    font-weight: bold;
    font-size: 8pt;
}}

.matrix-cell {{
    padding: 10pt 4pt;
    border: 1px solid {RULE_GRAY};
    min-height: 36pt;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}}

.matrix-cell-low {{ background: #C8E6C9; color: #1B5E20; }}
.matrix-cell-medium {{ background: #FFE0B2; color: #E65100; }}
.matrix-cell-high {{ background: #FFCDD2; color: #B71C1C; }}
.matrix-cell-critical {{ background: #C62828; color: #FFFFFF; }}
.matrix-cell-empty {{ background: #F5F5F5; color: {LIGHT_GRAY}; }}

/* Inline icons */
.icon {{ font-style: normal; }}
"""


def build_cover(doc_type: str, title: str, subtitle: str, metadata: dict) -> str:
    """Build the dark-theme cover page HTML."""
    version = metadata.get('version', 'v3.0')
    doc_id = metadata.get('doc_id', '')
    period = metadata.get('period', '')
    preparer = metadata.get('preparer', 'IfeSec — ijezie Risk Advisory')
    classification = metadata.get('classification', 'CONFIDENTIAL')

    meta_cells = []
    for label, value in [
        ('Document ID', doc_id),
        ('Version', version),
        ('Period', period),
        ('Preparer', preparer),
        ('Classification', classification),
        ('Status', 'Draft — Pending Review'),
    ]:
        if value:
            meta_cells.append(f'''
<div class="cover-meta-item">
    <div class="cover-meta-label">{label}</div>
    <div class="cover-meta-value">{value}</div>
</div>''')

    return f'''
<div class="cover">
    <div class="cover-header">
        <div class="cover-brand">IfeSec</div>
        <div class="cover-version">{version}</div>
    </div>

    <div class="cover-title-block">
        <h1 class="cover-title">{title}</h1>
        <p class="cover-subtitle">{subtitle}</p>
    </div>

    <div class="cover-metadata">
        {''.join(meta_cells[:3])}
    </div>

    <div class="cover-metadata" style="margin-top: 0; border-top: none; padding-top: 0;">
        {''.join(meta_cells[3:])}
    </div>

    <div class="cover-footer">
        <div class="cover-footer-brand">IfeSec — ijezie Risk Advisory</div>
        <div class="cover-footer-conf">{classification}</div>
    </div>
</div>
'''


def build_header_footer(doc_title: str, doc_type: str) -> str:
    """Header/footer markup applied via CSS @page rules."""
    # We'll handle this in CSS using @page top/bottom margins
    return ''  # no-op; CSS handles it


def wrap_html(cover_html: str, body_html: str, doc_title: str) -> str:
    """Wrap content in full HTML document with embedded CSS."""
    css = build_css()
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{doc_title}</title>
    <style>{css}</style>
</head>
<body>
    {cover_html}
    <div class="content">
        {body_html}
    </div>
</body>
</html>
'''


def render_pdf(html_path: str, pdf_path: str):
    """Render HTML to PDF using WeasyPrint via subprocess."""
    import subprocess

    result = subprocess.run(
        ['weasyprint', html_path, pdf_path],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f'WeasyPrint STDERR: {result.stderr}')
        raise RuntimeError(f'WeasyPrint failed: {result.stderr}')


def main():
    parser = argparse.ArgumentParser(description='Generate IfeSec portfolio PDF from markdown')
    parser.add_argument('source_md', help='Path to source markdown')
    parser.add_argument('output_pdf', help='Path to output PDF')
    parser.add_argument('doc_type', choices=['executive_briefing', 'risk_register', 'control_mapping', 'audit_walkthrough'],
                        help='Document type (controls cover/title/metadata)')
    args = parser.parse_args()

    # Read source
    with open(args.source_md) as f:
        md_content = f.read()

    # Doc type metadata
    doc_metadata = {
        'executive_briefing': {
            'title': 'AtlasPay FinTech',
            'subtitle': 'SOC 2 Type 1 Readiness — Executive Briefing',
            'doc_id': 'IFESEC-ATL-SOC2-EB-20260625',
            'period': 'FY 2026 Q3 Audit Window',
        },
        'risk_register': {
            'title': 'AtlasPay FinTech',
            'subtitle': 'SOC 2 Type 1 Readiness — Risk Register',
            'doc_id': 'IFESEC-ATL-SOC2-RR-20260625',
            'period': 'FY 2026 Q3 Audit Window',
        },
        'control_mapping': {
            'title': 'AtlasPay FinTech',
            'subtitle': 'SOC 2 Type 1 Readiness — Control Mapping',
            'doc_id': 'IFESEC-ATL-SOC2-CM-20260625',
            'period': 'FY 2026 Q3 Audit Window',
        },
        'audit_walkthrough': {
            'title': 'AtlasPay FinTech',
            'subtitle': 'SOC 2 Type 1 Readiness — Audit Walkthrough',
            'doc_id': 'IFESEC-ATL-SOC2-AW-20260625',
            'period': 'FY 2026 Q3 Audit Window',
        },
    }
    meta = doc_metadata[args.doc_type]

    # Convert markdown to HTML body
    body_html = md_to_html(md_content)

    # Build cover
    cover_html = build_cover(args.doc_type, meta['title'], meta['subtitle'], {
        'version': 'v3.0',
        'doc_id': meta['doc_id'],
        'period': meta['period'],
        'preparer': 'IfeSec — ijezie Risk Advisory',
        'classification': 'CONFIDENTIAL',
    })

    # Wrap in full HTML
    full_html = wrap_html(cover_html, body_html, meta['title'])

    # Write HTML to temp
    html_path = f'/tmp/{args.doc_type}_v3.html'
    with open(html_path, 'w') as f:
        f.write(full_html)

    print(f'HTML written to: {html_path} ({len(full_html):,} chars)')

    # Render to PDF
    print(f'Rendering PDF: {args.output_pdf}')
    render_pdf(html_path, args.output_pdf)
    print(f'PDF size: {os.path.getsize(args.output_pdf):,} bytes')


if __name__ == '__main__':
    main()