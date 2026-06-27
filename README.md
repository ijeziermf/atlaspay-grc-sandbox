# AtlasPay FinTech SOC 2 Type 1 Readiness

A portfolio case study demonstrating end-to-end SOC 2 Type 1 readiness work for a FinTech payments startup. This repository contains the methodology, source documents, and final deliverables produced during the engagement. All content is for portfolio demonstration purposes; the persona and supporting data are synthetic.

---

## The Engagement

**Client profile:** AtlasPay is a 50-employee FinTech payment processor preparing for its first SOC 2 Type 1 audit. Like most early-stage FinTechs in the payments space, AtlasPay faces a compressed timeline: enterprise customers and partners require SOC 2 attestation before they will integrate, store funds, or sign MSAs. The audit window target was Q3 2026.

**Scope of work:**

- Trust Services Criteria selected: Security (Common Criteria), Availability, Confidentiality
- Out of scope: Processing Integrity, Privacy
- 4 perimeters: Core Payment System, Internal Infrastructure, Payments, Data
- 6 risk scenarios (R-01 through R-06)
- 4 active policies (Access Control, Incident Response, Security Awareness, Third-Party Risk Management)
- 7 vendors with Master Service Agreements
- 1 risk assessment container (RA-ATLASPAY-SOC2)
- 5x5 ISO 27005-aligned risk matrix

**Engagement objective:** Assess current SOC 2 readiness, identify gaps, produce a remediation roadmap, and deliver board-ready documentation that meets hiring-manager and audit-firm review standards.

---

## The Process

### Phase 1 - Baseline (Days 1-2)

Started from a clean slate. Established the engagement container, ingested the AtlasPay persona data into the risk register, mapped risks against the SOC 2 Trust Services Criteria, and built initial risk register and control matrix documentation. Identified 14 POA&M items requiring action. Produced first versions of the executive briefing and risk register PDFs.

The first round revealed an important lesson: **the v1 PDFs, while technically complete, were visually poor**. Headers wrapped awkwardly, text overflowed text boxes, severity badges didn't render correctly, and the cover page had contrast issues. This is the typical state of a first engagement - the methodology is sound, but the deliverables need iteration before they are stakeholder-ready.

### Phase 2 - Hardening (Day 3)

Took the Phase 1 baseline and:

- Built out the SOC 2 control matrix to all 33 Common Criteria plus Availability and Confidentiality sub-criteria
- Performed gap assessment with severity grading
- Marked 4 of 6 risks as board-relevant for executive reporting
- Produced 14 additional POA&M items (now 19 total) covering data classification, vendor onboarding checklists, board security reporting cadence, and other administrative gaps
- Created the audit walkthrough simulation - 10 questions a real SOC 2 auditor would ask, with expected findings and management response templates
- Rewrote the deliverables from scratch using HTML + CSS + WeasyPrint instead of programmatic PDF generation, which eliminated the layout pathologies from v1
- Validated every PDF visually before commit

---

## Key Findings

### 1. AtlasPay is technically strong but administratively incomplete

The technical controls are operational: MFA enforcement is live, audit logging is streaming to Datadog with retention and alerting, the incident response plan is documented, and change management runs through pull requests with reviewer approval. **None of the 6 risk scenarios require a missing technical control to mitigate.**

What AtlasPay lacks is the administrative scaffolding auditors look for:

- Vendor SOC 2 Type 2 reports not collected from any Tier 1 vendor
- Board-level security KPI reporting cadence not formalized
- Quarterly privileged access attestation process documented but not yet executed
- Vendor onboarding checklist informal, not codified
- Data classification policy not formally approved and disseminated

This pattern is common in early-stage FinTechs: the engineering team implements strong technical controls, but the documentation and reporting cadence lag because nobody owns the GRC function.

### 2. Third-party vendor risk is the highest residual risk that cannot be eliminated

R-04 (Third-Party SaaS Breach) sits at residual High and **stays there**. This is not a control failure; it is the structural reality of depending on third-party infrastructure. AtlasPay can:

- Require SOC 2 Type 2 reports from Tier 1 vendors
- Monitor vendor security ratings continuously
- Negotiate breach notification SLAs into MSAs (under 24 hours)
- Coordinate incident response with vendor security teams

AtlasPay cannot:

- Eliminate the possibility that a vendor is breached
- Eliminate the possibility that a vendor breach exposes AtlasPay customer data
- Control a vendor's internal security culture or hiring practices

The honest answer for the board: third-party risk is managed, not eliminated. This is the realistic ceiling for residual risk and the defensible position for an audit committee.

### 3. Insider threat residual floor is Medium, not Low

R-05 (Insider Threat - Malicious Employee) sits at residual Medium after mitigation. The reasoning: humans are inherently unpredictable. Background checks, separation of duties, and quarterly access reviews reduce the likelihood significantly, but no control eliminates the possibility that an authorized user will misuse their access. **Medium is the realistic floor for insider threat.** Any engagement that claims residual Low for insider threat is misrepresenting the risk.

### 4. The audit walkthrough simulation surfaces gaps that documentation review misses

The 10-question walkthrough simulation revealed gaps that the Phase 1 control mapping had not surfaced:

