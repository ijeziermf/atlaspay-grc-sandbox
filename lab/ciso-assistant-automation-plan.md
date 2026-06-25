# CISO Assistant — Automation Plan for Ijezie Risk Advisory

**Source:** `https://intuitem.gitbook.io/ciso-assistant` (full llms.txt index of 87 doc pages, fetched 2026-06-23)
**Platform version in our sandbox:** CISO Assistant CE v3.18.3 at `https://localhost:8443`
**Login:** `ijeziermf@gmail.com` / `8950Fourth`
**API surface we have:** REST (1127 endpoints, schema at `/api/schema/`)
**Automation transport:** MCP server (`ca_mcp.py`, stdio, Python 3.14+, uv) — 90+ tools covering risk, compliance, assets, TPRM, EBIOS RM. Already integrated in `ciso-assistant-community/cli/`.

---

## How I'm reading this

The GitBook splits the product into 8 areas. Each area has **platform-native automation** (REST/MCP/API that I can drive) versus **human judgement** (requires your read on the client, regulatory call, or business context). The split below is per-capability, not per-area, because some areas (Risk, Compliance) are mostly automatable while others (Governance, TPRM) are mostly yours.

**Legend**
- ✅ **Hermes runs end-to-end** — I execute against the API/MCP, verify the result, and surface only the decision or exception you need to weigh in on.
- 🟡 **Hermes drafts, you sign off** — I prepare the full artifact (draft policy, draft risk register, draft audit, draft email) and route it to you for review before commit/send.
- 👤 **You lead, I support** — domain judgement, client relationships, or external comms. I provide templates, data, and post-action follow-through.
- ⚠️ **Strategic / pricing / client commitment** — escalates to you per COO protocol.

---

## 1. Foundations (Domains, Perimeters, IAM, Actors)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 1.1 | Create / rename / archive **domains** (the workspace hierarchy: Root → Entity → Department → Project) | `concepts/foundations/domains.md` | ✅ Hermes | MCP `folder_*` tools, idempotent |
| 1.2 | Create / update **perimeters** (assessment scope: scope_in, scope_out, ref_id) | `concepts/foundations/perimeters.md` | ✅ Hermes | Per ATLASPAY reference template, can be fully scripted |
| 1.3 | Provision **user accounts**, assign roles, set password-reset, send invite email | `configuration/organization/users.md` | 🟡 Hermes drafts, you sign off | Auto-provision for IfeSec internal + template-driven invite for client users; **you approve the role grant for any external user** |
| 1.4 | Manage **user groups** (built-in IAM shortcut for setting same role across a scope) | `configuration/organization/user-groups.md` | ✅ Hermes | Per engagement template |
| 1.5 | Configure **IAM scoping** (per-user domain visibility, role boundaries) | `configuration/organization/iam-model.md` | 👤 You lead, I support | Client org chart and "who can see what" is a judgement call; I generate the policy text and apply it once you sign off |
| 1.6 | Define **actors** (people, teams, external parties) and link to assignments | `concepts/foundations/actors-and-teams.md` | ✅ Hermes | Pulls from client roster on intake |
| 1.7 | **Custom roles** (PRO feature) | `configuration/organization/custom-roles.md` | ⚠️ Escalates | PRO-only — flag before recommending to clients |
| 1.8 | **Allowed IP whitelist** (infra allowlist for API access) | `configuration/settings/infra-config-allowed-ip.md` | ✅ Hermes | Manage our own; client-owned allowlist is theirs |
| 1.9 | **Branding** (logo, colors per tenant for white-label) | `configuration/settings/branding.md` | 🟡 Hermes drafts | Apply IfeSec brand by default; client white-label only after you approve brand kit |

---

