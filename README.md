# AtlasPay FinTech SOC 2 Type 1 Readiness

A portfolio case study demonstrating end-to-end SOC 2 Type 1 readiness work for a FinTech payments startup. This repository contains the source documents, working methodology, and final stakeholder deliverables produced during a 5-hour focused engagement. All content is for portfolio demonstration purposes; the persona and supporting data are synthetic.

---

## At a Glance

| Dimension | Value |
|---|---|
| Engagement duration | 5 hours focused (front-loaded assessment + deliverable production) |
| Engagement window | FY 2026 Q3 audit window, target Q2 2027 attestation |
| Client persona | 50-employee FinTech payment processor |
| Trust Services Criteria in scope | Security (Common Criteria) + Availability + Confidentiality |
| Perimeters scoped | 4 (Core Payment System, Internal Infrastructure, Payments, Data) |
| Risk scenarios assessed | 6 (R-01 through R-06) |
| Vendors under management | 7 (3 Tier 1 Critical, 2 Tier 2 Important, 2 Tier 3 Deferrable) |
| Active policies in place | 4 (Access Control, Incident Response, Security Awareness, Third-Party Risk Management) |
| SOC 2 criteria evaluated | 40 across 9 Common Criteria categories + Availability + Confidentiality |
| Current audit readiness | 85% (Q4 2026 projection); 100% by Q2 2027 |
| POA&M items tracked | 19 (0 Critical, 2 High, 3 Medium, 1 Low open, 13 closed) |
| Final deliverable count | 5 stakeholder PDFs + 1 POA&M CSV + 9 source markdowns + 4 methodology docs |
| Frameworks referenced | SOC 2 TSC 2022, NIST SP 800-53 Rev. 5, ISO 27005 risk scoring, PCI DSS 4.0 adjacency |

---

## The Engagement

### Client Profile

AtlasPay is a 50-employee FinTech payment processor preparing for its first SOC 2 Type 1 audit. Like most early-stage FinTechs, AtlasPay faces a compressed timeline: enterprise customers, banking partners, and card networks require SOC 2 attestation before integration, fund custody, or production processing approvals. The audit window target was Q3 2026; after this engagement, the realistic window moved to Q2 2027 to allow administrative scaffolding to mature.

### Scope

- **In scope:** SOC 2 Common Criteria (CC1-CC9), Availability (A1), Confidentiality (C1)
- **Out of scope:** Processing Integrity (PI), Privacy (P) - not relevant to current service offerings
- **Frameworks referenced:** SOC 2 Trust Services Criteria 2022, NIST SP 800-53 Rev. 5 control mapping, ISO 27005 5x5 risk scoring methodology, PCI DSS 4.0 adjacency for payment-specific controls
- **Adjacent work:** PCI DSS readiness overlaps significantly with SOC 2 Security; this engagement surfaced 4 control mappings that satisfy both frameworks simultaneously

### Why This Work Matters

For a FinTech CISO, SOC 2 readiness is a revenue enabler, not a paperwork exercise. Customer trust, partner onboarding requirements, funding conversations, and the ability to compete with larger processors that already have auditor-validated controls all depend on a clean attestation. A pre-audit risk assessment like this one does three things: (1) surfaces gaps while there is still time to fix them before the auditor arrives, (2) creates a documented, repeatable risk language that the board, auditors, and engineers can all use, and (3) ties each control investment to a specific risk scenario, so security spend is defensible rather than reactive.

---

## Risk Register Summary

The full risk register (with scoring rationale, treatment plans, and residual acceptance) is in `deliverables/phase-2/risk-register.pdf`. The summary:

| Risk ID | Scenario | Inherent | Residual | Treatment | Board-Relevant |
|---|---|---|---|---|---|
| R-01 | Privileged Account Compromise | High | Medium | PAM tool + session recording | Yes |
| R-02 | Payment Data Exfiltration via API | High | Medium | Tokenization + rate limiting + WAF | No |
| R-03 | Ransomware on Production Database | High | Medium | Immutable backups + 24-hour recovery SLA | No |
| R-04 | Third-Party SaaS Breach | High | High | Vendor SOC 2 collection + monitoring + MSA SLAs | Yes |
| R-05 | Insider Threat - Malicious Employee | Medium | Medium | Background checks + separation of duties + quarterly attestation | Yes |
| R-06 | Insufficient Audit Logging | Medium | Low | Datadog streaming + retention + alerting | Yes |

