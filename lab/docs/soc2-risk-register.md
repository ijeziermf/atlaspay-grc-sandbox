# SOC 2 Type 1 Readiness  -  Risk Register

**Engagement:** AtlasPay FinTech SOC 2 Type 1 Readiness
**Period:** FY 2026 Q3 audit window (target)
**Source of truth:** CISO Assistant v3.18.3 (live state, folder `d272ee78-ef71-4a70-8235-df2335cd0b3c`)
**Risk Assessment container:** RA-ATLASPAY-SOC2 (AtlasPay SOC 2 Readiness Risk Assessment)
**Risk Matrix:** AtlasPay 5x5 (5 probability levels × 5 impact levels)

## Scoring Methodology

**Probability scale (1-5):**
1. Unlikely (1-5%)
2. Rather unlikely (5-25%)
3. Likely (25-50%)
4. Very likely (50-80%)
5. Almost certain (80%+)

**Impact scale (1-5):**
1. Minor (negligible consequences)
2. Significant (limited consequences)
3. Serious (substantial consequences)
4. Critical (disastrous consequences)
5. Catastrophic (sector or regulatory consequences beyond the organization)

**Risk levels (composite lookup):**
- Very Low (1)
- Low (2)
- Medium (3)
- High (4)
- Very High (5)

**Treatment options:** Mitigate, Accept, Transfer, Avoid

---

## Risk Register Summary

| ID | Risk | Inherent | Current | Residual | Treatment | Owner |
|---|---|---|---|---|---|---|
| R-01 | Privileged Account Compromise | Very High (5) | Medium (3) | **Medium (3)** | Mitigate | CISO |
| R-02 | Payment Data Exfiltration via API | Very High (5) | Medium (3) | **Medium (3)** | Mitigate | CISO + CTO |
| R-03 | Ransomware on Production DB | High (4) | Medium (3) | **Medium (3)** | Mitigate | CTO + CISO |
| R-04 | Third-Party SaaS Breach | High (4) | High (4) | **High (4)** | Accept (with mitigation) | CISO + Vendor Mgmt |
| R-05 | Insider Threat (Malicious Employee) | High (4) | High (4) | **Medium (3)** | Mitigate | Head of People + CISO |
| R-06 | Insufficient Audit Logging | High (4) | Low (2) | **Low (2)** | Mitigate | CISO + Engineering |

**Distribution:**
- Inherent: 2 Very High, 4 High, 0 Medium, 0 Low, 0 Very Low
- Current: 0 Very High, 2 High, 3 Medium, 1 Low, 0 Very Low
- Residual: 0 Very High, 1 High, 3 Medium, 2 Low, 0 Very Low

---

## Detailed Risk Scenarios

### R-01: Privileged Account Compromise

**Description:** A privileged account (administrator, root, or service account with elevated permissions) is compromised through phishing, credential stuffing, or insider action. The attacker gains access to production systems, customer data, or financial controls.

**Inherent risk:** Probability 4 (Very likely) × Impact 5 (Catastrophic) = Very High (5)

**Existing controls:**
- V-03 (Identity Provider) enforces SSO + MFA for all production access
- ACC-01 (Access Control & Privileged Access Policy) requires quarterly access reviews
- PAM session recording for production database and payment systems
- Separation of duties between developer, DBA, and security roles

**Current risk:** Probability 2 (Rather unlikely) × Impact 5 (Catastrophic) = Medium (3)

**Residual risk:** Probability 2 (Rather unlikely) × Impact 5 (Catastrophic) = **Medium (3)**

**Treatment:** Mitigate
- Continued quarterly access reviews
- PAM session recording for all privileged access
- Phishing simulation program for all privileged users (Q3 2026 target)

**Owner:** CISO
**Review cadence:** Quarterly

---

### R-02: Payment Data Exfiltration via API

**Description:** Payment data (card numbers, transaction history, customer PII) is exfiltrated from AtlasPay's APIs through API key compromise, man-in-the-middle attack, or insider abuse.

**Inherent risk:** Probability 4 (Very likely) × Impact 5 (Catastrophic) = Very High (5)

**Existing controls:**
- V-02 (Payment Gateway) provides tokenization  -  no raw card data stored
- API gateway with mTLS for all internal service-to-service communication
- WAF with rate limiting and behavioral analysis
- DLP on egress traffic
- Quarterly penetration testing by external firm

**Current risk:** Probability 2 (Rather unlikely) × Impact 5 (Catastrophic) = Medium (3)

**Residual risk:** Probability 2 (Rather unlikely) × Impact 5 (Catastrophic) = **Medium (3)**

**Treatment:** Mitigate
- Continued penetration testing (quarterly)
- API key rotation cadence (90 days)
- Behavioral analytics on API traffic via V-05 (Monitoring Tools)

**Rationale for unchanged residual:** Controls are operating as designed. Additional residual reduction would require architectural changes (e.g., moving to zero-trust network segmentation) that exceed engagement scope.

**Owner:** CISO + CTO
**Review cadence:** Quarterly

---

### R-03: Ransomware on Production Database Host

**Description:** Ransomware encrypts AtlasPay's production database host, rendering the system unavailable and potentially exfiltrating customer data before encryption.

**Inherent risk:** Probability 3 (Likely) × Impact 5 (Catastrophic) = High (4)

**Existing controls:**
- Immutable backup snapshots stored in isolated V-01 (AWS) account
- EDR (Endpoint Detection and Response) deployed on all production hosts
- Tested restore procedure (quarterly restore-from-backup drill)
- Network segmentation between production and corporate networks
- Principle of least privilege enforced via RBAC