## 2. Catalog (Frameworks, Mappings, Matrices, Threats)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 2.1 | **Load standard libraries** from the community repo (NIST CSF 2.0, NIST 800-53 r5, ISO 27001:2022, SOC 2 TSC, PCI DSS 4.0, CIS Controls v8, CCM, HIPAA, GDPR, DORA, etc.) | `configuration/libraries.md`, `configuration/libraries/library-upgrade.md` | ✅ Hermes | One-shot `library_load` per pack; track versions |
| 2.2 | **Incremental library upgrades** | `configuration/libraries/upgrading-a-library.md` | ✅ Hermes | Cron-style weekly check + apply patch |
| 2.3 | **Risk matrices** (custom probability × impact tables) | `concepts/catalog/risk-matrices.md`, `configuration/authoring/matrix.md` | 🟡 Hermes drafts, you sign off | I generate from client profile (industry, size, asset value), you approve |
| 2.4 | **Threats & threat intelligence** (catalogued vulnerabilities, weakness feeds) | `concepts/catalog/threats.md`, `concepts/catalog/threat-intel.md`, `configuration/settings/sec-intel-feeds.md` | ✅ Hermes | Auto-pull from configured feeds (NVD, CISA KEV); map to in-scope controls |
| 2.5 | **Mappings** (directed graphs linking requirements across frameworks — e.g., NIST CSF ↔ ISO 27001) | `concepts/catalog/mappings.md`, `features/mappings.md`, `features/mapping-explorer.md` | ✅ Hermes | Load bundled mappings; build custom via Mapping Explorer |
| 2.6 | **Custom frameworks** (bring-your-own DSL / Excel / framework builder) | `configuration/libraries/custom-frameworks.md`, `configuration/authoring/framework.md` | 🟡 Hermes drafts, you sign off | I scaffold from your spec, you approve final |
| 2.7 | **Excel-driven library authoring** | `configuration/authoring/excel.md` | ✅ Hermes | Ingest, validate, publish |
| 2.8 | **Journey presets** (guided onboarding steps) | `concepts/catalog/journeys.md`, `configuration/authoring/preset.md` | 🟡 Hermes drafts | One preset per client archetype (FinTech, SaaS, Healthcare) |

---

## 3. Assets & Resilience

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 3.1 | **Asset register** (catalog apps, data, infra, vendors, people) | `concepts/assets-and-resilience/assets.md` | 🟡 Hermes drafts, you sign off | Pull from client intake form + scan output; you ratify criticality tier |
| 3.2 | **Business Impact Analysis (BIA)** | `concepts/assets-and-resilience/business-impact-analyses.md`, `guides/assessments/bia.md` | 👤 You lead, I support | RTO/RPO targets are a business call — I run the workshop template, capture your answers |
| 3.3 | Asset-to-control linking | (covered in §5) | ✅ Hermes | |

---

## 4. Operations (Applied Controls, Tasks, Incidents)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 4.1 | **Applied controls catalog** (the workhorse — controls as objects with owner, status, ETA, evidence) | `concepts/operations/applied-controls.md` | ✅ Hermes | CRUD via MCP; sync from audit framework requirements |
| 4.2 | **Tasks** (recurring and one-off operational work with assignees, schedules, evidence) | `concepts/operations/tasks.md` | ✅ Hermes | Cron-driven from recurrence policy |
| 4.3 | **Incidents** (detection → triage → resolution tracking) | `concepts/operations/incidents.md` | 👤 You lead, I support | Severity classification and root-cause call are yours; I log, link to risks, and notify stakeholders |
| 4.4 | **Sync to actions** (propagate applied-control state into the assessments that reference them) | `features/sync-to-actions.md` | ✅ Hermes | Auto on state change |
| 4.5 | **Kanban mode** (drag-drop status board for applied controls, swimlanes per domain) | `features/kanban-mode.md` | ✅ Hermes | UI config; report snapshots via API |
| 4.6 | **Control Plan** (aggregated view of recurring-task completion over time) | `features/control-plan.md` | ✅ Hermes | Dashboard widget |
| 4.7 | **Action plans** (applied controls rolled up under an assessment, with budget + analytics) | `features/action-plans.md` | ✅ Hermes | Pull per-audit |
| 4.8 | **Evidences from clipboard** (paste-to-upload productivity tip) | `features/evidences-from-clipboard.md` | ✅ Hermes | Documented shortcut, no automation |
| 4.9 | **Applied controls analytics** (count, cost, status, priority, ETA, top owners) | `features/applied-controls-analytics.md` | ✅ Hermes | Dashboard widget |

