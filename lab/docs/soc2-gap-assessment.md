# SOC 2 Type 1 Readiness — Gap Assessment

**Engagement:** AtlasPay FinTech SOC 2 Type 1 Readiness
**Assessment Date:** 2026-06-25
**Audit Window Target:** Q3 2026
**Scope:** Common Criteria (CC) + Availability (A) + Confidentiality (C)
**Source:** `lab/docs/soc2-control-mapping.md`

## Severity Rating Scale

| Severity | Definition | Example |
|---|---|---|
| **🔴 Critical** | Will result in audit qualification if not remediated before audit window | No risk assessment exists; no logical access controls |
| **🟠 High** | Material gap requiring remediation; auditor will likely raise a finding | Background checks not implemented; no documented change management |
| **🟡 Medium** | Design exists, evidence incomplete; auditor may request additional evidence | Policy attestation not enforced; recovery test cadence informal |
| **🟢 Low** | Minor documentation gap; auditor likely accepts verbal explanation | Org chart slightly outdated; communication logs incomplete |

## Remediation Time Estimates

| Estimate | Meaning |
|---|---|
| **Quick Win** | 1-2 weeks, internal resources only |
| **Short Term** | 1-2 months, internal + vendor coordination |
| **Medium Term** | 2-3 months, may require budget approval |
| **Long Term** | 3-6 months, may require architectural change |

---

## Critical Findings (🔴)

*No critical findings identified.* AtlasPay's existing controls cover the SOC 2 Type 1 baseline. The gaps are documentation and evidence-completeness issues, not missing controls.

---

## High Findings (🟠)

### HF-01: Change Management Control (CC8.1)

**Current state:** V-04 (Application Platform) GitOps workflow exists but is not formally documented as a control. Production deployments follow PR review + CI/CD pipeline pattern, but no formal Change Advisory Board (CAB) documentation, no change request tickets, no rollback procedures on file.

**Evidence gap:** No documented CAB charter, no change request templates, no production deployment log retention policy.

**Risk if not remediated:** Auditor will issue a finding that change management is informal; may impact Type 1 opinion.

**Remediation:**
1. Document the V-04 GitOps workflow as a formal Change Management Policy (2 weeks)
2. Establish CAB meeting cadence (weekly for production, ad-hoc for emergencies)
3. Configure V-05 (Monitoring Tools) to retain deployment logs for 12 months
4. Train engineering team on change request submission process

**Estimated effort:** Quick Win (1-2 weeks, internal engineering + CISO)
**Owner:** CTO + CISO
**Target completion:** 2026-07-15

### HF-02: Pre-Employment Background Check Program (CC1.4)

**Current state:** Background check policy is drafted but not operational. No vendor selected, no HR system integration, no onboarding workflow enforces background checks.

**Evidence gap:** No vendor contract, no executed background check reports in personnel files.

**Risk if not remediated:** Auditor will issue a finding on CC1.4; high-impact control for FinTech because insider threat is a named risk scenario (R-05).

**Remediation:**
1. Select background check vendor (Checkr, Sterling, or equivalent) — 1 week
2. Sign MSA with vendor; integrate with HRIS (Gusto, Rippling, etc.) — 2 weeks
3. Update employee onboarding checklist to enforce background check completion
4. Define background check scope: identity, criminal, credit (for finance roles), employment history

**Estimated effort:** Short Term (1-2 months)
**Owner:** Head of People + CISO
**Target completion:** 2026-08-15

### HF-03: Vulnerability Management Program (CC7.1)

**Current state:** Vulnerability scanning is ad-hoc. V-05 (Monitoring Tools) has scanning capability but no formal vulnerability management policy, no scan cadence, no remediation SLA, no CVE tracking.

**Evidence gap:** No scan reports retained, no remediation tickets, no CVE prioritization framework.

**Risk if not remediated:** Auditor will issue a finding on CC7.1; SOC 2 Type 1 auditors expect documented vuln management even if minimal.

**Remediation:**
1. Configure V-05 for weekly authenticated vulnerability scans (1 week)
2. Define remediation SLA: Critical CVEs = 7 days, High = 30 days, Medium = 90 days
3. Establish weekly vulnerability review meeting (CISO + Engineering Lead)
4. Retain scan reports for 12 months in V-05 with monthly summary report to leadership
5. Subscribe to CVE feeds for V-01 (AWS), V-02 (Payment Gateway), V-04 (K8s) dependencies

**Estimated effort:** Short Term (1-2 months)
**Owner:** CISO + Engineering Lead
**Target completion:** 2026-08-30

---

## Medium Findings (🟡)

### MF-01: Policy Attestation Cadence (CC1.1, CC1.5)

**Current state:** 4 policies exist (ACC-01, IR-01, SA-01, TPRM-01). Policy attestation (employee sign-off that they have read and understood the policy) is not enforced.

**Evidence gap:** No annual attestation records, no HRIS integration.

**Remediation:**
1. Configure V-03 (Identity Provider) to require policy acceptance at first login after policy publication
2. Annual re-attestation reminder via email + calendar
3. HR system integration for completion tracking

**Estimated effort:** Short Term (1-2 months)
**Owner:** CISO + Head of People

### MF-02: Incident Response Tabletop Exercise (CC7.4, CC7.5)

**Current state:** IR-01 (Incident Response Policy) is documented. No tabletop exercise has been conducted in the past 12 months.

**Evidence gap:** No tabletop exercise reports, no lessons-learned documentation.

**Remediation:**
1. Schedule annual tabletop exercise (Q4 2026)
2. Scenarios: ransomware on production DB (R-03), payment data breach (R-02), vendor breach notification (R-04)
3. Engage external facilitator for first exercise
4. Document lessons learned; update IR-01

