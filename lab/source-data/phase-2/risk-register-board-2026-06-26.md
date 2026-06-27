---
type: source
title: AtlasPay Phase 2 Risk Register (Board-Relevant Subset)
created: 2026-06-26
updated: 2026-06-26
tags: [risk-register, atlaspay, soc2, board-ready]
raw_paths:
  - raw/clients/atlaspay/state-2026-06-26.md
status: active
---

# AtlasPay Phase 2 Risk Register (Board-Relevant Subset)

[LAB-SYNTHETIC] — This risk register is a portfolio demonstration artifact for Ijezie Risk Advisory's vCISO capability. AtlasPay is a fictional FinTech persona, not a real client.

## Board-relevant risks (4 of 6)

**Selection criteria:** Residual level ≥ High OR likelihood ≥ likely AND impact ≥ critical OR treatment-dependent OR audit-board focus.

| Ref | Risk | Residual | Why board-relevant |
|---|---|---|---|
| R-01 | Privileged Account Compromise | Medium | Insider access risk, board audit committee focus area |
| R-04 | Third-Party SaaS Breach (Vendor Compromise) | **High** | Single highest residual; can't be eliminated, only managed |
| R-05 | Insider Threat (Malicious Employee) | Medium | People risk, audit committee and HR coordination |
| R-06 | Insufficient Audit Logging | Low | Foundational control; if logging fails, all other controls fail |

## Non-board risks (2 of 6) — tracked at management level

| Ref | Risk | Residual | Why not board-level |
|---|---|---|---|
| R-02 | Payment Data Exfiltration via API | Medium | Technical control; managed by engineering + security ops |
| R-03 | Ransomware on Production Database Host | Medium | Operational risk; covered by IRP and BCP board reporting |

## Phase 1B Decisions (Hermes-driven, Ifeanyi-approved)

1. **R-04 residual stays High.** Per [[Honest-Call-Discipline]], third-party breach can't be reduced below current state. Mitigation actions exist but cannot eliminate source. Board reporting must reflect this honestly.

2. **R-06 logging risk reduced to Low after audit log forwarder** (Helix-era forwarder test artifact). Logging pipeline now streams to Datadog with retention + alerting. However, board reporting should note that audit log integrity depends on Datadog availability — a separate dependency to monitor.

3. **R-05 residual Medium is defensible** with HR background check + access review cadence. Honest-call note: insider threat residual can never drop to Low because humans are unpredictable; Medium is the realistic floor.

4. **Risk treatment is "mitigate" for all 6.** No accept / transfer / avoid calls. This is correct for a SOC 2 Type 1 readiness engagement where the audit expects mitigation evidence for every identified risk.

5. **Vendor risk (R-04) drives the Third-Party Risk Management Policy (TPRM-01).** Direct line of sight from risk → policy → control → evidence.

## Board narrative (1-paragraph version)

AtlasPay has 6 identified risk scenarios across the SOC 2 scope. Four are board-relevant due to residual severity or strategic exposure. The highest residual risk is third-party SaaS breach (R-04 at High), which reflects the structural reality that vendor compromise cannot be eliminated — only managed through contractual controls, continuous monitoring, and incident response readiness. The remaining 3 board-relevant risks (privileged access, insider threat, audit logging) sit at residual Medium with documented mitigation. Mitigation actions are tracked in the [[#POA&M|POA&M]] with assigned owners and target dates.

## POA&M (Plan of Action & Milestones)

| Item | Linked Risk | Severity | Action | Owner | Target | Status |
|---|---|---|---|---|---|---|
| POA&M-01 | R-01 | High | Implement PAM tool with session recording for all admin accounts | CISO | Q4 2026 | Open |
| POA&M-02 | R-01 | Medium | Quarterly privileged access review with attestation | Security Lead | Q4 2026 | Open |
| POA&M-03 | R-04 | High | Require SOC 2 Type 2 reports from all Tier 1 vendors annually | TPRM Lead | Q1 2027 | Open |
| POA&M-04 | R-04 | High | Continuous security rating monitoring (BitSight/SecurityScorecard) | TPRM Lead | Q1 2027 | Open |
| POA&M-05 | R-04 | High | Vendor breach notification SLA in MSA (≤24h) | Legal | Q4 2026 | Open |
| POA&M-06 | R-05 | Medium | Annual background checks for all employees with financial system access | HR | Q4 2026 | Open |
| POA&M-07 | R-05 | Medium | Quarterly access review for all production systems | Security Lead | Ongoing | In Progress |
| POA&M-08 | R-06 | Low | Quarterly audit log integrity test (sample 1% of events) | Security Ops | Q4 2026 | Open |
| POA&M-09 | R-02 | Medium | API rate limiting + anomaly detection on payment endpoints | Engineering | Q4 2026 | Open |
| POA&M-10 | R-03 | Medium | Quarterly ransomware tabletop exercise with IR team | Security Lead | Q1 2027 | Open |
| POA&M-11 | R-03 | Medium | Immutable backup verification + restore test (monthly) | Infrastructure | Ongoing | In Progress |
| POA&M-12 | R-06 | Low | Datadog availability dependency documented in BCP | Security Ops | Q4 2026 | Open |
| POA&M-13 | All | Medium | Annual security awareness training (100% completion) | HR | Annual | In Progress |
| POA&M-14 | All | Low | Update risk register quarterly with material changes | vCISO | Quarterly | In Progress |

**Summary:** 14 POA&M items. 3 In Progress, 11 Open. 5 High severity, 7 Medium, 2 Low.

## Open questions for Ifeanyi (Phase 1B)

- **Q-B1.** Should POA&M items have monetary estimates (cost-to-implement)? Adds business context for board.
  - **Recommendation:** Yes, but only at the line-item level for High-severity items. Avoids clutter.
- **Q-B2.** R-04 board narrative: do we include the specific vendor count (7 vendors, 0 with SOC 2 Type 2 reports today) or generalize?
  - **Recommendation:** Generalize for the board version. Specifics belong in the vendor register and TPRM program docs.
- **Q-B3.** R-05 "Medium is the realistic floor for insider threat" — is this defensible enough for a board, or do we need to cite a framework (e.g., NIST SP 800-53 AC-2(7) privileged user management)?
  - **Recommendation:** Cite the framework. Board members with security backgrounds will look for it.

## Evidence trail

- `raw/clients/atlaspay/state-2026-06-26.md` — Phase 1A live state
- [[AtlasPay]] — entity page with risk register summary
- [[Honest-Call-Discipline]] — the principle driving R-04 residual High
- [[SOC2-Type1-Readiness-Workflow]] — the engagement pattern this risk register serves