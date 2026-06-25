# AtlasPay Sandbox — Eramba CE Enterprise Gate Limitations

**Date captured:** 22 June 2026
**Eramba version:** Community v3.30.0
**Source:** Direct DOM inspection of the Eramba CE sidebar (Playwright)

## Why this doc exists

Eramba Community Edition ships with the **full UI shell** but gates three modules
behind a license check that points to Eramba's upgrade page. This file documents
which modules are blocked, what they would do in Enterprise, and the workaround
pattern we use instead for the AtlasPay sandbox.

## The three gated modules

| Module | Sidebar label (visible) | What it does in Enterprise | Our workaround |
|---|---|---|---|
| **Online Assessments** | "Online Assessments `Enterprise`" (links to eramba.org/eramba-software) | Send questionnaires to vendors/clients, collect responses in-app, auto-score | Vendor CRUD only in Eramba; questionnaire is a separate Google Sheets / Notion / doc template deliverable, attached back to the vendor record |
| **Awareness Programs** | "Awareness Programs `Enterprise`" | Phishing simulation, security training campaigns, completion tracking, SCORM content | Out of scope for sandbox year-1 engagements; recommend external free tools (Curricula free tier, Habitu8 free content, KnowBe4 free phishing test) to clients |
| **Account Reviews** | "Account Reviews `Enterprise`" | Quarterly access-review workflows, attestation cycles, joiner/mover/leaver automation | Quarterly access reviews delivered as a Google Sheet + email template service; consultant runs them, doesn't need in-app workflow |

## Why we are NOT fighting these gates

The brief from `~/Desktop/IfeSec/Research/GRC-Consulting-Intelligence-Brief-2026-06-22.html`
(Section 10, "Tool Stack — Next 60 Days") was explicit:

> *"Set up an Eramba sandbox for budget-conscious startup clients. Freemium tier lets us
> demonstrate value without upfront tool cost."*

The brief assumes Eramba CE is enough for the GRC program foundation. The Enterprise
gates only matter for the **operational delivery layer** (questionnaires, training,
access reviews), which is a year-2 ask for most sub-$15K clients.

The brief's actual recommended pattern:

1. **Year 1 (in Eramba CE):** Risk register + Control library + Policy library + Asset
   inventory + Incident management + BCP. Free.
2. **Year 2 (graduate to Vanta/Drata/Tugboat Logic on the client's side):** Operational
   layer — continuous monitoring, automated evidence collection, vendor questionnaires.
   Client pays for tool licenses, we move them off Eramba.

So the gates are not a problem. They are a **feature of the engagement model.**

## Decision: questionnaire = later deliverable

Per direct user instruction (22 June 2026):

> *"In terms of the Vendor Risk Workflow, I would like to use the Eramba Vendor crud only
> for now. Once we wrap our heads around this platform, then we can build a Vendor Risk
> Questionnaire template."*

The vendor-risk questionnaire is **deferred** until we are comfortable with the rest
of the Eramba workflow. It will be a standalone deliverable, not an Eramba module.

## Verification

The three "Enterprise" badges appear in the live sidebar. See screenshot
`screenshots/06-compliance-analysis.png` for the broader Compliance Management view, or
inspect any of the screenshots that show the left sidebar (all v3 screenshots show it).

Programmatic verification (from `inspect_eramba.py` output, `docs/00-dom-inspection.txt`):

```
<a> text='Online AssessmentsEnterprise' href=https://www.eramba.org/eramba-software
<a> text='Awareness ProgramsEnterprise' href=https://www.eramba.org/eramba-software
<a> text='Account ReviewsEnterprise' href=https://www.eramba.org/eramba-software
```
