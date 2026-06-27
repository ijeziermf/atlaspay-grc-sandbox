# Scenario-Based Cyber Risk Analyses

> **Privileged Account Abuse & Third-Party Vendor Breach, NIST-aligned threat pathways, quantitative scoring, executive decision support.**

---

## What This Demonstrates

| Capability | Details |
|---|---|
| **Framework Alignment** | NIST SP 800-53 Rev. 5, 5×5 Risk Matrix |
| **Methodology** | Scenario-based threat pathways, quantitative risk scoring |
| **Deliverables** | Risk analysis reports, executive summaries, treatment recommendations |
| **Stakeholder Focus** | Executive decision-making, governance, risk prioritization |
| **Industry Relevance** | All industries, internal threats and third-party risk |

---

## Overview

This project contains two **scenario-based cyber risk analyses** designed to evaluate how realistic security incidents can escalate into **material business risk**. The scenarios, **Privileged Account Abuse** (internal threat) and **Third-Party Vendor Breach** (external threat), demonstrate how threats originating inside or outside the organization can lead to:

- Data exposure
- Operational disruption
- Regulatory scrutiny
- Reputational harm

Rather than focusing solely on control gaps, each analysis traces a **full threat pathway** from initial compromise to organizational impact, supporting informed executive decision-making and risk prioritization.

---

## Deliverables

| Artifact | Purpose | Audience |
|---|---|---|
| **Risk Analysis Report** | Narrative-driven scenario with threat pathway | Security team, leadership |
| **Quantitative Risk Scoring** | Impact × Likelihood using 5×5 matrix | Risk owners |
| **Business Impact Analysis** | Affected assets, data types, business functions | Executive stakeholders |
| **Treatment Options** | Mitigation strategies with cost/benefit | Decision-makers |
| **Executive Summary** | Governance-ready briefing language | C-suite, board |

---

## Key Features

- - **Narrative-Driven Scenarios**, Realistic, relatable threat stories
- - **Threat Pathway Mapping**, From initial compromise to business impact
- - **Quantitative Inherent Risk**, 5×5 matrix scoring (Impact × Likelihood)
- - **Business-Focused Language**, Accessible to non-technical executives
- - **Treatment Recommendations**, Clear decision support, not just findings
- - **NIST-Aligned Structure**, Audit-defensible methodology

---

## Scenario 1: Privileged Account Abuse

| Aspect | Details |
|---|---|
| **Threat Origin** | Internal (malicious insider or compromised admin) |
| **Initial Access** | Legitimate privileged credentials |
| **Threat Pathway** | Credential misuse → data exfiltration → business impact |
| **Affected Assets** | Customer databases, financial records, admin systems |
| **Business Impact** | Regulatory fines, customer lawsuits, reputational damage |
| **Inherent Risk Score** | 20 (Critical), Impact 5 × Likelihood 4 |
| **Treatment Priority** | Immediate, PAM implementation, session monitoring |

### Threat Pathway Diagram

```
Privileged Account Compromise
         │
         ▼
  Lateral Movement
         │
         ▼
  Data Access (Customer PII)
         │
         ▼
  Exfiltration
         │
         ▼
  Business Impact
  (Regulatory + Reputational)
```

---

## Scenario 2: Third-Party Vendor Breach

| Aspect | Details |
|---|---|
| **Threat Origin** | External (vendor security failure) |
| **Initial Access** | Vendor system compromise |
| **Threat Pathway** | Vendor breach → shared data exposure → downstream impact |
| **Affected Assets** | Shared customer data, integration APIs, contracts |
| **Business Impact** | Contractual liability, customer notification costs, trust loss |
| **Inherent Risk Score** | 16 (High), Impact 4 × Likelihood 4 |
| **Treatment Priority** | High, Vendor risk assessments, contract clauses |

### Threat Pathway Diagram

```
Vendor System Breach
         │
         ▼
  Access to Shared Data
         │
         ▼
  Data Exposure
         │
         ▼
  Downstream Impact
  (Liability + Notification)
```

---

## Risk Scoring Methodology

| Score | Impact | Likelihood |
|---|---|---|
| **5** | Catastrophic (business failure) | Almost Certain (>90%) |
| **4** | Major (significant financial/reputational) | Likely (>70%) |
| **3** | Moderate (operational disruption) | Possible (30-70%) |
| **2** | Minor (limited impact) | Unlikely (10-30%) |
| **1** | Negligible (minimal impact) | Rare (<10%) |

**Inherent Risk = Impact × Likelihood**

| Score Range | Risk Level | Treatment Priority |
|---|---|---|
| 20-25 | Critical | Immediate action required |
| 15-19 | High | Priority treatment within 30 days |
| 10-14 | Medium | Scheduled treatment within 90 days |
| 5-9 | Low | Accept or monitor |
| 1-4 | Very Low | Accept |

---

## Why Scenario-Based Analysis Matters

Scenario-based cyber risk analysis **bridges the gap** between technical security failures and real business impact. By tracing how an incident could realistically unfold, whether through insider misuse or vendor compromise, this method helps leadership understand:

- **Why the risk matters** (not just that it exists)
- **Where resources should be focused** (priority allocation)
- **What decisions need to be made** (treatment options)

This provides a level of **clarity** that abstract ratings or control checklists cannot.

---

## Value to GRC Consulting

This project demonstrates **client-ready deliverables** for:

| Service | Application |
|---|---|
| **Cyber Risk Assessments** | Scenario-based methodology, threat pathways |
| **Executive Advisory** | Business impact narratives, decision support |
| **Third-Party Risk** | Vendor breach scenarios, contract requirements |
| **Insider Threat** | Privileged abuse scenarios, PAM justification |

---

## Tools & Frameworks

| Tool/Framework | Use |
|---|---|
| **Microsoft Word** | Formal risk analysis report |
| **NIST SP 800-53** | Control family alignment |
| **5×5 Risk Matrix** | Impact and likelihood scoring |
| **Quantitative Scoring** | Impact × Likelihood model |

---

## Key Takeaways

1. **Internal and External Threats Both Matter**, Privileged access and vendor relationships are high-risk
2. **Scenario-Based > Control-Only**, Realistic pathways beat abstract checklists
3. **Quantitative Scoring Strengthens Prioritization**, Consistent ranking enables resource allocation
4. **Cyber Risk = Decision Support**, Not just technical findings, but governance input

---

## Growth & Next Iterations

Future enhancements:
- Comparative scoring across multiple scenarios or vendors
- Integration with formal risk registers or GRC platforms
- Expanded modeling of privilege escalation pathways
- Vendor tiering and continuous monitoring frameworks

---

## Video Walkthrough

https://github.com/user-attachments/assets/6a4be3a9-3bb1-4597-ac70-4231d840346e

---

## License

This project is for educational and portfolio demonstration purposes. Organizations may adapt the methodology for internal use.