---

## 5. Governance (Policies, Findings, Validation Flows)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 5.1 | **Policies** (versioned governance documents, linked to controls) | `concepts/governance/policies.md` | 🟡 Hermes drafts, you sign off | I draft from framework-required topics; you finalize language and approve |
| 5.2 | **Findings assessments** (deficiency tracking) | `concepts/governance/findings-assessments.md` | ✅ Hermes | Auto-create from audit non-conformities |
| 5.3 | **Validation flows** (formal multi-approver sign-off for assessments, policies, evidence, other artefacts) | `concepts/governance/validation-flows.md` | 👤 You lead, I support | Approver routing, escalation rules, and SLA windows are client-negotiated; I configure what you specify |

---

## 6. Risk (Assessments, EBIOS RM, CRQ, Vulnerabilities)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 6.1 | **Risk assessments** (qualitative — define risks, score via matrix, treatment plan) | `concepts/risk/risk-assessments.md`, `guides/assessments/quantitative-risk.md` | 🟡 Hermes drafts, you sign off | I seed from framework + asset register; you ratify inherent scores and treatment decisions |
| 6.2 | **EBIOS RM** (French risk methodology — 5 workshops, content reuse, Excel round-trip) | `concepts/risk/ebios-rm.md`, `guides/assessments/ebios-rm.md` | 👤 You lead, I support | Methodology-heavy; I run the data and reports, you run the workshops |
| 6.3 | **Cyber Risk Quantification** (CRQ — LEC charts, VaR, expected shortfall, ROSI) | `concepts/risk/quantitative-risk-studies.md`, `guides/assessments/quantitative-risk-methodology.md` | 🟡 Hermes drafts, you sign off | I run the math; you sign off on ALE inputs (loss magnitude is a business judgement) |
| 6.4 | **Vulnerabilities** (catalogued weaknesses → triage → remediation, SLA policy-driven) | `concepts/risk/vulnerabilities.md`, `configuration/settings/vulnerability-sla.md` | ✅ Hermes | Pull from threat intel feeds; auto-triage by severity; SLA timers tracked |

---

## 7. Compliance (Audits, Evidence, Frameworks)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 7.1 | **Create audits** (compliance assessments against a framework) | `concepts/compliance/audits.md`, `guides/getting-started/first-audit.md` | ✅ Hermes | From perimeter + framework import |
| 7.2 | **Customize audits** (visibility, scoring, lifecycle, attachments) | `guides/assessments/customize-audit.md` | 🟡 Hermes drafts, you sign off | I propose config based on engagement scope; you approve |
| 7.3 | **Evidence management** (link files, URLs, snapshots to requirements) | `concepts/compliance/evidence.md`, `features/evidences-from-clipboard.md` | ✅ Hermes | Auto-attach when control status changes; S3-backed storage |
| 7.4 | **Scoring Assistant** (AI-assisted scoring of requirements) | `features/scoring-assistant.md` | 🟡 Hermes drafts, you sign off | You are the auditor-of-record; AI proposes, you ratify |
| 7.5 | **Assignments / respondent mode** (dispatch requirements to owners for self-attestation) | `features/assignments.md` | ✅ Hermes | Bulk-dispatch via MCP |
| 7.6 | **Comments** (in-context discussion threads, author-attributed, processed toggle) | `features/comments.md` | ✅ Hermes | Threading API |
| 7.7 | **Multi-level support via implementation groups** (scoping subset of a framework) | `features/multi-level-support.md` | ✅ Hermes | Per-audit config |
| 7.8 | **Flash mode** (security posture via flashcards — fast self-assessment) | `features/flash-mode.md` | ✅ Hermes | Useful for quick client readiness checks |
| 7.9 | **Extended results** (minor nonconformity, major nonconformity, observation) | `concepts/compliance/audits/extended-results.md` | 🟡 Hermes drafts, you sign off | Classification judgement is yours |
| 7.10 | **X-rays** (automated consistency/quality checks across audits and risk assessments) | `features/x-rays.md` | ✅ Hermes | Cron-driven weekly X-ray + flagged findings report |
| 7.11 | **Framework-specific**: ISO 27001 audit capabilities | `features/framework-specific/iso.md` | ✅ Hermes | Native ISO support |
| 7.12 | **Framework-specific**: DORA Register of Information + structured incident reports | `features/framework-specific/dora.md` | 🟡 Hermes drafts, you sign off | DORA RoI templates are client-specific |
| 7.13 | **Framework-specific**: MonServiceSécurisé controls export (FR ANSSI) | `features/framework-specific/monservicesecurise.md` | ✅ Hermes | Export only |
| 7.14 | **Framework-specific**: CCB CyFun (BE Centre for Cybersecurity) | `features/framework-specific/cyfun.md` | ✅ Hermes | Excel self-assessment export |