**Key observations:**
- 4 of 6 risks sit at residual Medium, which is realistic for an early-stage FinTech
- R-04 (Third-Party SaaS Breach) is the only risk at residual High. This is structural, not a control failure. See Finding 2 below.
- R-06 dropped from Medium to Low because audit logging is already streaming and alerting
- The board-relevant subset (R-01, R-04, R-05, R-06) is what the executive briefing surfaces to the audit committee

---

## Vendor Risk Snapshot

7 vendors under Master Service Agreement, classified by criticality and review cadence:

| Vendor | Tier | Criticality | SOC 2 Status | Review Cadence |
|---|---|---|---|---|
| Payment Gateway | 1 | Critical | Executed 2025-Q4 | Quarterly |
| Cloud Provider | 1 | Critical | Executed 2025-Q1 | Quarterly |
| Identity Provider | 1 | Critical | Executed 2025-Q2 | Quarterly |
| Monitoring Tools | 2 | Important | Executed 2025-Q3 | Semi-annual |
| Finance Systems | 2 | Important | Executed 2025-Q3 | Semi-annual |
| Data Warehouse | 2 | Important | Executed 2025-Q4 | Semi-annual |
| Application Platform | 3 | Deferrable | Executed 2026-Q1 | Annual |

**Tiering logic:** Any vendor whose failure would stop payment processing, block authentication, or break cloud infrastructure is Tier 1. Tools that support operations but have workable alternatives are Tier 2. Deferrable platforms are Tier 3 and reviewed annually.

---

## Process and Methodology

### Phase 1: Baseline (Days 1-2)

Established the engagement container, ingested the AtlasPay persona data, and produced the first version of the risk register and control matrix. Initial pass surfaced 14 POA&M items. First PDF generation round revealed a hard lesson: programmatic PDF libraries produce text-box overflow, shape overlap, and font-clipping pathologies when the source content is long. The methodology was sound, but the deliverables were not stakeholder-ready.

### Phase 2: Hardening (Day 3)

Rebuilt the deliverables using an HTML + CSS template rendered through WeasyPrint. This eliminated the layout pathologies from v1 and produced stakeholder-ready PDFs that scale cleanly across page breaks. Expanded the control matrix to all 40 SOC 2 criteria in scope. Performed severity-graded gap assessment. Marked 4 of 6 risks as board-relevant. Created the audit walkthrough simulation - 10 questions a real SOC 2 auditor would ask, with expected findings and management response templates. Validated every PDF visually before commit.

### Risk Scoring Methodology

**Probability scale (5 levels):**
1. Unlikely (1-5%)
2. Rather Unlikely (5-25%)
3. Likely (25-50%)
4. Very Likely (50-80%)
5. Almost Certain (80%+)

**Impact scale (5 levels):**
1. Minor (negligible consequences)
2. Significant (limited consequences)
3. Moderate (material consequences, recoverable)
4. Major (severe consequences, difficult recovery)
5. Catastrophic (existential consequences)

**Risk = Probability x Impact.** Inherent risk is scored before controls; residual risk is scored after controls. Residual risk that is higher than the client wants triggers treatment planning.

### Control Mapping Discipline

Each SOC 2 criterion is mapped against:
- The AtlasPay policies that satisfy it
- The AtlasPay risks it mitigates
- The AtlasPay vendors that contribute to its operation
- The current status (Met, Partial, Missing, or Not Applicable)
- Evidence that demonstrates the control

A control marked Met has design and operating effectiveness with evidence. Partial has design but incomplete evidence. Missing has no design or evidence. This produces a defensible audit position - every Met claim can be backed by a specific artifact.

---

## Key Findings

### 1. AtlasPay is technically strong but administratively incomplete

The technical controls are operational: MFA enforcement is live, audit logging is streaming to Datadog with retention and alerting, the incident response plan is documented, and change management runs through pull requests with reviewer approval. None of the 6 risk scenarios require a missing technical control to mitigate.

What AtlasPay lacks is the administrative scaffolding auditors look for:
- Vendor SOC 2 Type 2 reports not collected from any Tier 1 vendor
- Board-level security KPI reporting cadence not formalized
- Quarterly privileged access attestation process documented but not yet executed
- Vendor onboarding checklist informal, not codified
- Data classification policy not formally approved and disseminated

This pattern is common in early-stage FinTechs: the engineering team implements strong technical controls, but the documentation and reporting cadence lag because nobody owns the GRC function. The remediation effort should focus on administrative scaffolding first.

### 2. Third-party vendor risk is the highest residual risk that cannot be eliminated

R-04 (Third-Party SaaS Breach) sits at residual High and stays there. This is not a control failure; it is the structural reality of depending on third-party infrastructure.

AtlasPay can:
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

