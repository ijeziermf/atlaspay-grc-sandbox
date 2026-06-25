# AtlasPay GRC Sandbox — Eramba Export Summary

**Exported:** 2026-06-22T22:45:10.489282
**Source:** Eramba CE 3.30.0 (https://localhost:8443)

## Record Counts

| Section | Count |
|---|---|
| Risk Classification Types | 2 |
| Risk Classifications | 10 |
| Risks | 6 |
| Security Policies | 4 |
| Business Continuity Plans | 4 |
| Third Parties | 7 |
| Security Incidents | 1 |
| **Total** | **34** |

## Risk Classification Types

- **Impact**
- **Likelihood**

## Risk Classifications

| Type | Name | Value |
|---|---|---|
| Impact | Critical | 20 |
| Impact | High | 12 |
| Impact | Medium | 8 |
| Impact | Low | 4 |
| Impact | Very Low | 2 |
| Likelihood | Almost Certain | 5 |
| Likelihood | Likely | 4 |
| Likelihood | Possible | 3 |
| Likelihood | Unlikely | 2 |
| Likelihood | Rare | 1 |

## Asset Risks

| ID | Title | Residual | Threats | Vulnerabilities |
|---|---|---|---|---|
| 1 | [R-01] Phishing Attacks | 20.0 | Phishing campaigns, credential stuffing, social engineering | Lack of MFA, untrained staff, email gateway gaps |
| 2 | [R-02] Access Control Weakness | 12.0 | Phishing campaigns, credential stuffing, social engineering | Lack of MFA, untrained staff, email gateway gaps |
| 3 | [R-03] Logging and Monitoring Gaps | 9.0 | Phishing campaigns, credential stuffing, social engineering | Lack of MFA, untrained staff, email gateway gaps |
| 4 | [R-04] Incident Response Planning and Testing | 12.0 | Phishing campaigns, credential stuffing, social engineering | Lack of MFA, untrained staff, email gateway gaps |
| 5 | [R-05] Third-Party and Vendor Risk Management | 12.0 | Phishing campaigns, credential stuffing, social engineering | Lack of MFA, untrained staff, email gateway gaps |
| 6 | [R-06] Security Awareness and Training | 10.0 | Phishing campaigns, credential stuffing, social engineering | Lack of MFA, untrained staff, email gateway gaps |

## Security Policies

| ID | Name | Version | Published | Next Review |
|---|---|---|---|---|
| 1 | Access Control & Privileged Access Policy | 1.0 | 2026-05-23 | 2026-09-20 |
| 2 | Incident Response Policy | 1.0 | 2026-05-23 | 2026-09-20 |
| 3 | Security Awareness & Acceptable Use Policy | 1.0 | 2026-05-23 | 2026-09-20 |
| 4 | Third-Party Risk Management Policy | 1.0 | 2026-05-23 | 2026-09-20 |

## Business Continuity Plans

| ID | Title | Objective | Audit Metric (RTO/RPO) |
|---|---|---|---|
| 1 | Payment Processing BCP | Restore payment processing capability within 4 hours of disr | RTO: 4 hours, RPO: Near-real-time, MTPD: 24 hours |
| 2 | Customer Account Access BCP | Restore customer account access within 8 hours of disruption | RTO: 8 hours, RPO: 24 hours, MTPD: 48 hours |
| 3 | Fraud Monitoring BCP | Restore fraud monitoring within 4 hours of disruption. | RTO: 4 hours, RPO: Near-real-time, MTPD: 24 hours |
| 4 | Financial Reporting BCP | Restore financial reporting capability within 24 hours of di | RTO: 24 hours, RPO: 24 hours, MTPD: 72 hours |

## Third Parties (Vendors)

| ID | Name | Description |
|---|---|---|
| 1 | Cloud Provider (Sandbox) | Primary cloud infrastructure provider for the AtlasPay sandbox. |
| 2 | Payment Gateway (Sandbox) | Payment processing gateway integration. |
| 3 | Identity Provider (Sandbox) | SSO and identity federation for the AtlasPay application. |
| 4 | Application Platform (Sandbox) | Application runtime platform (PaaS). |
| 5 | Monitoring Tools (Sandbox) | Infrastructure and application monitoring SaaS. |
| 6 | Finance Systems (Sandbox) | Finance and accounting system of record. |
| 7 | Data Warehouse (Sandbox) | Analytics data warehouse for reporting. |

## Security Incidents

| ID | Title | Open Date | Closure |
|---|---|---|---|
| 1 | Sample Phishing Incident - Finance Department | 2026-06-22 | NULL |

---

## Notes for CISO Assistant Import

- All Eramba IDs preserved as `_eramba_id` for traceability
- Eramba-specific columns (workflow_status, workflow_owner_id) prefixed with `_` and not used in import
- RTO/RPO is in `audit_metric` field as text (Eramba doesn't have a separate field)
- `description` field on policies/risks/BCPs is the human-readable content
- `threats` and `vulnerabilities` on risks are the source-context text from the AtlasPay PDF

When importing to CISO Assistant, the natural mapping is:

| Eramba | CISO Assistant |
|---|---|
| risk_classification_types | Risk Matrix (custom or built-in) |
| risk_classifications | Risk Matrix values |
| risks | Risk Assessment scenarios |
| security_policies | Policies (under Governance) |
| business_continuity_plans | Business Continuity scenarios + BIA |
| third_parties | Third Parties (Entities) |
| security_incidents | Incidents |
