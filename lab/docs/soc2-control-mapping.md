# SOC 2 Type 1 Trust Services Criteria  -  Control Mapping

**Engagement:** AtlasPay FinTech SOC 2 Type 1 Readiness Assessment
**Period:** FY 2026 Q3 audit window (target)
**Scope:** Common Criteria (CC) + Availability (A) + Confidentiality (C)
**Excluded:** Processing Integrity (PI), Privacy (P)  -  not in scope for this engagement
**Framework:** SOC 2 Trust Services Criteria, Revision 2022
**Reference:** `urn:intuitem:risk:library:soc2-2017-rev-2022` (loaded in CISO Assistant)

## Status Legend

- ✅ **Covered**  -  Control is designed and operating; evidence available
- ⚠️ **Partial**  -  Control exists but evidence is incomplete or remediation in progress
- ❌ **Missing**  -  Control does not exist or no evidence available
- 🟡 **[LAB-SYNTHETIC]**  -  Evidence item is fabricated for portfolio demonstration; clearly marked; do not replicate for real client work without proper authorization

---

## Common Criteria (CC)  -  22 criteria

### CC1  -  Control Environment

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC1.1** | COSO Principle 1: Integrity & Ethical Values | SA-01 (Acceptable Use), TPRM-01 | R-05 (Insider) |  -  | ⚠️ Partial | Code of Conduct documented in SA-01; annual employee attestation not yet implemented (FY 2026 Q4 target) |
| **CC1.2** | Board oversight |  -  |  -  |  -  | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Quarterly board reporting on security posture via Risk Committee charter (drafted 2026-06) |
| **CC1.3** | Management establishes structures, reporting lines, authorities | ACC-01, IR-01 |  -  |  -  | ⚠️ Partial | Org chart documented; reporting lines for security incidents in IR-01 |
| **CC1.4** | Background checks as part of hiring |  -  | R-05 (Insider) |  -  | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Pre-employment background check policy (drafted); vendor partner identified for FY 2026 Q4 onboarding |
| **CC1.5** | Accountability for policies | ACC-01, SA-01 |  -  |  -  | ⚠️ Partial | Policy attestation cadence not yet enforced; HR system integration planned Q4 2026 |

### CC2  -  Information and Communication

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC2.1** | Quality information for internal control |  -  |  -  |  -  | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Slack `#security-announcements` channel; monthly all-hands security update; quarterly board reporting |
| **CC2.2** | Internal communication of security responsibilities | SA-01, TPRM-01 |  -  |  -  | ⚠️ Partial | SA-01 covers acceptable use; new-hire onboarding includes security training |
| **CC2.3** | External communication of security commitments | IR-01 | R-04 (Vendor), R-06 (Logging) | V-01, V-02 | ⚠️ Partial | Customer-facing security page published; breach notification SLAs in IR-01 |
| **CC2.4** | Separate evaluations / independent assessments |  -  |  -  | V-05 (Monitoring) | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Annual penetration test by external firm; SOC 2 Type 1 audit (current engagement) |

### CC3  -  Risk Assessment

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC3.1** | Specifies suitable objectives | RA-ATLASPAY-SOC2 | All 6 risks |  -  | ✅ Covered | Risk Assessment container in CISO Assistant; engagement-defined risk tolerance |
| **CC3.2** | Identifies and analyzes risk | RA-ATLASPAY-SOC2 | All 6 risks | TPRM-01 (vendor risk) | ✅ Covered | 6 risk scenarios scored on 5x5 ISO-27005 matrix; vendor risk tiers assigned |
| **CC3.3** | Considers potential for fraud | RA-ATLASPAY-SOC2, TPRM-01 | R-04 (Vendor), R-05 (Insider) | V-02 (Payment Gateway) | ✅ Covered | R-04 and R-05 explicitly address fraud scenarios; payment gateway controls documented |
| **CC3.4** | Identifies and assesses changes that could significantly impact the system | RA-ATLASPAY-SOC2 |  -  |  -  | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Quarterly Risk Committee meeting minutes; risk register review at each meeting |
| **CC3.5** | Documentation of risk assessment | RA-ATLASPAY-SOC2 | All 6 risks |  -  | ✅ Covered | Risk register and treatment plans documented in `lab/soc2-risk-register.md` |

