<div class="lab-tag">[LAB-SYNTHETIC]</div>

# AtlasPay SOC 2 Type 1 Readiness — Executive Briefing

**Document Type:** Executive Briefing
**Engagement:** AtlasPay SOC 2 Type 1 Readiness
**Phase:** 2 (Re-engagement after Phase 1 baseline)
**Date:** 2026-06-26
**Prepared by:** Ijezie Risk Advisory
**Document Version:** 1.0
**Status:** Final

---

## Executive Summary

AtlasPay has engaged Ijezie Risk Advisory to prepare the organization for SOC 2 Type 1 audit readiness, targeting Q2 2027 audit window. Phase 1 (2026-06-24 to 2026-06-25) established the baseline: 6 risk scenarios, 4 policies, 7 vendors, 1 risk assessment. Phase 2 (this document) advances AtlasPay from baseline to 85% audit-ready through gap remediation and control documentation.

**Bottom line:** AtlasPay has strong technical controls but incomplete documentation and reporting cadence. The 6 identified gaps are administrative, not technical. All can be remediated within 2 quarters at low cost.

## Engagement Scope

| Category | In Scope |
|---|---|
| Trust Services Categories | Security (Common Criteria), Availability, Confidentiality |
| Perimeters | AtlasPay Core Payment System, AtlasPay Internal Infrastructure, AtlasPay-Payments, AtlasPay-Data |
| Risk Scenarios | R-01..R-06 |
| Policies | 4 (Access Control, Incident Response, Security Awareness, Third-Party Risk) |
| Vendors | 7 (Cloud, Payment Gateway, Identity, App Platform, Monitoring, Finance, Data Warehouse) |
| Audit Window | Q2 2027 (planned) |

## Risk Register Summary

| Ref | Risk | Inherent | Current | Residual | Treatment |
|---|---|---|---|---|---|
| R-01 | Privileged Account Compromise | Very High | Medium | Medium | mitigate |
| R-02 | Payment Data Exfiltration via API | Very High | Medium | Medium | mitigate |
| R-03 | Ransomware on Production Database Host | High | Medium | Medium | mitigate |
| R-04 | Third-Party SaaS Breach | High | High | High | mitigate |
| R-05 | Insider Threat (Malicious Employee) | High | High | Medium | mitigate |
| R-06 | Insufficient Audit Logging | High | Low | Low | mitigate |

**Aggregate residual:** 0 very high, 1 high (R-04), 4 medium, 1 low, 0 very low.

**Honest-call note:** R-04 (Third-Party SaaS Breach) retains residual High because vendor compromise cannot be eliminated through AtlasPay's controls alone — only managed via contractual requirements, continuous monitoring, and incident response readiness. This is the realistic ceiling for third-party risk.

## Board-Relevant Risks (4 of 6)

| Ref | Risk | Residual | Why Board-Relevant |
|---|---|---|---|
| R-01 | Privileged Account Compromise | Medium | Insider access risk; board audit committee focus |
| R-04 | Third-Party SaaS Breach | High | Single highest residual; cannot be eliminated |
| R-05 | Insider Threat | Medium | People risk; audit committee and HR coordination |
| R-06 | Insufficient Audit Logging | Low | Foundational control; if logging fails, all controls fail |

## Control Coverage

40 SOC 2 criteria evaluated (33 Common Criteria + 3 Availability + 1 Confidentiality + 3 expanded). 31 Met (78%), 8 Partial (20%), 1 Missing (2%), 0 N/A.

| Category | Met | Partial | Missing | N/A |
|---|---|---|---|---|
| CC1 Control Environment | 4 | 1 | 0 | 0 |
| CC2 Communication | 3 | 0 | 0 | 0 |
| CC3 Risk Assessment | 2 | 2 | 0 | 0 |
| CC4 Monitoring | 1 | 1 | 0 | 0 |
| CC5 Control Activities | 3 | 0 | 0 | 0 |
| CC6 Logical Access | 6 | 2 | 0 | 0 |
| CC7 System Operations | 5 | 0 | 0 | 0 |
| CC8 Change Management | 1 | 0 | 0 | 0 |
| CC9 Risk Mitigation | 1 | 1 | 0 | 0 |
| A1 Availability | 3 | 0 | 0 | 0 |
| C1 Confidentiality | 2 | 1 | 1 | 0 |

## Gap Assessment Summary

| Severity | Count | Examples |
|---|---|---|
| Critical | 0 | None |
| High | 2 | Vendor SOC 2 collection; Board reporting cadence |
| Medium | 3 | Quarterly access attestation; Vendor onboarding checklist; Vendor fraud assessment |
| Low | 1 | BEC tabletop exercise result |

**Audit readiness projection:**
- Q4 2026: 85% (Medium gaps closed)
- Q1 2027: 95% (High gaps closed)
- Q2 2027: 100% (Low gap closed, audit-ready)

## POA&M (Plan of Action & Milestones)

14 POA&M items total. 3 In Progress, 11 Open. Top 5 by severity:

| Item | Linked Risk | Action | Owner | Target |
|---|---|---|---|---|
| POA&M-01 | R-01 | Implement PAM tool with session recording | CISO | Q4 2026 |
| POA&M-03 | R-04 | Collect Tier 1 vendor SOC 2 Type 2 reports | TPRM Lead | Q1 2027 |
| POA&M-04 | R-04 | Continuous security rating monitoring | TPRM Lead | Q1 2027 |
| POA&M-05 | R-04 | Vendor breach notification SLA in MSA | Legal | Q4 2026 |
| POA&M-06 | R-05 | Annual background checks | HR | Q4 2026 |

## Engagement Timeline

| Phase | Activity | Window | Status |
|---|---|---|---|
| Phase 1 | Baseline + risk register | 2026-06-24 to 2026-06-25 | Complete |
| Phase 2 | Control matrix + gap assessment | 2026-06-26 | Complete (this engagement) |
| Phase 3 | Gap remediation (POA&M execution) | Q4 2026 to Q1 2027 | Pending |
| Phase 4 | Audit window | Q2 2027 | Pending |

## Engagement Economics

| Item | Estimate |
|---|---|
| Total effort (Phase 1 + Phase 2) | ~9 hours focused |
| Phase 3 effort estimate (POA&M execution) | ~120 hours over 2 quarters |
| Phase 4 audit cost (separate engagement) | $25K-$50K (typical SOC 2 Type 1 audit) |
| IfeSec engagement fee (this engagement) | $7,500 (SOC 2 readiness, mid-tier package) |

## Engagement Outcome

AtlasPay is positioned for SOC 2 Type 1 audit readiness by Q2 2027. The 6 identified gaps are administrative in nature and require documentation + cadence changes rather than new control implementations. All gaps have assigned owners, target dates, and remediation actions in the POA&M.

---

**[LAB-SYNTHETIC]** This document is a portfolio demonstration artifact for Ijezie Risk Advisory's vCISO capability. AtlasPay is a fictional FinTech persona; all data is illustrative. For real client engagements, the structure remains the same but the content reflects actual assessments, evidence, and stakeholder interviews.

**Ijezie Risk Advisory** — Solo vCISO consulting, NIST-first methodology, SOC 2 / ISO 27001 / HIPAA / FFIEC.