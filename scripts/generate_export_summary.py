"""
Generate human-readable summary of the AtlasPay export.
"""
import json
from pathlib import Path
from datetime import datetime

SRC = Path.home() / "Documents/IfeSec/Projects/atlaspay-grc-sandbox/data" / "atlaspay_eramba_export.json"
OUT = Path.home() / "Documents/IfeSec/Projects/atlaspay-grc-sandbox/data" / "atlaspay_export_summary.md"

with open(SRC) as f:
    d = json.load(f)

lines = []
lines.append("# AtlasPay GRC Sandbox — Eramba Export Summary")
lines.append("")
lines.append(f"**Exported:** {d['meta']['exported_at']}")
lines.append(f"**Source:** {d['meta']['source']} ({d['meta']['source_url']})")
lines.append("")
lines.append("## Record Counts")
lines.append("")
lines.append("| Section | Count |")
lines.append("|---|---|")
for k, v in d['counts'].items():
    if k != 'total_ingested':
        lines.append(f"| {k.replace('_', ' ').title()} | {v} |")
lines.append(f"| **Total** | **{d['counts']['total_ingested']}** |")
lines.append("")

# Risk Classifications
lines.append("## Risk Classification Types")
lines.append("")
for t in d['risk_classification_types']:
    lines.append(f"- **{t['name']}**")
lines.append("")

# Risk Classifications (with types resolved)
lines.append("## Risk Classifications")
lines.append("")
lines.append("| Type | Name | Value |")
lines.append("|---|---|---|")
for c in d['risk_classifications']:
    lines.append(f"| {c['_type_name']} | {c['name']} | {c['value']} |")
lines.append("")

# Risks
lines.append("## Asset Risks")
lines.append("")
lines.append("| ID | Title | Residual | Threats | Vulnerabilities |")
lines.append("|---|---|---|---|---|")
for r in d['risks']:
    score = r.get('residual_risk') or r.get('risk_score') or '-'
    lines.append(f"| {r['_eramba_id']} | {r['title']} | {score} | {(r.get('threats') or '')[:60]} | {(r.get('vulnerabilities') or '')[:60]} |")
lines.append("")

# Policies
lines.append("## Security Policies")
lines.append("")
lines.append("| ID | Name | Version | Published | Next Review |")
lines.append("|---|---|---|---|---|")
for p in d['security_policies']:
    lines.append(f"| {p['_eramba_id']} | {p['name']} | {p.get('version', '-')} | {p.get('published_date', '-')} | {p.get('next_review_date', '-')} |")
lines.append("")

# BCPs
lines.append("## Business Continuity Plans")
lines.append("")
lines.append("| ID | Title | Objective | Audit Metric (RTO/RPO) |")
lines.append("|---|---|---|---|")
for b in d['business_continuity_plans']:
    lines.append(f"| {b['_eramba_id']} | {b['title']} | {(b.get('objective') or '')[:60]} | {b.get('audit_metric', '-')} |")
lines.append("")

# Vendors
lines.append("## Third Parties (Vendors)")
lines.append("")
lines.append("| ID | Name | Description |")
lines.append("|---|---|---|")
for t in d['third_parties']:
    lines.append(f"| {t['_eramba_id']} | {t['name']} | {(t.get('description') or '')[:80]} |")
lines.append("")

# Incidents
lines.append("## Security Incidents")
lines.append("")
lines.append("| ID | Title | Open Date | Closure |")
lines.append("|---|---|---|---|")
for s in d['security_incidents']:
    lines.append(f"| {s['_eramba_id']} | {s['title']} | {s.get('open_date', '-')} | {s.get('closure_date', '-')} |")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## Notes for CISO Assistant Import")
lines.append("")
lines.append("- All Eramba IDs preserved as `_eramba_id` for traceability")
lines.append("- Eramba-specific columns (workflow_status, workflow_owner_id) prefixed with `_` and not used in import")
lines.append("- RTO/RPO is in `audit_metric` field as text (Eramba doesn't have a separate field)")
lines.append("- `description` field on policies/risks/BCPs is the human-readable content")
lines.append("- `threats` and `vulnerabilities` on risks are the source-context text from the AtlasPay PDF")
lines.append("")
lines.append("When importing to CISO Assistant, the natural mapping is:")
lines.append("")
lines.append("| Eramba | CISO Assistant |")
lines.append("|---|---|")
lines.append("| risk_classification_types | Risk Matrix (custom or built-in) |")
lines.append("| risk_classifications | Risk Matrix values |")
lines.append("| risks | Risk Assessment scenarios |")
lines.append("| security_policies | Policies (under Governance) |")
lines.append("| business_continuity_plans | Business Continuity scenarios + BIA |")
lines.append("| third_parties | Third Parties (Entities) |")
lines.append("| security_incidents | Incidents |")
lines.append("")

OUT.write_text('\n'.join(lines))
print(f"Summary written to: {OUT}")
print(f"Lines: {len(lines)}")
