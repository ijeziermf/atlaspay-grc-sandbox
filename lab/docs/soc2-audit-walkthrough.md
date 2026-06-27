# SOC 2 Type 1 Audit Walkthrough  -  Management Response

**Engagement:** AtlasPay FinTech SOC 2 Type 1 Readiness
**Walkthrough Date:** 2026-06-25
**Auditor:** vCISO Engagement Team (synthetic walkthrough for portfolio demonstration)
**Audit Type:** SOC 2 Type 1  -  design of controls at a point in time

## Walkthrough Structure

This document captures the audit walkthrough simulation performed during the SOC 2 Type 1 readiness engagement. The auditor walked the AtlasPay control environment using the risk register, policies, vendor list, and other artifacts in CISO Assistant. Findings represent what a real auditor would surface during a Type 1 walkthrough.

**Note:** This is a **synthetic walkthrough** for portfolio demonstration. The findings reflect realistic gaps for an early-stage FinTech SOC 2 Type 1 engagement. The management responses are illustrative  -  in a real engagement, the client's actual responses would be documented here.

---

## Walkthrough Questions and AtlasPay Responses

### Q1: Risk Register Walk  -  R-04 (Third-Party SaaS Breach) Residual Acceptance

**Auditor Question:** R-04 has residual risk of High. Walk me through your risk acceptance. Who signed off?

**AtlasPay Response:** "The Risk Committee accepted this residual at the Q2 2026 meeting based on three factors: (1) the TPRM program with annual SOC 2 Type 2 review for Tier-1 vendors, (2) contractual breach notification SLAs at 72 hours and sub-processor notification rights, and (3) cyber insurance coverage for vendor breach scenarios. The Risk Committee charter authorizes residual risk acceptance up to High without board escalation."

**Auditor Follow-up:** Show me the meeting minutes documenting this acceptance decision.

**AtlasPay Response:** "Minutes are in our shared drive. I'll send them after this walkthrough."

**Auditor Note:** Request minutes; verify Risk Committee charter scope. **Finding AW-13** if minutes cannot be produced.

---

### Q2: Policy Lifecycle and Attestation

**Auditor Question:** How do you communicate policy changes to employees? How do you know employees have read them?

**AtlasPay Response:** "We push policy updates via Slack #security-announcements and require acknowledgment in V-03 (Identity Provider) at next login. Annual re-attestation reminder via email."

**Auditor Follow-up:** Show me the attestation record for SA-01. I want the date each employee acknowledged the current version.

**AtlasPay Response:** "V-03 holds the attestation records but we haven't configured the reporting yet. Engineering is working on the dashboard."

**Auditor Note:** **Finding AW-07** (Policy attestation records).

---

### Q3: Change Management

**Auditor Question:** Walk me through your last production deployment.

**AtlasPay Response:** "All production deploys go through V-04 (Application Platform) GitOps workflow. PR review required, CI/CD pipeline runs automated tests, deployment is automated, rollback is automated. We have a Change Advisory Board (CAB) meeting weekly for production changes."

**Auditor Follow-up:** Show me the CAB meeting minutes, the change request ticket, and the post-deployment review.

**AtlasPay Response:** "The CAB meetings happen informally. We document decisions in Slack threads. We don't have formal meeting minutes."

**Auditor Note:** **Finding AW-04** (Change management documentation).

---

### Q4: Vulnerability Management

**Auditor Question:** When was your last penetration test? What were the findings?

**AtlasPay Response:** "We have V-05 (Monitoring Tools) for internal scanning. We were planning to engage an external pen test firm for Q3 2026 but haven't done one yet."

**Auditor Follow-up:** Show me the pen test report or the internal scan reports.

**AtlasPay Response:** "V-05 dashboards exist but we haven't been saving scan reports."

**Auditor Note:** **Finding AW-03** (Penetration test reports) and **Finding AW-06** (Vulnerability scan reports).

---

### Q5: Vendor Risk

