---
type: source
title: AtlasPay SOC 2 Gap Assessment
created: 2026-06-26
updated: 2026-06-26
tags: [gap-assessment, soc2, atlaspay, poam]
raw_paths:
  - raw/clients/atlaspay/state-2026-06-26.md
  - raw/clients/atlaspay/risk-register-board-2026-06-26.md
  - raw/clients/atlaspay/control-matrix-soc2-2026-06-26.md
status: active
---

# AtlasPay SOC 2 Gap Assessment

[LAB-SYNTHETIC] — Gap assessment demonstration for AtlasPay SOC 2 Type 1 readiness. AtlasPay is a fictional FinTech persona; the gaps here are illustrative patterns for a SOC 2 readiness engagement, not real client findings.

## Bottom line

**AtlasPay is ~85% ready for SOC 2 Type 1 audit.** 6 gaps identified, 0 critical, 0 missing controls. All gaps are administrative or documentation gaps, not control implementation gaps. This is the typical pattern for a FinTech startup that has implemented strong technical controls but hasn't formalized the documentation and cadence evidence.

## Gap summary

| Severity | Count | Description |
|---|---|---|
| Critical | 0 | No critical gaps. AtlasPay's technical controls are operational. |
| High | 2 | TPRM vendor SOC 2 collection, board reporting cadence |
| Medium | 3 | Quarterly access attestation, vendor onboarding checklist, vendor fraud assessment |
| Low | 1 | BEC tabletop exercise result documentation |
| **Total** | **6** | |

## Detailed gaps

### GAP-01 (High): Vendor SOC 2 Type 2 report collection incomplete

**Linked CC:** CC9.2
**Linked risk:** R-04 (Third-Party SaaS Breach)
**Linked POA&M:** POA&M-03

**Current state:** 7 vendors in AtlasPay TPRM scope. 0 vendors have current SOC 2 Type 2 reports on file.

**Gap:** Without vendor SOC 2 Type 2 reports, AtlasPay cannot demonstrate that critical vendors meet equivalent security controls. CC9.2 is Partial, not Met.

**Remediation:**
1. Identify Tier 1 vendors (likely V-01 Cloud, V-02 Payment Gateway, V-03 Identity, V-04 App Platform)
2. Request SOC 2 Type 2 reports from each Tier 1 vendor (request through vendor portal or TPRM team)
3. Review reports against AtlasPay's minimum controls baseline
4. Document exceptions and compensating controls for any gaps
5. File reports in encrypted evidence repository with annual refresh cadence

**Owner:** TPRM Lead
**Target:** Q1 2027
**Effort:** ~40 hours (collection + review)
**Cost estimate:** $0 (vendor reports are free) + ~$2K if TPRM platform license purchased

### GAP-02 (High): Board-level security KPI reporting cadence not formalized

**Linked CC:** CC1.2, CC4.2
**Linked risk:** R-04 (residual High, board-relevant)

**Current state:** Quarterly board meetings occur but security KPI reporting is ad-hoc, often bundled into operational risk reports.

**Gap:** Board audit committee should receive a dedicated security update quarterly covering: risk register changes, POA&M status, incident summary, vendor risk summary, audit readiness status. CC1.2 (board oversight) and CC4.2 (deficiency communication) are both Partial.

**Remediation:**
1. Draft board security report template (1-page executive summary + 5-page detail)
2. Establish quarterly cadence (calendar invites to audit committee)
3. Define 5 KPIs: risk register change velocity, POA&M closure rate, incident count by severity, vendor risk concentration, audit readiness % complete
4. First report due Q1 2027 board meeting

**Owner:** vCISO (Ijezie Risk Advisory in this sandbox)
**Target:** Q1 2027
**Effort:** ~20 hours (template + first report)
**Cost estimate:** $0 (existing tools)

### GAP-03 (Medium): Quarterly privileged access attestation not running

**Linked CC:** CC6.3
**Linked risk:** R-01 (Privileged Account Compromise)
**Linked POA&M:** POA&M-02

**Current state:** Leaver process is documented and operational. Joiner process is documented and operational. Quarterly attestation of existing privileged accounts is NOT running.

**Gap:** Without quarterly attestation, stale privileged accounts accumulate over time. CC6.3 (access removal) is Partial because removal-on-departure works but removal-on-role-change doesn't have a systematic check.

**Remediation:**
1. Generate quarterly report of all privileged accounts from Auth0
2. Security Lead reviews and attests each account (still needed? same scope?)
3. Revoke accounts no longer needed
4. Document review and remediation in change log