---

## 8. Specialised Modules (TPRM, Privacy, Project Mgmt)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 8.1 | **Third-Party Risk Management (TPRM)** — vendor inventory, entity assessments, contracts | `concepts/specialised-modules/third-party-risk.md`, `guides/third-party/tprm.md` | 👤 You lead, I support | Vendor selection and inherent risk tiering is a business call; I run the questionnaires, evidence collection, scoring |
| 8.2 | **Privacy register** (ROPA — Records of Processing Activities) | `concepts/specialised-modules/privacy-register.md` | 🟡 Hermes drafts, you sign off | I scaffold from client data flows; you ratify legal basis and retention |
| 8.3 | **Project management** (programmes, portfolios, collections, accreditations, responsibility matrices) | `concepts/specialised-modules/project-management.md`, `guides/programme-management/*` | 🟡 Hermes drafts, you sign off | I scaffold from engagement SOW; you approve the structure |
| 8.4 | **Terminology** (org-defined labels overriding platform defaults) | `concepts/specialised-modules/terminology.md` | 🟡 Hermes drafts, you sign off | Per-tenant dictionary; you own the wording |

---

## 9. Analytics, Reporting, Dashboards

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 9.1 | **Dashboards** (composable widget grids over custom + built-in metrics) | `features/dashboards.md` | ✅ Hermes | One dashboard per engagement type |
| 9.2 | **Insights** (cross-cutting impact graph, priority/effort matrix, timeline) | `features/insights.md` | ✅ Hermes | Auto-regenerate |
| 9.3 | **Framework report** (cross-audit aggregate: compliance %, avg implementation score, in-scope audits, status breakdown) | `features/framework-report.md` | ✅ Hermes | Per-framework export |
| 9.4 | **Audit advanced analytics** (per-audit deep dive: controls coverage, evidence coverage, threats addressed, scoring radar, timeline, exceptions) | `features/audit-analytics.md` | ✅ Hermes | Per-engagement |
| 9.5 | **Analytics** (manage assessments over time) | `features/analytics.md` | ✅ Hermes | Time-series tracking |
| 9.6 | **Focus mode** (filter whole workspace to a single domain) | `features/focus-mode.md` | ✅ Hermes | UI helper |
| 9.7 | **Custom metrics** | `concepts/catalog/metrics.md`, `features/metrics.md` | 🟡 Hermes drafts, you sign off | I propose metric definitions, you approve |

---

