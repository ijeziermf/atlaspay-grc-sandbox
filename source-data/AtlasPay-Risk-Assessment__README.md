# AtlasPay Risk Assessment, NIST SP 800-53 Rev. 5

> **End-to-end risk assessment for a simulated FinTech payment processor, quantitative scoring, executive-ready heat maps, and audit-defensible treatment plans.**

---

## What This Demonstrates

| Capability | Details |
|---|---|
| **Framework Alignment** | NIST SP 800-53 Rev. 5, NIST Cybersecurity Framework (CSF) |
| **Risk Methodology** | Quantitative scoring (Impact × Likelihood), 5×5 risk matrix |
| **Deliverables** | Risk register, heat map, treatment plan, executive summary |
| **Stakeholder Focus** | Executive decision-making, audit readiness, governance |
| **Industry Relevance** | FinTech, payment processing, SOC 2 readiness |

---

## Overview

This project documents a complete risk assessment performed for **AtlasPay**, a simulated FinTech payment processing organization. The goal was to evaluate information security and operational risks in a way that supports **executive decision-making**, **audit readiness**, and **long-term risk governance**, not just technical control checklists.

The assessment identifies risks, quantifies exposure, prioritizes treatment, and produces governance artifacts that mirror real-world GRC consulting deliverables.

---

## Deliverables

| Artifact | Purpose | Audience |
|---|---|---|
| **Risk Assessment Worksheet** | Structured risk identification and scoring | Security team, auditors |
| **Quantitative Risk Register** | Inherent and residual risk tracking with ownership | Risk owners, leadership |
| **Heat Map Visualization** | Executive-ready priority visualization | C-suite, board |
| **Risk Treatment Plan** | Mitigation actions with timelines and owners | Operations, security |
| **Executive Summary** | Business impact and decision support | Leadership, stakeholders |

---

## Key Features

- ✅ **Plain English Risk Descriptions**, Accessible to non-technical stakeholders
- ✅ **Quantitative Scoring Model**, Impact × Likelihood for consistent prioritization
- ✅ **NIST Control Mapping**, Audit-defensible framework alignment
- ✅ **Residual Risk Tracking**, Post-treatment exposure visibility
- ✅ **Executive Heat Map**, Visual priority communication
- ✅ **Ownership & Timelines**, Accountability built into treatment plan

---

## Process (Start to Finish)

```
1. Define Scope & Objectives
   └─→ SOC 2 readiness alignment
   └─→ Executive decision support

2. Risk Identification
   └─→ Threat-vulnerability-impact model
   └─→ Plain business language documentation

3. Framework Mapping
   └─→ NIST SP 800-53 Rev. 5 control families
   └─→ NIST CSF function alignment

4. Quantitative Scoring
   └─→ 5×5 impact/likelihood matrix
   └─→ Inherent risk calculation

5. Treatment Planning
   └─→ Mitigation strategies
   └─→ Residual risk projection
   └─→ Ownership and timelines

6. Executive Reporting
   └─→ Heat map visualization
   └─→ Business impact narrative
```

---

## Risk Scoring Model

| Score | Impact | Likelihood |
|---|---|---|
| **5** | Catastrophic (business failure) | Almost Certain (>90%) |
| **4** | Major (significant financial/reputational) | Likely (>70%) |
| **3** | Moderate (operational disruption) | Possible (30-70%) |
| **2** | Minor (limited impact) | Unlikely (10-30%) |
| **1** | Negligible (minimal impact) | Rare (<10%) |

**Risk Level = Impact × Likelihood**

| Score Range | Risk Level | Treatment Priority |
|---|---|---|
| 20-25 | Critical | Immediate action required |
| 15-19 | High | Priority treatment within 30 days |
| 10-14 | Medium | Scheduled treatment within 90 days |
| 5-9 | Low | Accept or monitor |
| 1-4 | Very Low | Accept |

---

## Sample Risk Register Entry

| Field | Example |
|---|---|
| **Risk ID** | RISK-001 |
| **Risk Description** | Unauthorized access to cardholder data via compromised admin credentials |
| **Affected Assets** | Payment processing database, admin accounts |
| **Business Impact** | PCI-DSS violation, customer data exposure, reputational damage |
| **Inherent Risk** | 20 (Critical), Impact 5 × Likelihood 4 |
| **Existing Controls** | MFA, role-based access, logging |
| **Control Gaps** | No privileged access monitoring, no session recording |
| **Treatment** | Implement PAM solution, enable session recording, quarterly access reviews |
| **Residual Risk** | 8 (Low), Impact 4 × Likelihood 2 |
| **Owner** | CISO |
| **Target Date** | Q3 2026 |

---

## Why the Heat Map Matters

The heat map translates complex risk data into a **single, intuitive visual** that highlights priority areas at a glance. When paired with residual risk projections, it becomes a **decision-making tool** rather than a static graphic.

**Use Cases:**
- Board presentations (priority justification)
- Budget requests (resource allocation)
- Audit discussions (treatment progress)
- Vendor risk conversations (third-party exposure)

---

## Value to GRC Consulting

This project demonstrates **client-ready deliverables** for:

| Service | Application |
|---|---|
| **Risk Assessments** | Full methodology, scoring, register, treatment |
| **Audit Readiness** | NIST mapping, control documentation, evidence tracking |
| **Executive Advisory** | Heat maps, business impact narratives, decision support |
| **Policy Development** | Risk-based policy requirements, governance structure |

---

## Tools & Frameworks

| Tool/Framework | Use |
|---|---|
| **Microsoft Excel** | Risk register, scoring model, heat map |
| **NIST SP 800-53 Rev. 5** | Control family alignment |
| **NIST CSF** | Function mapping (Identify, Protect, Detect, Respond, Recover) |
| **Quantitative Scoring** | Impact × Likelihood model |

---

## Key Takeaways

1. **Clear Language Drives Ownership**, Executives act on risks they understand
2. **Quantitative Scoring Improves Prioritization**, Consistent ranking beats gut feel
3. **Heat Maps Need Narrative Context**, Visuals + story = decision support
4. **Risk Management = Governance + Communication**, Not just controls

---

## Growth & Next Iterations

Future enhancements:
- Integration with GRC platforms (ServiceNow GRC, Archer)
- Automated evidence tracking
- Continuous risk monitoring dashboards
- Third-party risk assessment extension

---

## Video Walkthrough

*Embedded walkthrough video coming soon*

---

## License

This project is for educational and portfolio demonstration purposes. Organizations may adapt the methodology for internal use.