**Owner:** Security Lead
**Target:** Q4 2026 (first quarterly review)
**Effort:** ~8 hours per quarter
**Cost estimate:** $0 (existing Auth0 reporting)

### GAP-04 (Medium): Vendor onboarding checklist not codified

**Linked CC:** CC3.4
**Linked risk:** R-04

**Current state:** Vendor onboarding is informal — driven by procurement + security review on a case-by-case basis.

**Gap:** Without a codified checklist, vendor onboarding is inconsistent. New vendors may skip security review steps. CC3.4 (change / onboarding) is Partial.

**Remediation:**
1. Draft vendor onboarding checklist: vendor security questionnaire, SOC 2 report request, security rating baseline, contract security addendum review, TPRM tier assignment
2. Approve checklist in TPRM policy update
3. Train procurement team on checklist usage
4. First checklist-driven onboarding: any new Tier 1 vendor in Q1 2027

**Owner:** TPRM Lead
**Target:** Q4 2026
**Effort:** ~12 hours (draft + approve + train)
**Cost estimate:** $0

### GAP-05 (Medium): Vendor fraud risk assessment not performed

**Linked CC:** CC3.3
**Linked risk:** R-04, plus fraud-specific scenarios

**Current state:** Vendor security review covers data protection and access controls. Fraud-specific risks (BEC, social engineering, payment redirect) are not formally assessed.

**Gap:** Vendor fraud is a top-of-mind risk for FinTech SOC 2 audits. CC3.3 (fraud risk) requires explicit consideration.

**Remediation:**
1. Add fraud risk assessment step to vendor onboarding (for Tier 1 vendors)
2. Specific scenarios: BEC attempts, payment redirect, fake invoice, vendor impersonation
3. Test via tabletop exercise: simulate BEC against finance team with Payment Gateway vendor
4. Document results, assign remediation actions

**Owner:** TPRM Lead + Security Lead
**Target:** Q1 2027 (tabletop), Q2 2027 (documentation)
**Effort:** ~24 hours (tabletop + documentation)
**Cost estimate:** $0 (internal exercise)

### GAP-06 (Low): BEC tabletop exercise result not documented

**Linked CC:** CC7.4 (incident response validation)
**Linked risk:** R-04

**Current state:** IRP exists. Tabletop exercises scheduled but not yet executed (POA&M-10).

**Gap:** Without documented tabletop result, AtlasPay cannot demonstrate IR readiness to SOC 2 auditors. Low severity because the IRP itself is documented and the tabletop is scheduled.

**Remediation:**
1. Execute BEC tabletop scenario per POA&M-10
2. Document results: time-to-detect, time-to-respond, gaps identified
3. Update IRP based on tabletop lessons learned
4. File tabletop report in evidence repository

**Owner:** Security Lead
**Target:** Q1 2027
**Effort:** ~16 hours (exercise + documentation)
**Cost estimate:** $0

## POA&M cross-reference

All 6 gaps are already in the POA&M (see [[risk-register-board-2026-06-26#POA&M|Phase 1B POA&M]]). No new POA&M items added by gap assessment.

| Gap | POA&M | Severity |
|---|---|---|
| GAP-01 | POA&M-03 | High |
| GAP-02 | (new for Phase 2) | High |
| GAP-03 | POA&M-02 | Medium |
| GAP-04 | (new for Phase 2) | Medium |
| GAP-05 | (new for Phase 2) | Medium |
| GAP-06 | POA&M-10 | Low |

## Audit readiness projection

| Quarter | Projected readiness | Gates cleared |
|---|---|---|
| Q4 2026 | 85% | GAP-03, GAP-04 closed (CC6.3, CC3.4 to Met) |
| Q1 2027 | 95% | GAP-01, GAP-02, GAP-06 closed (CC9.2, CC1.2, CC4.2, CC7.4 to Met) |
| Q2 2027 | 100% | GAP-05 closed (CC3.3 to Met) |

**Audit window recommendation:** Q2 2027 onward for full SOC 2 Type 1 audit (after Q2 2027 gap closure).

## Evidence trail

- `raw/clients/atlaspay/control-matrix-soc2-2026-06-26.md` — Phase 1C matrix that surfaced these gaps
- `raw/clients/atlaspay/risk-register-board-2026-06-26.md` — Phase 1B POA&M
- [[AtlasPay]] — entity page
- [[SOC2-Type1-Readiness-Workflow]] — engagement pattern