**Auditor Question:** Walk me through your Tier 1 vendor risk review.

**AtlasPay Response:** "V-01 (Cloud), V-02 (Payment Gateway), V-03 (IdP) are our critical vendors. Last review was informal during the Q1 2026 planning cycle. We reviewed their SOC 2 Type 2 reports and confirmed no material findings."

**Auditor Follow-up:** Show me the tier classification document, the Q1 review minutes, and the SOC 2 Type 2 reports for V-01, V-02, V-03.

**AtlasPay Response:** "Tier classification is in TPRM-01 but not formalized as a separate document. I have the SOC 2 Type 2 reports in my files. Q1 review minutes weren't captured."

**Auditor Note:** **Finding AW-01** (Vendor tier classification) and **Finding AW-13** (Risk acceptance documentation).

---

### Q6: Background Checks

**Auditor Question:** How do you vet new hires before granting production access?

**AtlasPay Response:** "We have a background check policy in draft. The vendor selection is in progress. Currently we don't conduct formal background checks."

**Auditor Follow-up:** When will this be operational? What's your interim control?

**AtlasPay Response:** "Target is Q3 2026 to be operational. Interim, we rely on reference checks and probationary period review."

**Auditor Note:** **Finding AW-02** (Background check program).

---

### Q7: Incident Response

**Auditor Question:** Describe your last security incident.

**AtlasPay Response:** "We had a BEC attempt targeting a commercial customer in Q4 2025. Caught by callback verification, contained within 4 hours, customer notified within contractual SLA. Post-incident review documented in IR-01 addendum."

**Auditor Follow-up:** Show me the IR-01 activation log, decision log, customer notification timestamps, and PIR.

**AtlasPay Response:** "I have the documentation. Will share after this walkthrough."

**Auditor Note:** Verify when provided. **No finding expected if documentation is complete.**

---

### Q8: Recovery Testing

**Auditor Question:** When was your last recovery test?

**AtlasPay Response:** "We have backup procedures documented but haven't formalized recovery testing. Restore-from-backup was tested informally during a Q1 2026 incident response."

**Auditor Follow-up:** Show me the test report with measured RTO/RPO.

**AtlasPay Response:** "We don't have a formal report. The team can describe what happened."

**Auditor Note:** **Finding AW-05** (Recovery testing) and **Finding AW-12** (DR plan documentation).

---

### Q9: Board Reporting

**Auditor Question:** What does the board know about security posture?

**AtlasPay Response:** "Risk Committee meets quarterly. Security is a standing agenda item. Reports include incident count, vuln status, training completion."

**Auditor Follow-up:** Show me the Q1 and Q2 2026 board reports.

**AtlasPay Response:** "Verbal updates have been given. Formal written reports are being developed."

**Auditor Note:** **Finding AW-08** (Board reporting documentation).

---

### Q10: Personnel Security

**Auditor Question:** Employee terminated March 15. When was their production access revoked?

**AtlasPay Response:** "Within 4 hours of termination per our offboarding procedure. V-03 audit log shows the access revocation."

**Auditor Follow-up:** Show me the termination ticket, access revocation ticket, audit log entry, offboarding checklist.

**AtlasPay Response:** "Termination is in HRIS. V-03 audit log will show the revocation. Offboarding checklist is on a shared spreadsheet."

**Auditor Note:** Verify ticket retention. **Finding AW-14** if offboarding documentation not retained systematically.

---

## Audit Findings Summary