**Estimated effort:** Medium Term (2-3 months including exercise execution)
**Owner:** CISO + Engineering Lead

### MF-03: Vendor Risk Tier Re-Classification (CC9.2)

**Current state:** All 7 vendors have MSAs. Tier classification exists but is not formally documented per vendor.

**Evidence gap:** No vendor risk tier memo, no formal tier criteria documented in TPRM-01.

**Remediation:**
1. Document tier classification criteria in TPRM-01 (Tier 1 = customer data access, Tier 2 = business operations, Tier 3 = non-critical)
2. Re-classify V-01 through V-07 against documented criteria
3. Annual tier review cadence

**Estimated effort:** Quick Win (1-2 weeks)
**Owner:** CISO + Vendor Management Officer

### MF-04: Capacity Planning Documentation (A1.1)

**Current state:** V-01 (AWS) auto-scaling is operational. Capacity planning process is informal.

**Evidence gap:** No documented capacity review process, no quarterly capacity reports.

**Remediation:**
1. Document capacity review process (monthly)
2. Generate capacity reports from V-01 CloudWatch + V-05 dashboards
3. Quarterly capacity planning review with Engineering + Finance

**Estimated effort:** Quick Win (1-2 weeks)
**Owner:** Engineering Lead + CTO

### MF-05: Recovery Testing Cadence (A1.3)

**Current state:** Backup procedures documented in IR-01. Recovery testing is ad-hoc.

**Evidence gap:** No recovery test reports, no documented RTO/RPO targets.

**Remediation:**
1. Document RTO/RPO targets per system (4h RTO for production DB, 1h for wires, 8h for digital channels)
2. Quarterly restore-from-backup tests with documented reports
3. Annual full DR tabletop with executive participation

**Estimated effort:** Short Term (1-2 months for initial documentation)
**Owner:** Engineering Lead + CISO

### MF-06: Data Disposal Procedure (C1.2)

**Current state:** AWS data lifecycle policies are configured. Data disposal procedure is not formally documented.

**Evidence gap:** No data disposal policy, no records of disposal actions.

**Remediation:**
1. Document data disposal procedure in TPRM-01 or new Records Retention Policy
2. Quarterly disposal review for retired customer data
3. Vendor (V-01) attestation of secure deletion

**Estimated effort:** Quick Win (1-2 weeks)
**Owner:** CISO + Legal

---

## Low Findings (🟢)

### LF-01: Org Chart Documentation (CC1.3)

**Current state:** Org chart exists but is 6 months out of date.

**Remediation:** Update org chart, establish quarterly org chart review.

**Estimated effort:** Quick Win (1 week)
**Owner:** Head of People

### LF-02: External Communication Documentation (CC2.3)

**Current state:** Customer-facing security page exists but is not version-controlled.

**Remediation:** Move security page to V-04 (Application Platform) git repo with change history.

**Estimated effort:** Quick Win (1 week)
**Owner:** Marketing + CISO

### LF-03: Records Retention Policy (CC3.5, C1.1)

**Current state:** Retention is informal; AWS lifecycle policies exist but no master retention schedule.

**Remediation:** Document master Records Retention Policy covering customer data, employee data, audit logs, financial records.

**Estimated effort:** Quick Win (2 weeks)
**Owner:** Legal + CISO

### LF-04: Board Reporting Template (CC1.2, CC2.1)

**Current state:** Risk Committee charter exists but no standard board reporting template.

**Remediation:** Develop quarterly board security reporting template with KPI dashboard.

**Estimated effort:** Quick Win (1 week)
**Owner:** CISO

---

## Remediation Roadmap Summary

| Severity | Count | Quick Win | Short Term | Medium Term |
|---|---|---|---|---|
| 🔴 Critical | 0 | 0 | 0 | 0 |
| 🟠 High | 3 | 1 | 2 | 0 |
| 🟡 Medium | 6 | 3 | 2 | 1 |
| 🟢 Low | 4 | 4 | 0 | 0 |
| **Total** | **13** | **8** | **4** | **1** |

**Realistic SOC 2 Type 1 audit readiness date:** 2026-09-15 (assuming all High findings remediated by 2026-08-30)

**Audit window recommendation:** Q4 2026 (October-December) to allow 4-6 weeks buffer between remediation completion and audit kickoff.

---

## Risk Treatment Recommendations

For each High finding, recommend the following risk treatment in the engagement risk register:

| Finding | Treatment | Owner | Target |
|---|---|---|---|
| HF-01 (CC8.1) | Mitigate — document existing GitOps workflow | CTO + CISO | 2026-07-15 |
| HF-02 (CC1.4) | Mitigate — vendor selection + HRIS integration | Head of People + CISO | 2026-08-15 |
| HF-03 (CC7.1) | Mitigate — formalize vuln mgmt program | CISO + Engineering Lead | 2026-08-30 |

For Medium and Low findings, treatment plans should be added to the risk register as separate risks with their own treatment plans.

---

## [LAB-SYNTHETIC] Disclosure

This gap assessment is based on a synthesized engagement state. In a real SOC 2 Type 1 readiness engagement, the findings would be derived from:
- Interviews with the AtlasPay CISO, CTO, Engineering Lead, Head of People
- Review of existing policies, MSAs, vendor documentation
- Inspection of V-01 through V-07 configurations and access controls
- Sample testing of controls (e.g., provisioning tickets, access reviews)

The recommendations above are realistic for an early-stage FinTech but have not been validated against actual AtlasPay operations. The remediation roadmap is the consultant's deliverable to the client for prioritization.

---

**Last Updated:** 2026-06-25 01:20 EDT
**Engagement:** Phase 1C — Gap Assessment
**Engagement Status:** Ready for Phase 3 (Audit Walkthrough Simulation)