### CC5  -  Control Activities

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC5.1** | Selects and develops control activities | All 4 policies | All 6 risks | V-01 to V-07 | ⚠️ Partial | Policy library covers major risks; gaps in CC7.1, CC8.1 (see below) |
| **CC5.2** | Selects and develops general control activities over technology | ACC-01, IR-01 | R-01, R-02, R-06 | V-01, V-03, V-04, V-05 | ⚠️ Partial | Identity & access controls documented; vuln mgmt documented in CC7.1; change mgmt in CC8.1 |
| **CC5.3** | Deploys through policies and procedures | All 4 policies |  -  |  -  | ⚠️ Partial | Policy lifecycle (review, approval, distribution) not yet formalized |

### CC6  -  Logical and Physical Access

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC6.1** | Logical access security software, infrastructure, and architectures | ACC-01 | R-01 (Priv Account) | V-03 (Identity Provider) | ✅ Covered | Identity Provider (V-03) enforces SSO + MFA; ACC-01 covers privileged access |
| **CC6.2** | New user provisioning authorization | ACC-01 | R-01 | V-03 | ⚠️ Partial | Manual approval workflow in place; automated provisioning via V-03 in progress (target Q4 2026) |
| **CC6.3** | User access removal | ACC-01 | R-01, R-05 | V-03 | ⚠️ Partial | Offboarding procedure within 4 hours documented; automation target Q4 2026 |
| **CC6.4** | Physical access restrictions |  -  |  -  | V-01 (AWS), V-04 (K8s) | ✅ Covered | AWS data centers + K8s control plane access; vendor-managed |
| **CC6.5** | Data disposal |  -  |  -  | V-01 | ⚠️ Partial | AWS data lifecycle policies (lab-synthetic); secure delete for customer data |
| **CC6.6** | Logical access encryption | ACC-01 | R-02 (Payment Exfil) | V-01, V-02, V-03 | ✅ Covered | At-rest encryption via V-01 KMS; tokenization via V-02 |
| **CC6.7** | Transmission encryption | ACC-01 | R-02, R-04 | V-01, V-02, V-03 | ✅ Covered | TLS 1.3 enforced at all egress points; mTLS for internal service mesh via V-04 |
| **CC6.8** | Malicious software prevention, detection, correction | ACC-01, IR-01 | R-03 (Ransomware) | V-05 (Monitoring) | ⚠️ Partial | EDR deployed on production hosts; SIEM (V-05) monitors for malware indicators |

### CC7  -  System Operations

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC7.1** | Detects vulnerabilities to system components |  -  | R-03, R-04 | V-05 | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Quarterly external penetration test + monthly internal vulnerability scan via V-05 |
| **CC7.2** | Monitors system components and operation | IR-01, TPRM-01 | R-06 (Logging) | V-05 | ✅ Covered | Centralized SIEM (V-05) with 90-day hot retention + 6-year cold archive per FFIEC retention pattern |
| **CC7.3** | Detects and acts upon security events | IR-01 | R-06 | V-05 | ✅ Covered | SIEM alerting rules; on-call rotation documented in IR-01 |
| **CC7.4** | Responds to identified security incidents | IR-01 | All 6 risks | V-05 | ✅ Covered | Incident Response Policy (IR-01) with severity classification, escalation paths, communication plan |
| **CC7.5** | Recovery from identified security incidents | IR-01 | R-03 (Ransomware) | V-01 | ⚠️ Partial | Backup restore procedure documented (lab-synthetic); annual tabletop exercise; full hot-standby not yet deployed |

### CC8  -  Change Management

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC8.1** | Authorizes, designs, develops, tests, implements changes |  -  | R-03 | V-04 (App Platform) | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | V-04 GitOps workflow with PR review + CI/CD; CAB for production deploys |

### CC9  -  Risk Mitigation

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **CC9.1** | Identifies, selects, and develops risk mitigation activities | TPRM-01, all 4 policies | All 6 risks |  -  | ✅ Covered | Risk treatment plans (mitigate) for all 6 risks; TPRM-01 governs vendor risk |
| **CC9.2** | Assesses and manages risks associated with vendors and business partners | TPRM-01 | R-04 (Vendor) | All 7 vendors | ✅ Covered | 7 vendors with MSAs, tier classification, annual SOC 2 Type 2 review for Tier-1 |

## Availability (A)  -  3 criteria

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **A1.1** | Current capacity demand maintained |  -  |  -  | V-01, V-05 | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | AWS auto-scaling; CloudWatch capacity dashboards; monthly capacity reviews |
| **A1.2** | Environmental protections, software, data backup, recovery infrastructure |  -  | R-03 | V-01, V-04 | ✅ Covered | AWS multi-AZ deployment; immutable backup snapshots; K8s control plane HA |
| **A1.3** | Tests recovery plan procedures | IR-01 | R-03 | V-01 | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | Quarterly restore-from-backup tests; annual tabletop for full DR scenario |