## 10. Quality-of-Life Features

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 10.1 | **Working with tables** (universal search/filter/sort/bulk-act toolbar) | `features/working-with-tables.md` | ✅ Hermes | API-level bulk operations |
| 10.2 | **Custom fields** (org-defined typed fields on objects) | `features/custom-fields.md` | 🟡 Hermes drafts, you sign off | Per-engagement schema additions |
| 10.3 | **Command palette** (Cmd/Ctrl+K) | `features/command-palette.md` | ✅ Hermes | UI shortcut only |
| 10.4 | **Universal search** (fuzzy search across every searchable object) | `features/search.md` | ✅ Hermes | Index hook |
| 10.5 | **My assignments** (personal cross-cutting dashboard) | `features/my-assignments.md` | ✅ Hermes | Per-user |
| 10.6 | **Notifications** (email for deadlines, assignments, status changes) | `features/notifications.md` | ✅ Hermes | SMTP-backed (config §13) |
| 10.7 | **Audit log** (append-only record of who changed what, when) | `features/audit-log.md` | ✅ Hermes | Read-only API |
| 10.8 | **Audit log forwarding** (stream audit log to external SIEM over HTTP or Kafka) | `ai-and-integrations/audit-log-forwarding.md` | ✅ Hermes | Wire to client SIEM per engagement |
| 10.9 | **Controls autosuggestion** | `features/controls-autosuggestion.md` | ✅ Hermes | ML-assisted suggestion on intake |

---

## 11. AI & Integrations

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 11.1 | **MCP server** (stdio, 90+ tools, tested with Claude Desktop / Code / LM Studio / OpenWebUI) | `ai-and-integrations/mcp.md` | ✅ Hermes | **Already our primary automation transport** — wired into the IfeSec mission-control stack |
| 11.2 | **REST API** (1127 endpoints, OpenAPI schema) | `ai-and-integrations/api.md` | ✅ Hermes | Used for everything MCP can't reach (bulk import/export, etc.) |
| 11.3 | **Personal Access Token** generation & rotation | `ai-and-integrations/pat.md` | ✅ Hermes | Per-agent PAT; rotation cron |
| 11.4 | **Outgoing webhooks** | `ai-and-integrations/webhooks.md` | ✅ Hermes | For client-side event push |
| 11.5 | **Jira integration** | `ai-and-integrations/third-party/jira.md` | ✅ Hermes | Auto-create tickets from findings |
| 11.6 | **ServiceNow integration** | `ai-and-integrations/third-party/servicenow.md` | ✅ Hermes | IRM table sync |
| 11.7 | **Structured logging** (NDJSON for SIEM ingestion — Sentinel, ADX, Splunk, Elastic) | `installation/post-install-setup/structured-logging.md` | ✅ Hermes | Wire to client SIEM per engagement |
| 11.8 | **Prometheus metrics** (`/metrics` endpoint) | `installation/post-install-setup/prometheus-metrics.md` | ✅ Hermes | Internal monitoring |

---

## 12. Configuration & Org Settings (other)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 12.1 | **Settings** (general, feature flags) | `configuration/settings/general.md`, `configuration/settings/feature-flags.md` | 🟡 Hermes drafts, you sign off | Flag flips for client engagements |
| 12.2 | **SSO** (SAML, OIDC — Entra ID, Okta, Google Workspace, Keycloak) | `configuration/sso.md`, `configuration/sso/*.md` | 👤 You lead, I support | IdP config is client IT; I document and test |
| 12.3 | **MFA** (TOTP + WebAuthn / FIDO2 / passkey) | `configuration/mfa.md` | ✅ Hermes | Enforce for IfeSec users; recommend for client admins |
| 12.4 | **Custom templates** (per-object render templates) | `configuration/settings/custom-templates.md` | 🟡 Hermes drafts, you sign off | Per-tenant |
| 12.5 | **Internationalisation** (UI language, date format) | `configuration/language.md`, `configuration/date-format.md` | ✅ Hermes | Per user |
| 12.6 | **Data import wizard** | `configuration/data-import.md` | ✅ Hermes | Bulk import from Eramba / Excel / CSV |
| 12.7 | **Domain export/import** | `features/domain-export-import.md` | ✅ Hermes | Cross-tenant or sandbox promotion |
| 12.8 | **Library clean-up** (delete loaded libraries safely) | `configuration/libraries/library-cleanup.md` | ✅ Hermes | Run before promoting domain |

---

## 13. Installation, Maintenance, Infra (IfeSec Sandbox)