- Audit log integrity depends on Datadog availability - a separate dependency not currently documented in the BCP
- The incident response tabletop exercise has not yet been executed (IRP is documented but not validated via simulation)
- Security awareness training completion is 80%, not 100% (training is tied to performance review but enforcement is inconsistent)

These gaps are administrative, not technical, but auditors will surface them in a real engagement. **The walkthrough simulation is the single most efficient way to train the client's team for the actual audit.**

### 5. The "quick win" sales asset is the maturity snapshot

The maturity snapshot deliverable (10 areas scored current vs. target) is the artifact that closes deals. It tells the prospective client in one page: here's where you are, here's where you need to be, here's the gap. For sales, this matters more than the full risk register or control matrix.

---

## Audit Readiness Projection

| Quarter | Projected Readiness | Key Gates Cleared |
|---|---|---|
| Q4 2026 | 85% | Quarterly access attestation, vendor onboarding checklist codified |
| Q1 2027 | 95% | Vendor SOC 2 Type 2 reports collected, board reporting cadence established, IRP tabletop executed |
| Q2 2027 | 100% | Vendor fraud risk assessment + data classification policy finalized |

AtlasPay should target a Q2 2027 audit window. Earlier windows risk a qualified opinion because of the administrative gaps.

---

## Residuals to Carry Into the Next Engagement

The following patterns came out of this engagement and should be applied to every future SOC 2 readiness engagement, regardless of industry:

1. **Honest-call discipline on third-party risk.** Residual risk that cannot be eliminated stays at its real level. Reduced residuals require evidence, not optimism. Board reporting must reflect this honestly.

2. **Administrative gaps, not technical gaps, are the typical audit risk for early-stage companies.** The engagement focus should be on documentation, reporting cadence, and process maturity - not on implementing more technical controls.

3. **The audit walkthrough simulation is non-negotiable.** 10 questions, 10 expected findings, management response templates. This trains the client team for the real audit and surfaces gaps that documentation review misses.

4. **Board-relevant risks are a subset of all risks.** Not every risk belongs in the executive briefing. Flag the 4 of 6 that the board can act on; track the rest at management level.

5. **The maturity snapshot is the sales asset.** One page, 10 areas, current vs. target. This is what closes deals.

6. **PDF generation pipeline matters for credibility.** Text overflow, shape overlap, brand inconsistencies undermine the engagement deliverable. HTML + CSS rendering produces stakeholder-ready PDFs; programmatic generation produces debug output.

7. **Severity-graded POA&M with owner, target, and optional cost estimate.** Every POA&M item has all three. This makes the POA&M actionable for budgeting and accountability.

8. **The engagement produces four categories of deliverables.** Governance, Assessment, Technical, Executive. Every SOC 2 readiness engagement fits this taxonomy regardless of industry vertical.

---

## Deliverables

### Executive and Stakeholder-Facing (PDFs)

- [Executive Briefing](deliverables/phase-2/executive-briefing.pdf) - board-ready summary, 9 pages
- [Risk Register (Detailed)](deliverables/phase-2/risk-register.pdf) - full risk register with scoring rationale, 10 pages
- [Control Matrix](deliverables/phase-2/control-matrix.pdf) - SOC 2 TSC mapping, all 33 Common Criteria + Availability + Confidentiality
- [Audit Walkthrough Simulation](deliverables/phase-2/audit-walkthrough.pdf) - 10 auditor questions with expected findings and management response
- [POA&M (CSV)](deliverables/phase-2/poam.csv) - 19-item Plan of Action and Milestones, importable to any GRC tool

### Methodology and Working Documents

- [SOC 2 Risk Register](lab/docs/soc2-risk-register.md) - detailed risk register methodology
- [SOC 2 Control Mapping](lab/docs/soc2-control-mapping.md) - control mapping methodology
- [SOC 2 Gap Assessment](lab/docs/soc2-gap-assessment.md) - gap assessment methodology
- [SOC 2 Audit Walkthrough](lab/docs/soc2-audit-walkthrough.md) - audit walkthrough methodology

### Source Data (Markdown)

The Phase 2 source markdowns in `lab/source-data/phase-2/` document the engagement from start to finish:

- `state-2026-06-26.md` - live state snapshot of the GRC platform
- `risk-register-board-2026-06-26.md` - board-relevant risk subset
- `risk-register-detailed-2026-06-26.md` - detailed risk register source
- `control-matrix-soc2-2026-06-26.md` - control matrix source
- `gap-assessment-2026-06-26.md` - gap assessment source
- `executive-briefing-2026-06-26.md` - executive briefing source
- `audit-walkthrough-2026-06-26.md` - audit walkthrough source
- `policy-pack-2026-06-26.md` - policy pack manifest
- `maturity-snapshot-2026-06-26.md` - maturity snapshot (sales asset)

### Reference Material

`lab/source-data/` contains reference policy documents and risk assessment artifacts from prior AtlasPay work. These are the input documents the engagement builds on.

---

## License

This portfolio demonstration work is for educational purposes only. Organizations may adapt the methodology for internal use. See `LICENSE` for full terms.