## Confidentiality (C)  -  2 criteria

| Criterion | Description | Mapped Policies | Mapped Risks | Mapped Vendors | Status | Evidence |
|---|---|---|---|---|---|---|
| **C1.1** | Identifies confidential information, determines retention, disposes | TPRM-01, ACC-01 | R-04 | V-01, V-07 (Data Warehouse) | ⚠️ Partial | Customer PII classification documented; data retention schedule in Records Retention Policy |
| **C1.2** | Disposes confidential information |  -  | R-04 | V-01 | ⚠️ Partial 🟡 [LAB-SYNTHETIC] | AWS data lifecycle policies; secure delete for retiring customer data; 7-year retention per financial regs |

---

## Coverage Summary

| Category | Total Criteria | Covered | Partial | Missing |
|---|---|---|---|---|
| CC1 Control Environment | 5 | 0 | 5 | 0 |
| CC2 Information & Communication | 4 | 0 | 4 | 0 |
| CC3 Risk Assessment | 5 | 3 | 2 | 0 |
| CC5 Control Activities | 3 | 0 | 3 | 0 |
| CC6 Logical & Physical Access | 8 | 4 | 4 | 0 |
| CC7 System Operations | 5 | 3 | 2 | 0 |
| CC8 Change Management | 1 | 0 | 1 | 0 |
| CC9 Risk Mitigation | 2 | 2 | 0 | 0 |
| A Availability | 3 | 1 | 2 | 0 |
| C Confidentiality | 2 | 0 | 2 | 0 |
| **Total** | **38** | **13 (34%)** | **25 (66%)** | **0 (0%)** |

**For a SOC 2 Type 1 readiness engagement, this is the realistic distribution.** Type 1 audits test the design of controls at a point in time, not their operating effectiveness over a period (that's Type 2). 34% fully covered + 66% partial-with-remediation-roadmap is the expected profile for an early-stage FinTech entering its first audit cycle.

---

## [LAB-SYNTHETIC] Evidence Items  -  Honest Disclosure

The following 8 evidence items are **fabricated for portfolio demonstration only**. They reflect controls that are realistic for an early-stage FinTech SOC 2 Type 1 engagement, but the underlying artifacts (meeting minutes, penetration test reports, GitOps CAB logs) do not exist. They are clearly marked throughout this document with the 🟡 [LAB-SYNTHETIC] tag.

In a real client engagement, fabricated evidence would be audit fraud. This document treats them as illustrative scenarios for portfolio demonstration.

| # | Item | Real Engagement Substitute |
|---|---|---|
| 1 | CC1.2 Quarterly board reporting on security posture | Actual board meeting minutes from the period under audit |
| 2 | CC1.4 Pre-employment background check policy | HR onboarding documentation + vendor contract with background check provider |
| 3 | CC2.1 Slack channel + monthly all-hands security update | Communication logs, meeting recordings, attendance records |
| 4 | CC2.4 Annual penetration test by external firm | Pen test reports, remediation tracking |
| 5 | CC3.4 Quarterly Risk Committee meeting minutes | Actual meeting minutes, attendance, action items |
| 6 | CC7.1 Quarterly pen test + monthly vuln scans | Scan reports, remediation tickets, CVE tracking |
| 7 | CC8.1 V-04 GitOps + CAB for production deploys | PR logs, CI/CD pipeline configs, CAB meeting minutes |
| 8 | A1.1, A1.3, C1.2 Capacity planning, recovery testing, data disposal | AWS architecture diagrams, test reports, lifecycle policy JSON |

---

## Mapped Artifacts in AtlasPay Sandbox

- **CISO Assistant folder:** AtlasPay (`d272ee78-ef71-4a70-8235-df2335cd0b3c`)
- **Risk Assessment:** RA-ATLASPAY-SOC2 (AtlasPay SOC 2 Readiness Risk Assessment, status: in_progress)
- **Risk Matrix:** AtlasPay 5x5 (urn:atlaspay-5x5)
- **Frameworks loaded:** SOC2-2017 Trust Services Criteria (revision 2022), NIST CSF, ISO 27001:2022 (via mapping libraries)
- **Policies:** ACC-01, IR-01, SA-01, TPRM-01 (4 total, all in Compliance sub-folder)
- **Vendors:** V-01 to V-07 with V-XX-MSA contracts
- **Risks:** R-01 to R-06

---

**Last Updated:** 2026-06-25 01:15 EDT
**Engagement:** Phase 1B  -  SOC 2 Control Mapping
**Engagement Status:** Ready for Phase 1C (Gap Assessment)