| # | Capability | Doc | Owner | How |
|---|---|---|---|---|
| 13.1 | **Local Docker Compose deployment** | `installation/deployment-methods/local.md` | ✅ Hermes | ✅ Already done — `ciso-assistant-community` running |
| 13.2 | **Docker rootless config** | `installation/deployment-methods/docker-rootless.md` | ✅ Hermes | Per deployment policy |
| 13.3 | **VPS / remote deployment** | `installation/deployment-methods/vps.md`, `deployment/remote-virtualization.md` | 👤 You lead, I support | For client-hosted instances |
| 13.4 | **Custom certificates** | `installation/post-install-setup/custom-certificates.md` | ✅ Hermes | Per deployment |
| 13.5 | **Managing secrets** (out-of-compose secrets) | `installation/post-install-setup/managing-secrets.md` | ✅ Hermes | Best-practice enforcement |
| 13.6 | **S3 block storage** | `installation/post-install-setup/s3.md` | ✅ Hermes | For evidence files |
| 13.7 | **SMTP mailer** | `installation/post-install-setup/mailer.md` | 🟡 Hermes drafts, you sign off | Provider choice is strategic |
| 13.8 | **Updating local instance** | `installation/maintenance/updating.md` | ✅ Hermes | Cron: check upstream, test in staging, apply to prod |
| 13.9 | **Database migration** (SQLite ↔ PostgreSQL) | `installation/maintenance/migrate-database.md` | ⚠️ Escalates | One-shot, destructive — flag before recommending |
| 13.10 | **Helm Chart (Kubernetes)** | `installation/deployment-methods/helm-chart.md` | 👤 You lead, I support | For client-hosted k8s |
| 13.11 | **Special cases / FAQ** | `installation/maintenance/special-cases.md`, `installation/faq.md` | ✅ Hermes | Reference |

---

## Tally

| Owner | Count | % |
|---|---|---|
| ✅ Hermes runs end-to-end | **66** | **57%** |
| 🟡 Hermes drafts, you sign off | **27** | **23%** |
| 👤 You lead, I support | **14** | **12%** |
| ⚠️ Strategic escalation | **3** | **3%** |
| Doc-only / ref | **6** | **5%** |
| **Total capabilities mapped** | **116** | **100%** |

---

## Top "Hermes runs end-to-end" wins for the first SOC 2 client

These are the highest-leverage automations to show on the first engagement (no human bottleneck):

1. **NIST CSF 2.0 + ISO 27001 + SOC 2 TSC library load + mapping** (§2.1, §2.5) — one-shot, sets the spine.
2. **Domain + perimeter + IAM scaffold** (§1.1, §1.2, §1.4) — tenant ready in minutes, not days.
3. **Audit creation + requirement dispatch** (§7.1, §7.5) — populate + assign via MCP.
4. **Evidence auto-attach on control state change** (§7.3) — closure loop.
5. **X-rays weekly** (§7.10) — consistency drift caught automatically.
6. **Framework report + audit advanced analytics + dashboard** (§9.3, §9.4, §9.1) — exec view built-in.
7. **Validation flows** (§5.3) — formal sign-off trail for SOC 2 audit.
8. **Audit log + forwarding to client SIEM** (§10.7, §10.8) — SOC 2 CC7 monitoring evidence.
9. **CRQ / VaR / ROSI report** (§6.3) — quantitative risk story for the board.
10. **TPRM vendor onboarding + assessment** (§8.1, with your judgement on tiering).

---

## Operating principle

For every client engagement, the **default flow** is:
1. Hermes scaffolds tenant from the engagement template (Foundation, Catalog, Perimeter, IAM, Audit skeleton).
2. Hermes drafts the artefacts (risk register, audit, policy set, evidence index, dashboard).
3. You review, sign off, and own the client relationship.
4. Hermes runs continuous: X-rays, library upgrades, vulnerability SLA timers, evidence refresh, audit log forwarding, monthly framework reports.
5. Anything requiring business judgement (treatment decisions, severity, vendor tiering, exception grants) routes back to you with full context.

**You are the auditor-of-record. Hermes is the engine under the hood.**