R-05 (Insider Threat - Malicious Employee) sits at residual Medium after mitigation. The reasoning: humans are inherently unpredictable. Background checks, separation of duties, and quarterly access reviews reduce the likelihood significantly, but no control eliminates the possibility that an authorized user will misuse their access.

Medium is the realistic floor for insider threat. Any engagement that claims residual Low for insider threat is misrepresenting the risk.

### 4. The audit walkthrough simulation surfaces gaps that documentation review misses

The 10-question walkthrough simulation revealed gaps that the Phase 1 control mapping had not surfaced:
- Audit log integrity depends on Datadog availability - a separate dependency not currently documented in the BCP
- The incident response tabletop exercise has not yet been executed (IRP is documented but not validated via simulation)
- Security awareness training completion is 80%, not 100% (training is tied to performance review but enforcement is inconsistent)

These gaps are administrative, not technical, but auditors will surface them in a real engagement. The walkthrough simulation is the single most efficient way to train the client's team for the actual audit.

### 5. The maturity snapshot is the sales asset

The maturity snapshot deliverable (10 areas scored current vs. target) is the artifact that closes deals. It tells the prospective client in one page: where you are, where you need to be, the gap between them. For sales, this matters more than the full risk register or control matrix.

---

## Audit Readiness Projection

| Quarter | Projected Readiness | Key Gates Cleared | Trigger |
|---|---|---|---|
| Q4 2026 | 85% | Quarterly access attestation, vendor onboarding checklist codified | 6 POA&M items closed |
| Q1 2027 | 95% | Vendor SOC 2 Type 2 reports collected, board reporting cadence established, IRP tabletop executed | 12 POA&M items closed |
| Q2 2027 | 100% | Vendor fraud risk assessment + data classification policy finalized | 19 POA&M items closed |

AtlasPay should target a Q2 2027 audit window. Earlier windows risk a qualified opinion because of the administrative gaps. The 3-quarter runway allows the client to demonstrate operating effectiveness on the new controls before the auditor tests them.

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
9. **Vendor tiering produces defensible review cadence.** Tier 1 critical vendors reviewed quarterly, Tier 2 important semi-annually, Tier 3 deferrable annually. This balances risk management with operational overhead.
10. **The control matrix has exactly four status options.** Met, Partial, Missing, Not Applicable. Anything more granular invites subjective interpretation; anything less hides gaps.
11. **The risk matrix should be 5x5, not 3x3.** A 3x3 matrix collapses meaningful differences in probability and impact and produces risk scores that don't differentiate real-world scenarios.

---

## Deliverables

### Stakeholder-Facing PDFs (5 files)

| Deliverable | Purpose | Pages | Audience |
|---|---|---|---|
| [Executive Briefing](deliverables/phase-2/executive-briefing.pdf) | Board-ready summary | 5 | Board, CISO, executive leadership |
| [Risk Register (Detailed)](deliverables/phase-2/risk-register.pdf) | Full risk register with scoring rationale | 5 | Board Risk Committee, SOC 2 audit team |
| [Control Matrix](deliverables/phase-2/control-matrix.pdf) | SOC 2 TSC mapping across 40 criteria | 7 | SOC 2 auditor, internal compliance |
| [Audit Walkthrough Simulation](deliverables/phase-2/audit-walkthrough.pdf) | 10 auditor questions with management response | 6 | Client team preparing for real audit |
| [POA&M (CSV)](deliverables/phase-2/poam.csv) | 19-item Plan of Action and Milestones | 19 rows | Project managers, budget owners |

**Total:** 23 pages of stakeholder-ready PDF documentation plus an importable POA&M CSV.

### Methodology Documents (4 files)

The detailed working documents that show the methodology, not just the deliverables:

- [SOC 2 Risk Register](lab/docs/soc2-risk-register.md) - detailed risk register methodology with full scoring rationale
- [SOC 2 Control Mapping](lab/docs/soc2-control-mapping.md) - control mapping methodology across all 33 Common Criteria
- [SOC 2 Gap Assessment](lab/docs/soc2-gap-assessment.md) - gap assessment methodology with severity grading
- [SOC 2 Audit Walkthrough](lab/docs/soc2-audit-walkthrough.md) - audit walkthrough methodology with 10 questions, expected findings, management response templates

### Phase 2 Source Markdowns (9 files)

The engagement record from start to finish, in `lab/source-data/phase-2/`:

| File | What It Documents |
|---|---|
| `state-2026-06-26.md` | Live state snapshot of the GRC platform (risks, policies, vendors, controls) |
| `risk-register-board-2026-06-26.md` | Board-relevant risk subset source (4 risks) |
| `risk-register-detailed-2026-06-26.md` | Full risk register source (6 risks) |
| `control-matrix-soc2-2026-06-26.md` | Control matrix source (40 criteria) |
| `gap-assessment-2026-06-26.md` | Gap assessment source (6 gaps, severity graded) |
| `executive-briefing-2026-06-26.md` | Executive briefing source markdown |
| `audit-walkthrough-2026-06-26.md` | Audit walkthrough source markdown |
| `policy-pack-2026-06-26.md` | Policy pack manifest (4 active + 6 planned policies) |
| `maturity-snapshot-2026-06-26.md` | Maturity snapshot source (sales asset, 10 areas scored) |

### Reference Material (Input Documents)

In `lab/source-data/`, the source documents this engagement builds on:

| Document | Purpose |
|---|---|
| `AtlasPay-Risk-Assessment__AtlasPay_SOC_2_Readiness.pdf` | NIST SP 800-53 Rev. 5 risk assessment input document |
| `AtlasPay-Risk-Assessment__README.md` | Index for the risk assessment document |
| `AtlasPay-Risk-Profile-BCP__AtlasPay_Risk_Profile.pdf` | AtlasPay enterprise risk profile |
| `AtlasPay-Risk-Profile-BCP__Atlaspay_Business_Continuity_Plan.pdf` | BCP input document |
| `AtlasPay-Risk-Profile-BCP__README.md` | Index for the risk profile and BCP |
| `Cyber-Security-Policy-Library__Access_Control_&_Privileged_Access_Policy.pdf` | Access control policy (AtlasPay active policy) |
| `Cyber-Security-Policy-Library__Incident_Response_Policy.pdf` | Incident response policy (AtlasPay active policy) |
| `Cyber-Security-Policy-Library__Security_Awareness_&_Acceptable_Use_Policy.pdf` | Security awareness policy (AtlasPay active policy) |
| `Cyber-Security-Policy-Library__Third-Party_Risk_Management_Policy.pdf` | Third-party risk policy (AtlasPay active policy) |
| `Cyber-Security-Policy-Library__README.md` | Index for the policy library |
| `Priviledged-Account-Abuse-Scenario-Analysis__Cyber_Risk_Scenario_Artifact.pdf` | Privileged account abuse scenario analysis input |
| `Priviledged-Account-Abuse-Scenario-Analysis__README.md` | Index for the privileged account analysis |
| `Scenario-Based-Cyber-Risk-Analyses__Priv_Accunt_Abuse_Analysis.pdf` | Insider threat scenario analysis input |
| `Scenario-Based-Cyber-Risk-Analyses__Third-Party_Vendor_Risk.pdf` | Third-party vendor risk scenario analysis input |
| `Scenario-Based-Cyber-Risk-Analyses__README.md` | Index for the scenario-based analyses |
| `atlaspay_persona_spec.json` | AtlasPay persona specification (input data) |
| `extracted/*.txt` | Plain-text extractions of the reference PDFs (searchable) |

---

## About the Work

This engagement was performed as a portfolio demonstration. The AtlasPay persona is fictional, but the methodology, deliverables, and decision discipline are production-grade. The same approach has been applied to HIPAA (healthcare), GLBA + FFIEC + SOX (banking), and ISO 27001 (international SaaS) engagements - each framework has a distinct scope, but the underlying operating model transfers cleanly.

The Solo vCISO operating model used in this engagement is documented separately. It covers:
- Pre-engagement: client onboarding, engagement letter, scope definition
- Discovery: data ingestion, stakeholder interviews, evidence collection
- Assessment: risk register, control matrix, gap assessment
- Deliverables: executive briefing, detailed reports, POA&M
- Remediation support: project management, evidence collection, audit prep
- Audit walkthrough: trial audit, management response templates, mock audit
- Closeout: final report, residual acceptance documentation, post-engagement support

For organizations considering SOC 2 readiness work, the engagement typically runs 4-12 weeks end to end depending on starting posture. The 5-hour focused effort represented here is the front-loaded assessment + deliverable production phase; the longer tail is remediation execution by the client team with advisory support.

---

## Related Portfolio Work

Other engagements using the same operating model, available as separate repositories:

- **Helix Health GRC Sandbox** - HIPAA + SOC 2 readiness for a HealthTech SaaS persona
- **Meridian Bank GRC Sandbox** - FFIEC CAT + GLBA Safeguards + SOX ITGC posture for a community bank persona

---

## License

This portfolio demonstration work is for educational and hiring-manager review purposes. Organizations may adapt the methodology for internal use. See `LICENSE` for full terms.