| ID | Finding | Severity | TSC Criterion | Remediation |
|---|---|---|---|---|
| AW-01 | Vendor tier classification not formalized | 🟡 Medium | CC9.2 | Document tier criteria in TPRM-01; re-classify V-01 to V-07 |
| AW-02 | Background check program not operational | 🟠 High | CC1.4 | Select vendor, sign MSA, integrate with HRIS, update onboarding |
| AW-03 | Penetration test reports missing | 🟠 High | CC2.4, CC7.1 | Engage external pen test firm for Q3 2026 |
| AW-04 | Change management documentation missing | 🟠 High | CC8.1 | Document V-04 GitOps workflow as formal Change Mgmt Policy; establish CAB cadence |
| AW-05 | Recovery test reports missing | 🟡 Medium | A1.3 | Establish quarterly recovery test cadence with documented reports |
| AW-06 | Vulnerability scan reports missing | 🟠 High | CC7.1 | Configure V-05 weekly scans; retain reports; establish remediation SLA |
| AW-07 | Policy attestation records missing | 🟡 Medium | CC1.1, CC1.5 | Configure V-03 attestation; integrate with HRIS |
| AW-08 | Board reporting documentation missing | 🟡 Medium | CC1.2, CC2.1 | Develop board reporting template; document Q1-Q2 2026 retroactively |
| AW-09 | Org chart outdated | 🟢 Low | CC1.3 | Update org chart; quarterly review cadence |
| AW-10 | Tabletop exercise reports missing | 🟡 Medium | CC7.4, CC7.5 | Schedule annual tabletop; engage external facilitator |
| AW-11 | Records Retention Policy missing | 🟢 Low | CC3.5, C1.1 | Document master retention schedule |
| AW-12 | Disaster Recovery Plan document missing | 🟡 Medium | A1.3, CC7.5 | Document DR plan with RTO/RPO targets |
| AW-13 | Risk acceptance documentation missing | 🟡 Medium | CC3.4 | Document Risk Committee meeting minutes; risk acceptance memos |
| AW-14 | Offboarding ticket retention unclear | 🟢 Low | CC6.3 | Configure HRIS-V-03 integration for systematic ticket retention |

**Severity distribution:** 0 Critical, 3 High, 8 Medium, 3 Low, 0 Missing

---

## Management Response

AtlasPay's management response to each finding is documented below. Management has reviewed the findings, agrees with the severity ratings, and has committed to remediation timelines.

### AW-01 (Vendor Tier Classification)

**Management Response:** Concur. CISO will document tier classification criteria in TPRM-01 within 2 weeks. Vendor Management Officer will re-classify V-01 through V-07 against documented criteria within 4 weeks.

**Owner:** CISO + Vendor Management Officer
**Target Completion:** 2026-07-23

### AW-02 (Background Check Program)

**Management Response:** Concur. Head of People has initiated vendor selection. Target vendor on-boarded by 2026-08-15. HRIS integration target Q4 2026.

**Owner:** Head of People + CISO
**Target Completion:** 2026-08-15 (vendor on-boarded); 2026-10-31 (HRIS integration)

### AW-03 (Penetration Test Reports)

**Management Response:** Concur. CISO has engaged [penetration testing firm] for external pen test. Test scheduled for 2026-08-15 through 2026-08-22. Report delivery 2026-09-01.

**Owner:** CISO
**Target Completion:** 2026-09-01 (initial report); 2026-10-01 (remediation verified)

### AW-04 (Change Management Documentation)

**Management Response:** Concur. CTO will document V-04 GitOps workflow as formal Change Management Policy within 2 weeks. CAB meeting cadence established weekly.

**Owner:** CTO + CISO
**Target Completion:** 2026-07-15 (documentation); ongoing (CAB cadence)

### AW-05 (Recovery Testing)

**Management Response:** Concur. Engineering Lead will document RTO/RPO targets per system within 2 weeks. Quarterly recovery test cadence established.

**Owner:** Engineering Lead + CISO
**Target Completion:** 2026-07-15 (RTO/RPO documentation); 2026-09-30 (first formal test report)

### AW-06 (Vulnerability Scan Reports)

**Management Response:** Concur. CISO will configure V-05 weekly authenticated scans within 1 week. Remediation SLA: Critical 7 days, High 30 days, Medium 90 days.

**Owner:** CISO + Engineering Lead
**Target Completion:** 2026-07-08 (scan configuration); 2026-08-15 (first full month of reports)

