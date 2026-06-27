<div class="lab-tag">[LAB-SYNTHETIC]</div>

# AtlasPay Policy Pack

**Document Type:** Policy Library (Summary + Pointer)
**Engagement:** AtlasPay SOC 2 Type 1 Readiness
**Date:** 2026-06-26
**Prepared by:** Ijezie Risk Advisory

---

## Purpose

This document is the pointer/manifest for AtlasPay's policy library. Each policy below exists as a separate document in the engagement repository and is mapped to the relevant SOC 2 Common Criteria, risks, and POA&M items. Full text of each policy is available in the corresponding `/policies/` directory.

---

## Policy Manifest

| Ref | Policy | Status | Priority | CSF Function | Linked CC | Linked Risks |
|---|---|---|---|---|---|---|
| ACC-01 | Access Control & Privileged Access Policy | Active | P2 | Protect | CC6.1, CC6.2, CC6.3, CC6.6, CC6.7 | R-01, R-02, R-05 |
| IR-01 | Incident Response Policy | Active | P1 | Respond | CC2.2, CC7.3, CC7.4, CC7.5 | R-03, R-04, R-06 |
| SA-01 | Security Awareness & Acceptable Use Policy | Active | P2 | Protect | CC1.1, CC1.4, CC1.5, CC2.1 | R-05 |
| TPRM-01 | Third-Party Risk Management Policy | Active | P2 | Govern | CC3.4, CC9.2 | R-04 |

---

## Policy Summaries (1-paragraph each)

### ACC-01: Access Control & Privileged Access Policy

Defines the principles of least privilege, role-based access control (RBAC), and privileged access management (PAM) for all AtlasPay systems. Covers user provisioning (joiner process via HR + Auth0), access removal (leaver process within 1 hour of termination), privileged access review (quarterly attestation), MFA enforcement, session recording for privileged accounts, and just-in-time access elevation. Mapped to SOC 2 CC6 (Logical and Physical Access) and CC5.2 (Technology Controls).

### IR-01: Incident Response Policy

Defines detection, triage, containment, eradication, and recovery procedures for security incidents. Includes severity classification (Critical/High/Medium/Low), escalation paths (security on-call → CISO → CEO → Board), customer notification triggers (state breach notification laws, contractual obligations), regulatory notification (SEC, state AGs), and post-incident review requirements. Tabletop exercises scheduled quarterly. Mapped to SOC 2 CC7 (System Operations) and CC2.2 (Internal Communication).

### SA-01: Security Awareness & Acceptable Use Policy

Defines annual security awareness training requirements (all employees + contractors), phishing simulation cadence (quarterly), acceptable use of corporate assets (laptops, mobile devices, cloud services), BYOD rules, and incident reporting obligations. Training completion is tied to performance review process. Mapped to SOC 2 CC1 (Control Environment) and CC2.1 (Internal Communication).

### TPRM-01: Third-Party Risk Management Policy

Defines vendor onboarding risk tiering (Tier 1/2/3 based on data access and criticality), inherent + residual risk assessment, annual reassessment cadence, contractual security requirements (SOC 2 Type 2 report, breach notification SLA, audit rights), ongoing monitoring (security ratings, breach disclosure monitoring), and offboarding procedures. Mapped to SOC 2 CC9.2 (Vendor Risk) and CC3.4 (Risk Assessment Changes).

---

## Planned Policies (not yet documented)

| Policy | Target | Linked Gap |
|---|---|---|
| Risk Management Policy | Q4 2026 | Establishes quarterly risk review cadence (CC3.1/3.2) |
| Data Classification Policy | Q1 2027 | C1.1 Confidentiality (F-07) |
| Data Retention & Disposal Policy | Q4 2026 | CC6.5 Data Disposal |
| Business Continuity Plan | Q1 2027 | A1.3 Disaster Recovery (POA&M-11) |
| Encryption & Key Management Policy | Q4 2026 | CC6.7 Data Transmission |
| Backup & Recovery Policy | Q4 2026 | CC7.5 Recovery |

---

**[LAB-SYNTHETIC]** This policy pack manifest is a portfolio demonstration artifact for Ijezie Risk Advisory's vCISO capability. AtlasPay is a fictional FinTech persona; the policies and their mappings are illustrative patterns for SOC 2 readiness engagements.

**Ijezie Risk Advisory**  -  Solo vCISO consulting, NIST-first methodology, SOC 2 / ISO 27001 / HIPAA / FFIEC.