**Current risk:** Probability 3 (Likely) × Impact 3 (Serious) = Medium (3)

**Residual risk:** Probability 3 (Likely) × Impact 3 (Serious) = **Medium (3)**

**Treatment:** Mitigate
- Continue quarterly restore-from-backup tests
- Annual tabletop exercise simulating ransomware scenario
- Continue EDR deployment and tuning

**Owner:** CTO + CISO
**Review cadence:** Quarterly

---

### R-04: Third-Party SaaS Breach (Vendor Compromise)

**Description:** A SaaS vendor in AtlasPay's supply chain (e.g., V-02 Payment Gateway, V-03 Identity Provider) is compromised, exposing AtlasPay customer data or disrupting operations.

**Inherent risk:** Probability 4 (Very likely) × Impact 4 (Critical) = High (4)

**Existing controls:**
- TPRM-01 (Third-Party Risk Management Policy) with vendor tier classification
- 7 vendors under MSA with security addenda
- Annual SOC 2 Type 2 review for Tier-1 vendors
- Contractual breach notification SLAs (72 hours)
- Vendor access segmentation via V-04 (Application Platform) service mesh

**Current risk:** Probability 3 (Likely) × Impact 4 (Critical) = High (4)

**Residual risk:** Probability 3 (Likely) × Impact 4 (Critical) = **High (4)**

**Treatment:** Accept (with mitigation)
- Accept residual high because supply-chain compromise is endemic in FinTech
- Mitigate through blast radius reduction: vendor access segmentation, contractual recovery rights, sub-processor notification clauses
- Quarterly vendor risk review with focus on Tier-1 vendors (V-01, V-02, V-03)

**Rationale for unchanged residual:** AtlasPay cannot prevent vendor-side security incidents. Industry incidents (SolarWinds, Okta, MOVEit, Log4j) demonstrate that even mature vendor risk programs cannot eliminate supply-chain compromise probability. Controls reduce blast radius and contractual recovery options, not occurrence.

**Owner:** CISO + Vendor Management Officer
**Review cadence:** Quarterly

---

### R-05: Insider Threat (Malicious Employee)

**Description:** A current or former AtlasPay employee abuses authorized access for malicious purposes (data theft, fraud, sabotage).

**Inherent risk:** Probability 4 (Very likely) × Impact 4 (Critical) = High (4)

**Existing controls:**
- Pre-employment background checks (policy drafted, vendor selection in progress)
- Principle of least privilege enforced via RBAC
- Separation of duties on financial transactions
- Immutable audit logging forwarded to SIEM with 90-day hot retention
- Documented offboarding procedure within 4 hours of termination
- Annual security awareness training

**Current risk:** Probability 3 (Likely) × Impact 4 (Critical) = High (4)

**Residual risk:** Probability 2 (Rather unlikely) × Impact 4 (Critical) = **Medium (3)**

**Treatment:** Mitigate
- Complete background check vendor onboarding (Q3 2026 target  -  see HF-02 in gap assessment)
- Continue quarterly access reviews
- Continue audit log retention and monitoring via V-05

**Rationale for one-level drop:** Mature access controls (RBAC, SoD) combined with continuous monitoring (SIEM) and fast offboarding reduce insider threat probability from "likely" to "rather unlikely." Impact stays critical because insider access by definition has privileged position.

**Owner:** Head of People + CISO
**Review cadence:** Quarterly

---

### R-06: Insufficient Audit Logging

**Description:** AtlasPay fails to capture, retain, or monitor security-relevant events, resulting in undetected incidents or inability to support forensic investigation.

**Inherent risk:** Probability 5 (Almost certain) × Impact 2 (Significant) = High (4)

**Existing controls:**
- Centralized SIEM (V-05) with 90-day hot retention
- 6-year cold archive per FFIEC IT Examination Handbook retention pattern
- Authentication, authorization, and data access events captured
- SIEM alerting rules with on-call rotation
- Immutable log forwarding (write-only Datadog integration)

**Current risk:** Probability 2 (Rather unlikely) × Impact 2 (Significant) = Low (2)

**Residual risk:** Probability 2 (Rather unlikely) × Impact 2 (Significant) = **Low (2)**

**Treatment:** Mitigate
- Continue SIEM deployment and tuning
- Quarterly review of alerting rules
- Annual audit log retention verification

**Owner:** CISO + Engineering
**Review cadence:** Quarterly

---

## Risk Acceptance Statement

**R-04 (Third-Party SaaS Breach) residual risk is formally accepted by AtlasPay executive leadership** with the following conditions:
1. Quarterly vendor risk review with documented minutes
2. Annual SOC 2 Type 2 review for all Tier-1 vendors
3. Contractual sub-processor notification rights enforced
4. Annual tabletop exercise simulating vendor breach scenario
5. Cyber insurance policy maintained with vendor breach coverage

If any of these conditions cannot be maintained, R-04 should be re-evaluated for treatment change (likely transfer via cyber insurance or escalate to board for risk avoidance discussion).

---

**Last Updated:** 2026-06-25 01:10 EDT
**Engagement:** Phase 1A  -  Risk Register Finalization
**Engagement Status:** Ready for Phase 1B (SOC 2 Control Mapping)

**[LAB-SYNTHETIC] Disclosure:** Risk register values reflect consultant judgment for a portfolio demonstration engagement. Real engagement residual values would be derived from AtlasPay's actual control environment and validated through control testing. The risk acceptance narrative for R-04 is illustrative.