### AW-07 (Policy Attestation Records)

**Management Response:** Concur. CISO will configure V-03 attestation reporting within 3 weeks. HRIS integration target Q4 2026.

**Owner:** CISO + Head of People
**Target Completion:** 2026-08-15 (V-03 configuration); 2026-10-31 (HRIS integration)

### AW-08 (Board Reporting Documentation)

**Management Response:** Concur. CISO will develop board reporting template within 2 weeks. Q1 and Q2 2026 reports will be documented retroactively based on Risk Committee minutes.

**Owner:** CISO
**Target Completion:** 2026-07-22

### AW-09 (Org Chart)

**Management Response:** Concur. Head of People will update org chart within 1 week. Quarterly review cadence established.

**Owner:** Head of People
**Target Completion:** 2026-07-08

### AW-10 (Tabletop Exercise)

**Management Response:** Concur. CISO has engaged [external facilitator] for Q4 2026 tabletop exercise. Scenarios: ransomware on production DB (R-03), payment data breach (R-02), vendor breach (R-04).

**Owner:** CISO
**Target Completion:** 2026-11-15 (exercise execution); 2026-12-15 (PIR documented)

### AW-11 (Records Retention Policy)

**Management Response:** Concur. Legal will document master Records Retention Policy within 2 weeks.

**Owner:** Legal + CISO
**Target Completion:** 2026-07-15

### AW-12 (Disaster Recovery Plan)

**Management Response:** Concur. Engineering Lead will document DR Plan within 4 weeks. Quarterly recovery tests per AW-05.

**Owner:** Engineering Lead + CISO
**Target Completion:** 2026-08-15

### AW-13 (Risk Acceptance Documentation)

**Management Response:** Concur. CISO will document Risk Committee charter and meeting cadence within 2 weeks. Q1 and Q2 2026 minutes documented retroactively.

**Owner:** CISO + CEO (Risk Committee Chair)
**Target Completion:** 2026-07-22

### AW-14 (Offboarding Ticket Retention)

**Management Response:** Concur. Head of People will configure HRIS-V-03 integration for systematic ticket retention within 4 weeks.

**Owner:** Head of People + Engineering Lead
**Target Completion:** 2026-08-22

---

## Audit Opinion (Synthetic)

**Type 1 Audit Opinion (Anticipated):**

Based on the walkthrough findings, the auditor would anticipate issuing a **qualified opinion** for the SOC 2 Type 1 report, with the qualification specifically addressing:
- AW-02 (Background check program)  -  controls not yet operational
- AW-03 (Penetration test reports)  -  no external attestation available
- AW-04 (Change management documentation)  -  control design informal
- AW-06 (Vulnerability scan reports)  -  scan cadence not yet established

The remaining 10 findings represent **design deficiencies** that, while material to control maturity, would be addressed in the management response and would not necessarily result in qualification if remediation is in progress.

For AtlasPay to obtain an **unqualified Type 1 opinion**, all High findings must be remediated and tested by the audit kickoff date (target: 2026-09-15).

---

## Engagement Status

| Phase | Status |
|---|---|
| Phase 0: Engagement State Verification | ✅ Complete |
| Phase 1A: Risk Register Finalization | ✅ Complete |
| Phase 1B: SOC 2 Control Mapping | ✅ Complete |
| Phase 1C: Gap Assessment | ✅ Complete |
| Phase 3: Audit Walkthrough Simulation | ✅ Complete |
| Phase 2A: Executive Briefing PDF | 🔄 Pending |
| Phase 2B: Risk Register PDF | 🔄 Pending |
| Phase 4: Repo Integration | 🔄 Pending |
| Phase 5: Skill Extraction | 🔄 Pending |

---

**Last Updated:** 2026-06-25 01:30 EDT
**Engagement:** Phase 3  -  Audit Walkthrough Simulation
**Engagement Status:** Ready for Phase 2 (PDF Generation)